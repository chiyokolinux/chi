import sys
from termcolor import *

class Error:
    def __init__(self, version, file, lineNumber):
        self.version = version
        self.file = file
        self.lineNumber = lineNumber
    
    def setFile(self, file):
        self.file = file
    
    def setLineNumber(self, lineNumber):
        self.lineNumber = lineNumber

    def error(self, text, val):
        text = str(text)
        val = str(val)
        if self.file == None and self.lineNumber == None:
            cprint("\nChi {"+self.version+"} "+str(self.file if self.file != None else "Startup"), "yellow", None, ["bold"])
        else:
            cprint("\nChi {"+self.version+"} <"+str(self.file if self.file != None else "Startup")+"> | Line "+str(self.lineNumber), "yellow", None, ["bold"])
        cprint(text, "red", None, ["bold"])
        cprint("    " + val, "red", None, ["bold"])
        sys.exit()
