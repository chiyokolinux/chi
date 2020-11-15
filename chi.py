import sys
import os

from lexer import lexer
from error import Error
from condition import Cond

from termcolor import *
from importlib import import_module
from glob import glob
from random import *
import subprocess

VERSION = "1.1.1"
error = Error(VERSION, None, None)
var = {}
lib = os.getcwd() + os.sep + "lib" + os.sep

if len(sys.argv) == 1:
    error.error("No file specified", "chi (options) <filename>")

"""
##################################################
##### OPEN FILE
##################################################
"""

filename = sys.argv[-1]
try:
    with open(filename) as codeFile:
        code = codeFile.read().split("\n")

except FileNotFoundError:
    error.error("Invalid file specified", filename)

"""
##################################################
##### DEFINE FUNCTIONS
##################################################
"""

def lexrepr(l):
    """
    Turns an already lexed array into a string for better reading.
    For debugging only!
    """
    e = ""
    for i in l:
        e += i["value"] + " "
    
    return e[:-1]

def verbose(*text):
    cprint(" ".join([str(t) for t in text]), "yellow")

def processFunc(line):
    """
    Taking a lexed line as an input, this function checks the syntax and
    extracts the elements of this line:
    
    name = input "Name: "
             |     |
           processFunc
             |
           func-name: "input"
           func-args: ["Name: "]
             |
           runFunc(func-name, func-args)
             |
    name <---´
    """
    args = []
    for c, a in enumerate(line[1:]):
        if c % 2 == 0 and a != {"type": "symbol", "value": ","}:
            a = getValue(a)

            args.append(a)

        elif c % 2 == 0 and a == {"type": "symbol", "value": ","}:
            error.error("Invalid syntax", "Non-comma expected")

        elif c % 2 == 1 and a != {"type": "symbol", "value": ","}:
            error.error("Invalid syntax", "comma expected")

        elif c % 2 == 1 and a == {"type": "symbol", "value": ","}:
            pass

    ret = runFunc(line[0]["value"], args)
    return ret


