#!/usr/bin/env python3
import sys
from termcolor import *

def setFile(_file):
    global file
    file = _file

def setVersion(_version):
    global version
    version = _version

def setLineNumber(_ln):
    global LineNumber
    LineNumber = _ln



def error(text, val):
    cprint("\nChi {"+version+"} <"+str(file)+"> | Line "+str(LineNumber), "yellow", None, ["bold"])
    cprint(text, "red", None, ["bold"])
    cprint("    " + val, "red", None, ["bold"])
    sys.exit()
