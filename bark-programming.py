from sys import *
import pyttsx3
import math

engine = pyttsx3.init()
voices = engine.getProperty('voices')
loop_ended = 0
variables = {}

def token(data):
    token = ""
    token_list = []
    speech = 0
    integer = 0
    for i in data:
        integer = 0
        if i == '"':
            if speech == 1:
                speech = 0
            else:
                speech = 1
        if (i != "\n" and i != " " and i != "\t") or (speech == 1 and i != '"'):
            token += i
        if (i == " " or i == "\n" or i == "\t") and speech != 1:
            token_list.append(token)
            token = ""
    token_list.append(token)
    print(token_list)
    return token_list

def evaluate(token_list):
    evaluated_list = []
    nuller = 0
    for i in token_list:
        if i == "":
            nuller=0
        elif len(i) > 1 and (i[0] == "+" and i[1] != "=") or (i[0] == "-" and i[1] != "=") or (i[0] == "*" and i[1] != "=") or (i[0] == "/" and i[1] != "=") or i[0] == "(" or i[0] == ")" or i[0] == '0' or i[0] == '1' or i[0] == '2' or i[0] == '3' or i[0] == '4' or i[0] == '5' or i[0] == '6' or i[0] == '7' or i[0] == '8' or i[0] == '9':
            temp = i
            for k in variables:
                temp = str(temp).replace("$" + k, str(variables[k]))
            evaluated_list.append(eval(temp))
        else:
            if i != '':
                temp = i
                for k in variables:
                    temp = str(temp).replace("$" + k, str(variables[k]))
                evaluated_list.append(eval(temp))
            
    return evaluated_list