def runFunc(func, args):
    #global functions
    ret = {"type": "none", "value": "none"}

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
            error.error("Invalid type", "got "+args[0]["type"]+" but expected <str>")
        fn = os.path.basename(args[0]["value"])
        _f = []

        #print("! Loading all modules from", fn)
        
        if fn == "random":
            functions["randint"] = None
            functions["randfloat"] = None
            functions["randchar"] = None
            functions["randupperchar"] = None
            functions["randlowerchar"] = None
            functions["randascii"] = None
            
        elif fn == "time":
            functions["datetime"] = None
            functions["unixtime"] = None
        
        else:
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
            error.error("Invalid number of arguments", "add <float/int> <float/int> (float/int) ... -> <float/int>")

        e = 0
        isFloat = False
        for arg in args:
            if arg["type"] != "float" and arg["type"] != "int":
                error.error("Invalid type", "got "+arg["type"]+" but expected float or int")
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
            error.error("Invalid number of arguments", "concat <*> <*> (*) ... -> <str>")
        e = ""
        for arg in args:
            e += arg["value"]

        ret = {"type": "str", "value": e}

    elif func == "conv":
        if len(args) != 2:
            error.error("Invalid number of arguments", "conv <*> <type> -> <type>")
        if args[0]["type"] == args[1]["value"]:
            ret = args[0]
        else:
            if args[1]["value"] == "float":
                try:
                    ret = {"type": "float", "value": float(args[0]["value"])}
                except ValueError:
                    error.error("Type error", "Cannot convert non-numerical object to float")
            elif args[1]["value"] == "int":
                try:
                    ret = {"type": "int", "value": int(args[0]["value"])}
                except ValueError:
                    error.error("Type error", "Cannot convert non-numerical object to int")
            elif args[1]["value"] == "str":
                try:
                    ret = {"type": "str", "value": str(args[0]["value"])}
                except ValueError:
                    error.error("Type error", "Cannot convert non-representable object to str")
            else:
                error.error("Type error", "Unknown type " + args[1]["value"])


    elif func == "type":
        if len(args) > 1  or len(args) == 0:
            error.error("Invalid number of arguments", "type <var> -> <str>")

        ret = {"type": "str", "value": args[0]["type"]}

    elif func == "in":
        if len(args) > 1:
            error.error("Invalid number of arguments", "in (text) -> <str>")
        if len(args) == 1:
            t = args[0]["value"]
        else:
            t = ""

        i = input(t)

        ret = {"type": "str", "value": i}

    elif func == "len":
        if len(args) == 0 or len(args) > 1:
            error.error("Invalid number of arguments", "len <str> -> <int>")

        ret = {"type": "int", "value": str(len(args[0]["value"]))}

    elif func == "shell":
        a = args[0]
        if a["type"] != "str":
            error.error("Invalid type", "got "+args[0]["type"]+" but expected <str>")
        sp = subprocess.Popen(a["value"].split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = sp.communicate()

        ret = {"type": "str", "value": stdout.decode()}

    elif func == "readfile":
        if len(args) != 1:
            error.error("Invalid number of arguments", "readfile <str>")

        if args[0]["type"] != "str":
            error.error("Invalid type", "got "+args[0]["type"]+" but expected <str>")

        filename = args[0]["value"]
        try:
            with open(os.path.abspath(filename)) as ff:
                ret = {"type": "str", "value": ff.read()}

        except FileNotFoundError:
            error.error("File not found", filename)

    elif func == "writefile": # writefile <filename> <content>
        if len(args) != 2:
            error.error("Invalid number of arguments", "writefile <str> <str>")

        if args[0]["type"] != "str":
            error.error("Invalid type", "got "+args[0]["type"]+" but expected <str>")
        if args[1]["type"] != "str":
            error.error("Invalid type", "got "+args[1]["type"]+" but expected <str>")

        filename = args[0]["value"]
        content = args[1]["value"]

        try:
            with open(os.path.abspath(filename), "w+") as ff:
                ff.write(content)

        except FileNotFoundError:
            error.error("File not found", filename)

        # Return none

    elif func == "appendfile": # appendfile <filename> <content>
        if len(args) != 2:
            error.error("Invalid number of arguments", "appendfile <str> <str>")

        if args[0]["type"] != "str":
            error.error("Invalid type", "got "+args[0]["type"]+" but expected <str>")
        if args[1]["type"] != "str":
            error.error("Invalid type", "got "+args[1]["type"]+" but expected <str>")

        filename = args[0]["value"]
        content = args[1]["value"]

        try:
            with open(os.path.abspath(filename), "a") as ff:
                ff.write(content)

        except FileNotFoundError:
            error.error("File not found", filename)

        # Return none

    elif func == "clearfile": # clearfile <filename>
        if len(args) != 1:
            error.error("Invalid number of arguments", "clearfile <str>")

        filename = args[0]["value"]

        try:
            with open(os.path.abspath(filename), "w+") as ff:
                pass

        except FileNotFoundError:
            error.error("File not found", filename)



    elif func == "randint":
        if len(args) != 2:
            error.error("Invalid number of arguments", "randint <int> <int> -> int")
        
        if args[0]["type"] != "int":
            error.error("Invalid type", "got "+args[0]["type"]+" but expected <int>")
        if args[1]["type"] != "int":
            error.error("Invalid type", "got "+args[1]["type"]+" but expected <int>")

        r = randint(int(args[0]["value"]), int(args[1]["value"]))
        ret = {"value": str(r), "type": "int"}
    
    elif func == "randfloat":
        if len(args) != 2:
            error.error("Invalid number of arguments", "randfloat <float/int> <float/int> -> float")
        
        if args[0]["type"] != "int" and args[0]["type"] != "float":
            error.error("Invalid type", "got "+args[0]["type"]+" but expected <float/int>")
        if args[1]["type"] != "int" and args[1]["type"] != "float":
            error.error("Invalid type", "got "+args[1]["type"]+" but expected <float/int>")

        r = uniform(float(args[0]["value"]), float(args[1]["value"]))
        ret = {"value": str(r), "type": "float"}
    
    elif func == "randchar":
        if len(args) > 0:
            error.error("Invalid number of arguments", "randchar -> str")

        r = choice(list(string.ascii_letters))
        ret = {"value": str(r), "type": "str"}
    
    elif func == "randlowerchar":
        if len(args) > 0:
            error.error("Invalid number of arguments", "randlowerchar -> str")

        r = choice(list(string.ascii_lowercase))
        ret = {"value": str(r), "type": "str"}
    
    elif func == "randupperchar":
        if len(args) > 0:
            error.error("Invalid number of arguments", "randupperchar -> str")

        r = choice(list(string.ascii_uppercase))
        ret = {"value": str(r), "type": "str"}
    
    elif func == "randascii":
        if len(args) > 0:
            error.error("Invalid number of arguments", "randascii -> str")

        r = choice(list(string.printable))
        ret = {"value": str(r), "type": "str"}
    
    
    
    elif func == "datetime":
        if len(args) > 1:
            error.error("Invalid number of arguments", "datetime <str> -> str")
        
        if len(args) == 0:
            ret = {"type": "str", "value": str(datetime.datetime.now().utcnow())}
        
        elif len(args) == 1:
            # Year          Y
            # Month         M
            # Day           D
            # Hour          h
            # Minute        m
            # Second        s
            # Millisecond   z
            
            if args[0]["type"] != "str":
                error.error("Invalid type", "got "+args[0]["type"]+" but expected <str>")
                
            d = args[0]["value"]
            d = d.replace("%Y", str(datetime.datetime.now().year))
            d = d.replace("%M", str(datetime.datetime.now().month))
            d = d.replace("%D", str(datetime.datetime.now().day))
            d = d.replace("%h", str(datetime.datetime.now().hour))
            d = d.replace("%m", str(datetime.datetime.now().minute))
            d = d.replace("%s", str(datetime.datetime.now().second))
            d = d.replace("%z", str(datetime.datetime.now().microsecond))
            
            ret = {"type": "str", "value": d}
    
    elif func == "unixtime":
        if len(args) > 0:
            error.error("Invalid number of arguments", "unixtime -> float")
        ret = {"type": "float", "value": str(time.time())}

    
    
    elif func == "round":
        if len(args) != 2:
            error.error("Invalid number of arguments", "round <float> <int> -> float/int")
            
        if args[0]["type"] != "float":
            error.error("Invalid type", "got "+args[0]["type"]+" but expected <float>")
        if args[1]["type"] != "int":
            error.error("Invalid type", "got "+args[1]["type"]+" but expected <int>")
        
        
        if args[1]["value"] == "0":
            ret = {"type": "int", "value": str(round(int(args[0]["value"])))}
        else:
            ret = {"type": "float", "value": str(round(int(args[0]["value"]),int(args[1]["value"])))}

        # Return none
    else:
        ret = False
    
    return ret


def getValue(v):
    """
    If <v> is a variable, get the value of this variable
    and return it, if not, return <v> itself
    
    Input   Output
    5       5
    true    true
    "hi"    "hi"
    x       (value of x)
    """
    
    if v["type"] == "var":
        if v["value"] in var:
            return var[v["value"]]
        else:
            error.error("Undefined variable", v["value"])
    else:
        return v

def parser(line, ln):
    blockInfo = [None, None, None]  # ["if"/"while"/..., BeginLN, EndLN]

    if line == []:
        return
    
    if line[-1] == {"type": "symbol", "value": "{"}:
        """
        This code finds the corresponding } for any if, while or for statement
        
        """
        blockInfo[0] = line[0]["value"]  # ["if"/"while"/..., BeginLN, EndLN]
        blockInfo[1] = ln
        
        INDENT = 1
        codeBlock = []
        for _ln, _line in enumerate(code[blockInfo[1]:]):
            #cprint(_line, "cyan")
            # Go through every line and see if } is the right bracket
            _line = lexer(_line, error)
            if _line == []:
                continue
            
            if _line[-1] == {"type": "symbol", "value": "{"}:
                INDENT += 1

            if _line == [{"type": "symbol", "value": "}"}]:
                INDENT -= 1
                if INDENT == 1:
                    blockInfo[2] = ln + _ln
                    # Right bracket found!
                    break

            # Add lines between { and } to code it should run
            codeBlock.append(_line)
        
        if blockInfo[0] == "while":
            runWhile = cond.checkCondition(codeBlock[0][1:-1])
            while runWhile:
                """
                print("RUN WHILE")
                while 5 > 2 { ... }
                      ^^^^^
                Checking this condition.
                Run through every line but without
                first line, because its the condition
                """
                for _ln, line in enumerate(codeBlock[1:]):
                    ret = parser(line, _ln + blockInfo[1] + 1)
                    if ret == False:
                        return blockInfo[2]
                    elif type(ret) == int:
                        return ret - 1
                    
                runWhile = cond.checkCondition(codeBlock[0][1:-1])
                
            return blockInfo[2]
            

        elif blockInfo[0] == "for":
            v = codeBlock[0][1]["value"]
            # for i in 10 {...}
            #     ^
            # Get this variable.
            
            for forCount in range(int(codeBlock[0][-2]["value"]) - 1):
                # Increment variable
                var[v] = {"type": "int", "value": str(forCount)}
                cbcond = codeBlock[0]
                
                for _ln, line in enumerate(codeBlock[1:]):
                    ret = parser(line, _ln + blockInfo[1] + 1)
                    if ret == False:
                        # Break
                        return blockInfo[2]
                    
                    elif type(ret) == int:
                        return ret
                    
        elif blockInfo[0] == "if":
            runIf = cond.checkCondition(codeBlock[0][1:-1])
            if runIf:
                # if 5 > 2 { ... }
                #    ^^^^^
                # Checking this condition.
                # Run through every line but without
                # first line, because its the condition
                for _ln, line in enumerate(codeBlock[1:]):
                    ret = parser(line, _ln + blockInfo[1] + 2)
                    if ret == False:
                        return blockInfo[2]
                    
                runWhile = cond.checkCondition(codeBlock[0][1:-1])
            else:
                pass # FALSE
            return blockInfo[2] - 1
    
    elif line == [{"type": "symbol", "value": "}"}]:
        pass  # return

    elif line[0] == {"type": "var", "value": "break"}:
        # Exit while and for loops as well as if statements
        return False
    
    # Define variable
    elif line[1] == {"type": "symbol", "value": "="}:
        if line[0]["type"] == "var":
            if line[2]["type"] == "var":
                ret = processFunc(line[2:])
                if ret == False:
                    var[line[0]["value"]] = getValue(line[2])
                else:
                    var[line[0]["value"]] = ret
                
            else:
                var[line[0]["value"]] = getValue(line[2])
        else:
            # Variable name is something like an integer or a string, which
            # doesn't make sense: "hi" = 42   /   5 = "Chi is cool!"
            error.error("Cant assing to " + str(line[0]["type"]), line[0]["value"])

    # a++
    elif line[1] == {"type": "symbol", "value": "+"} and line[2] == {"type": "symbol", "value": "+"}:
        if line[0]["type"] == "var":
            # Check if its an integer
            if var[line[0]["value"]]["type"] == "int":
                var[line[0]["value"]]["value"] = str(int(var[line[0]["value"]]["value"]) + 1)
            else:
                error.error("Can only increment integer", line[0]["value"] + " ("+var[line[0]["value"]]["type"]+")")
    
    # a--
    elif line[1] == {"type": "symbol", "value": "-"} and line[2] == {"type": "symbol", "value": "-"}:
        if line[0]["type"] == "var":
            # Check if its an integer
            if var[line[0]["value"]]["type"] == "int":
                var[line[0]["value"]]["value"] = str(int(var[line[0]["value"]]["value"]) - 1)
            else:
                error.error("Can only decrement integer", line[0]["value"] + " ("+var[line[0]["value"]]["type"]+")")
    
    
    
    elif line[0] == {"type": "var", "value": "use"}:
        error.error("This feature will not work until a future version", "use")
        """
        modules = []
        for c, a in enumerate(line[1:]):
            if c % 2 == 0 and a != {"type": "symbol", "value": ","}:
                if a["type"] != "var":
                    error.error("Invalid syntax", a["value"] + " ("+a["type"]+")")
                
                modules.append(a["value"])

            elif c % 2 == 0 and a == {"type": "symbol", "value": ","}:
                error.error("Invalid syntax", "Non-comma expected")

            elif c % 2 == 1 and a != {"type": "symbol", "value": ","}:
                error.error("Invalid syntax", "comma expected")

            elif c % 2 == 1 and a == {"type": "symbol", "value": ","}:
                pass
        
        for module in modules:
            for file in glob(lib + module + os.sep + "*"):
                ending = file.rsplit(".", 1)[-1]
                if ending == "py":
                    pass
                elif ending == "chi":
                    pass

        """

    else:
        # Run function, that doesn't save its return value into a variable
        if line[0]["type"] == "var":
            processFunc(line)
                
                
                

"""
##################################################
##### PARSE CODE
##################################################
"""

error.setFile(filename)
cond = Cond(error, var)

ln = 0
while ln != len(code):
    error.setLineNumber(ln + 1)
    line = code[ln]
    new_ln = parser(lexer(line, error), ln)
    if type(new_ln) == int:
        ln = new_ln

    ln += 1

"""
##################################################
##### DEBUGGING
##################################################
"""

if "--show-vars" in sys.argv:
    print(var)
