import os
import sys
import string
import subprocess

from lexer import lexer
from error import error, setFile, setVersion, setLineNumber

from termcolor import *
from glob import glob

# META STUFF
VERSION = "1.0.2"
setVersion(VERSION)
setLineNumber(0)


setFile("[init]")
if len(sys.argv) == 1:
    error("No input file specified.", "chi <filename>")

file = sys.argv[-1]
var = {}
functions = {"use": None, "out": None, "put": None, "add": None, "concat": None, "type": None, "in": None, "len": None, "conv": None, "shell": None, "readfile": None, "writefile": None}
lib = [os.getcwd()+os.sep+"lib"]

T_LT = {"type": "symbol", "value": "<"}
T_GT = {"type": "symbol", "value": ">"}
T_EQ = {"type": "symbol", "value": "="}



def runFunc(func, args):
    #global functions
    ret = {"type": "none", "value": "none"}

    if func in functions:
        if functions[func] == None:
            pass
        elif type(functions[func]) == list:
            LN = 0
            INDENT = 0
            fcode = functions[func]
            while LN != len(fcode)-1:
                setLineNumber(LN+1)
                line = fcode[LN]
                line = lexer(line.strip(), LN)

                LN += 1
                if line == [] or line[0] == {"type": "symbol", "value": "@"}:
                    continue


                parser(line)
            return ret

    if func == "out":
        for arg in args:
            print(arg["value"] + " ", end="")
        print()

    elif func == "put":
        for arg in args:
            print(arg["value"], end="")
        print()

    elif func == "use":
        if args[0]["type"] != "str":
            error("Invalid type", args[0]["type"]+" but expected <str>")
        fn = os.path.basename(args[0]["value"])
        _f = []

        #print("! Loading all modules from", fn)
        for l in lib:
            for root, sub, files in os.walk(os.path.abspath("lib"+os.sep+fn)):
                for file in files:
                    if file[-4:] != ".chi":
                        continue

                    fulldir = os.sep.join([l, fn]+sub+[file])
                    fdir = os.sep.join([fn]+sub+[file[:-4]])
                    _fn = ":".join(fdir.split(os.sep))

                    with open(fulldir) as ffile:
                        _f = ffile.read().split("\n")
                    functions[_fn] = _f


    elif func == "add":
        if len(args) <= 1:
            error("Invalid number of arguments", "add <float/int> <float/int> (float/int) ... -> <float/int>")

        e = 0
        isFloat = False
        for arg in args:
            if arg["type"] != "float" and arg["type"] != "int":
                error("Invalid type", arg["type"]+" but expected float or int")
            if arg["type"] == "float":
                isFloat = True
            e += float(arg["value"])

        if isFloat:
            e = float(e)
            t = "float"
        else:
            e = int(e)
            t = "int"

        ret = {"type": t, "value": str(e)}

    elif func == "concat":
        if len(args) <= 1:
            error("Invalid number of arguments", "concat <*> <*> (*) ... -> <str>")
        e = ""
        for arg in args:
            e += arg["value"]

        ret = {"type": "str", "value": e}

    elif func == "conv":
        if len(args) != 2:
            error("Invalid number of arguments", "conv <*> <type> -> <type>")
        if args[0]["type"] == args[1]["value"]:
            ret = args[0]
        else:
            if args[1]["value"] == "float":
                try:
                    ret = {"type": "float", "value": float(args[0]["value"])}
                except ValueError:
                    error("Type error", "Cannot convert non-numerical object to float")
            elif args[1]["value"] == "int":
                try:
                    ret = {"type": "int", "value": int(args[0]["value"])}
                except ValueError:
                    error("Type error", "Cannot convert non-numerical object to int")
            elif args[1]["value"] == "str":
                try:
                    ret = {"type": "str", "value": str(args[0]["value"])}
                except ValueError:
                    error("Type error", "Cannot convert non-representable object to str")
            else:
                error("Type error", "Unknown type " + args[1]["value"])


    elif func == "type":
        if len(args) > 1  or len(args) == 0:
            error("Invalid number of arguments", "type <var> -> <str>")

        ret = {"type": "str", "value": args[0]["type"]}

    elif func == "in":
        if len(args) > 1:
            error("Invalid number of arguments", "in (text) -> <str>")
        if len(args) == 1:
            t = args[0]["value"]
        else:
            t = ""

        i = input(t)

        ret = {"type": "str", "value": i}

    elif func == "len":
        if len(args) == 0 or len(args) > 1:
            error("Invalid number of arguments", "len <str> -> <int>")

        ret = {"type": "int", "value": str(len(args[0]["value"]))}

    elif func == "shell":
        a = args[0]
        if a["type"] != "str":
            error("Invalid type", args[0]["type"]+" but expected <str>")
        sp = subprocess.Popen(a["value"].split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = sp.communicate()

        ret = {"type": "str", "value": stdout.decode()}

    elif func == "readfile":
        if len(args) != 1:
            error("Invalid number of arguments", "readfile <str>")

        if args[0]["type"] != "str":
            error("Invalid type", args[0]["type"]+" but expected <str>")

        filename = args[0]["value"]
        try:
            with open(os.path.abspath(filename)) as ff:
                ret = {"type": "str", "value": ff.read()}

        except FileNotFoundError:
            error("File not found", filename)

    elif func == "writefile": # writefile <filename> <content>
        if len(args) != 2:
            error("Invalid number of arguments", "writefile <str> <str>")

        if args[0]["type"] != "str":
            error("Invalid type", args[0]["type"]+" but expected <str>")
        if args[1]["type"] != "str":
            error("Invalid type", args[1]["type"]+" but expected <str>")

        filename = args[0]["value"]
        content = args[1]["value"]

        try:
            with open(os.path.abspath(filename), "w+") as ff:
                ff.write(content)

        except FileNotFoundError:
            error("File not found", filename)

        # Return none

    elif func == "appendfile": # appendfile <filename> <content>
        if len(args) != 2:
            error("Invalid number of arguments", "appendfile <str> <str>")

        if args[0]["type"] != "str":
            error("Invalid type", args[0]["type"]+" but expected <str>")
        if args[1]["type"] != "str":
            error("Invalid type", args[1]["type"]+" but expected <str>")

        filename = args[0]["value"]
        content = args[1]["value"]

        try:
            with open(os.path.abspath(filename), "a") as ff:
                ff.write(content)

        except FileNotFoundError:
            error("File not found", filename)

        # Return none

    elif func == "clearfile": # clearfile <filename>
        if len(args) != 1:
            error("Invalid number of arguments", "clearfile <str>")

        filename = args[0]["value"]

        try:
            with open(os.path.abspath(filename), "w+") as ff:
                pass

        except FileNotFoundError:
            error("File not found", filename)

        # Return none



    return ret

def processFunc(line):
    args = []
    for c, a in enumerate(line[1:]):
        if c % 2 == 0 and a != {"type": "symbol", "value": ","}:
            if a["type"] == "var":
                if a["value"] in var:
                    a = var[a["value"]]
                else:
                    error("Undefined variable", a["value"])

            elif a["type"] == "symbol":
                if a["value"] == "+":
                    error("Invalid syntax", "No concatenation/addition allowed in function arguments")
                else:
                    error("Invalid syntax", "No mathematical operations allowed in function arguments")


            args.append(a)

        elif c % 2 == 0 and a == {"type": "symbol", "value": ","}:
            error("Invalid syntax", "Non-comma expected")

        elif c % 2 == 1 and a != {"type": "symbol", "value": ","}:
            error("Invalid syntax", "comma expected")

        elif c % 2 == 1 and a == {"type": "symbol", "value": ","}:
            pass

    ret = runFunc(line[0]["value"], args)
    return ret




def parser(line):
    global LN, INDENT
    if line[0]["type"] == "var":
        if line[0]["value"] in functions:
            processFunc(line)
        elif line[0] == {"type": "var", "value": "if"}:
            IF = False

            if line[1] == {"type": "symbol", "value": "!"}:
                NOT = True
                ifargs = line[2:]
            else:
                NOT = False
                ifargs = line[1:]

            a = ifargs[0]
            if ifargs[-1] == {"type": "symbol", "value": "{"}:
                del ifargs[-1]
                INDENT += 1

            a = ifargs[0]
            del ifargs[0]
            b = ifargs[-1]
            del ifargs[-1]

            if a["type"] == "var":
                if a["value"] in var:
                    a = var[a["value"]]
                else:
                    error("Undefined variable", a["value"])

            if b["type"] == "var":
                if b["value"] in var:
                    b = var[b["value"]]
                else:
                    error("Undefined variable", b["value"])

            if ifargs == [T_EQ]:
                error("Invalid syntax", "Did you mean == instead of =?")

            elif ifargs == [T_EQ, T_EQ]:
                if a == b:
                    IF = True

            elif ifargs == [T_GT, T_EQ]:
                if a["type"] != "float" and a["type"] != "int":
                    error("Invalid type", a["type"]+" but expected float or int")

                if float(a["value"]) >= float(b["value"]):
                    IF = True

            elif ifargs == [T_LT, T_EQ]:
                if a["type"] != "float" and a["type"] != "int":
                    error("Invalid type", a["type"]+" but expected float or int")

                if float(a["value"]) <= float(b["value"]):
                    IF = True

            elif ifargs == [T_GT]:
                if a["type"] != "float" and a["type"] != "int":
                    error("Invalid type", a["type"]+" but expected float or int")

                if float(a["value"]) > float(b["value"]):
                    IF = True

            elif ifargs == [T_LT]:
                if a["type"] != "float" and a["type"] != "int":
                    error("Invalid type", a["type"]+" but expected float or int")

                if float(a["value"]) < float(b["value"]):
                    IF = True

            if NOT == True:
                IF = not IF

            if code[LN] == "{":
                INDENT += 1
                LN += 1

            IFCODE = []
            IF_ENDLN = LN

            _INDENT = 1
            for _line in code[LN:]:
                IF_ENDLN += 1
                line = lexer(_line.strip(), 0)
                if {"type": "symbol", "value": "{"} in line:
                    _INDENT += 1
                elif {"type": "symbol", "value": "}"} in line:
                    _INDENT -= line.count({"type": "symbol", "value": "}"})
                    #if line[1] == {"type": "var", "value": "else"}:

                if _INDENT == 0:
                    break

                IFCODE.append(_line)

            if IF:
                for line in IFCODE:
                    line = lexer(line.strip(), LN)
                    parser(line)
            LN = IF_ENDLN





        else:
            if line[1] == T_EQ:
                if line[2]["type"] == "var":
                    if line[2]["value"] in functions:
                        v = processFunc(line[2:])
                    elif line[2]["value"] in var:
                        v = var[line[2]]
                    else:
                        error("Undefined variable/function", line[2]["value"])
                else:
                    v = line[2]

                var[line[0]["value"]] = v
            else:
                error("Invalid function", line[0]["value"])

    elif line[0] == {"type": "symbol", "value": "}"}:
        INDENT -= 1
        if INDENT < 0:
            error("Invalid syntax", "Unmatched }")




try:
    with open(os.path.abspath(file)) as codefile:
        code = codefile.read().split("\n")
except FileNotFoundError:
    error("Error in input file", "Not found")
except:
    error("Error in input file", "Unknown error")

# For errors
setFile(file)

try:
    LN = 0
    INDENT = 0
    while LN != len(code)-1:
        setLineNumber(LN+1)
        line = code[LN]
        line = lexer(line.strip(), LN)

        LN += 1
        if line == [] or line[0] == {"type": "symbol", "value": "@"}:
            continue


        parser(line)


except KeyboardInterrupt:
    error("Aborted.", "^C")
