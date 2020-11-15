import string

quotes = ["\"", "'"]

def lexer(line, stderr):
    line += " none"
    e = ""
    lexed = []
    inWord = False
    inNumber = False
    for letter in line:
        if letter in quotes:
            if inWord:
                inWord = False
                lexed.append({"value":e[1:], "type":"str"})
                e = ""
            else:
                inWord = True

        if inWord:
            e += letter
        else:

            if letter in "0123456789.":
                inNumber = True
                e += letter
            else:
                if inNumber:
                    inNumber = False
                    isVar = False
                    for l in e:
                        if l in string.ascii_letters + ":":
                            isVar = True


                    if isVar:
                        lexed.append({"value": e, "type": "var"})
                    else:
                        ec = e.count(".")
                        if ec == 0:
                            lexed.append({"value": e, "type": "int"})
                        elif ec == 1:
                            lexed.append({"value": e, "type": "float"})
                        else:
                            stderr.error("Invalid float", e)
                        e = ""
                    lexed.append({"value": letter, "type": "symbol"})

                else:
                    if letter == "@":
                	    break
                    if not letter in string.ascii_letters + "_:":
                        if e == "true" or e == "false":
                            lexed.append({"value":e, "type":"bool"})
                        else:
                            lexed.append({"value":e, "type":"var"})
                            
                        if not letter in quotes:
                            lexed.append({"value":letter, "type":"symbol"})
                        e = ""
                    else:
                        e += letter

    _lexed = lexed
    lexed = []

    for e in _lexed:
        if e["value"].strip() == "" and e["type"] != "str":
            continue

        lexed.append(e)

    return lexed
