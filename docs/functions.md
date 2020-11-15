You can execute a function like this:  
```
function arg1, arg2, ...
```  

function            Name of the function  
<arg>               required argument  
(arg)               Optional argument  
(arg) (arg) ...     Infinite arguments  
<arg> (arg) ...     Infinite arguments, but 1 required  
arg/type            Argument of specific type  
text/*              Argument of any type  
-> type             Return type  


out (text/str) (text/str) ... -> none  
    Prints text to the console. Every argument will be printed, seperated by a space.  

put (text/str) (text/str) ... -> none  
    Prints text to the console. Every argument will be printed directly behind each other  

in (text/str) -> str  
    Takes an input from the user  

use <module/str> -> none  
    Imports a module. Imported functions will act like normal ones.  
    If you import "myModule", it will automatically search the "/my/path/Chi/lib/myModule"  
    directory for any other directory or .chi file. You can call myFunction from myModule  
    like this:  
    ```
    myModule:myFunction
    ```  
    If there are any submodules, you can call functions like this:  
    ```
    myModule:mySub:myOtherFunction
    ```  

add <number/int,float> (number/int,float) ... -> float,int  
    Adds two or more numbers together  
    If any of the numbers is a float, the return value will also be a float.  

concat <text/*> <text/*> (text/*) -> str  
    Concatenates two or more strings  

conv <var/*> <type/str> -> ?  
    Converts a variable to a specific type. Returns the converted variable  

type <var/*> -> str  
    Returns the type of a variable  

len <text/str> -> int  
    Returns the length of a string  

shell <command/str> -> str  
    Runs a command in the shell and returns the output  

writefile <filename/str> <content/str> -> none  
    Writes content to a file  

appendfile <filename/str> <content/str> -> none  
    Appends content to the end of a file  

readfile <filename/str> -> str  
    Reads and returns the content of a file  

clearfile <filename/str> -> none  
    Clears a file  