def parse(token_list):
    j = 0
    done = 0
    repeating = 0
    num = 0
    while done == 0:
        if j >= len(token_list)-1:
            break
        if token_list[j] == "write":
            final = token_list[j+1]
            for k in variables:
                final = final.replace("$" + k, str(variables[k]))
            print(eval(str(final)))
            j+=1
        elif token_list[j] == "writeAtEnd":
            final = token_list[j+1]
            for k in variables:
                final = final.replace("$" + k, str(variables[k]))
            print(eval(str(final)),end="")
            j+=1
        elif token_list[j] == "writeAtEnd_stop":
            print("")
        elif token_list[j] == "let":
            num = str(token_list[j+3])
            for k in variables:
                num = num.replace("$" + k, str(variables[k]))
            num = eval(str(num))
            if token_list[j+2] == "=":
                variables[token_list[j+1]] = num
            elif token_list[j+2] == "-=":
                amount = int(variables[token_list[j+1]])
                amount -= int(num)
                variables[token_list[j+1]] = str(amount)
            elif token_list[j+2] == "+=":
                amount = int(variables[token_list[j+1]])
                amount += int(num)
                variables[token_list[j+1]] = str(amount)
            j += 3
        elif token_list[j] == "if":
            a = str(token_list[j+1])
            b = str(token_list[j+3])
            for k in variables:
                a = a.replace("$"+ k, str(variables[k]))
                b = b.replace("$"+ k, str(variables[k]))
            a = int(eval(str(a)))
            b = int(eval(str(b)))
            if a == b and str(token_list[j+2]) == '=':
                j+=3
            elif a > b and str(token_list[j+2]) == ">":
                j+=3
            elif a < b and str(token_list[j+2]) == "<":
                j+=3
            elif a >= b and str(token_list[j+2]) == ">=":
                j+=3
            elif a <= b and str(token_list[j+2]) == "<=":
                j+=3
            elif a != b and str(token_list[j+2]) == "!=":
                j+=3
            else:
                while token_list[j] != 'break' and token_list[j] != 'else':
                    j+=1
                if token_list[j-1] == "else":
                    j-=1
        elif token_list[j] == "stringIf":
            a = token_list[j+1]
            b = token_list[j+3]
            for k in variables:
                a = str(a).replace("$" + k, str(variables[k]))
            for k in variables:
                b = str(b).replace("$" + k, str(variables[k]))
            if str(a)[0] == '"':
                a = str(a)[1:]
            if str(a)[-1:] == '"':
                a = str(a)[0:-1]
            if str(b)[0] == '"':
                b = str(b)[1:]
            if str(b)[-1:] == '"':
                b = str(b)[0:-1]
            print(a)
            print(b)
            if str(a) == str(b) and token_list[j+2] == "=":
                j+=3
            elif str(a) != str(b) and token_list[j+2] == "!=":
                j+=3
            elif str(b) in str(a) and token_list[j+2] == "contains":
                j+=3
            elif str(a) in str(b) and token_list[j+2] == "in":
                j+=3
            else:
                while token_list[j] != 'break' and token_list[j] != 'else':
                    j+=1
                if token_list[j-1] == "else":
                    j-=1
        elif token_list[j] == "repeat":
            if repeating == 0:
                to_repeat = token_list[j+1]
                for k in variables:
                    to_repeat = str(to_repeat).replace("$" + k, str(variables[k]))
                to_repeat = eval(str(to_repeat))
                to_repeat = int(to_repeat)
                tj = j
                while token_list[tj] != 'breakRepeat':
                    tj+=1
                start = j
                end = tj
                repeats = 0
                j+=1
                repeating = 1
            else:
                j+=1
        elif token_list[j] == "getInput":
            temp = input(token_list[j+1])
            variables[token_list[j+2]] = temp
            j += 2
        elif token_list[j] == "else":
            while token_list[j] != 'break':
                j+=1
            j+=1
        elif token_list[j] == "end":
            break
        elif token_list[j] == "callRoutine":
            funcname = token_list[j+1]
            prev_j = j-2
            j = 0
            while token_list[j] != "routine" or token_list[j+1] != str(funcname):
                j += 1
            j += 1
        elif token_list[j] == "break":
            j+=0
        elif token_list[j] == "speak":
            text = str(token_list[j+1])
            for k in variables:
                text = text.replace("$" + k, str(variables[k]))
            text = str(text)
            engine.say(text)
            engine.runAndWait()
            j+=1
        elif token_list[j] == "speakVoice":
            voice = token_list[j+2]
            for k in variables:
                voice = str(voice).replace("$" + k, str(variables[k]))
            voice = eval(str(voice))
            voice = int(voice)
            engine.setProperty('voice', voices[voice].id)
            j+=2
        elif token_list[j] == "speakRate":
            rate = token_list[j+2]
            for k in variables:
                rate = str(rate).replace("$" + k, str(variables[k]))
            rate = eval(str(rate))
            rate = int(rate)
            engine.setProperty('rate', rate)
            j+=2
        elif token_list[j] == "speakVolume":
            volume = token_list[j+2]
            for k in variables:
                volume = str(volume).replace("$" + k, str(variables[k]))
            volume = eval(str(volume))
            volume = int(volume)
            engine.setProperty('volume', volume)
            j+=2
        elif token_list[j] == "loop":
            loop_ended = 0
            lstart = j
        elif token_list[j] == "breakLoop":
            loop_ended = 1
        if j+1 <= len(token_list)-1:
            if token_list[j+1] == "loopEnd" and loop_ended == 0:
                j = lstart
                    
        if j+1 <= len(token_list)-1:
            if token_list[j+1] == "endRoutine":
                j = prev_j
                j+=2
        if j >= len(token_list)-1:
            break
        j += 1
        if token_list[j] == "breakRepeat":
            repeats += 1
            if repeats != to_repeat and repeating == 1:
                j = start
            else:
                repeating = 0
    print(variables)

def run_file(file):
    data = open(file, "r").read()
    tokens = token(data)
    parse(tokens)

def run_line(line):
    tokens = token(line)
    parse(tokens)

if input("1. Use shell or 2. Use file upload: 1 or 2 ") == "1":
    line = 0
    while True:
        line += 1
        run_line(input(f"{line} >"))
else:
    run_file(input("Please specify project directory: "))
    input('Press ENTER to exit')
