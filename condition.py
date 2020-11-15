class Cond:
    def __init__(self, error, var):
        self.error = error
        self.var = var
    
    def getValue(self, v):
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
            if v["value"] in self.var:
                return self.var[v["value"]]
            else:
                self.error.error("Undefined variable", v["value"])
        else:
            return v


    
    def checkVarBool(self, v):
        """
        Check boolean value from a single variable (<v>):
            Input   Output
            -----------------
            true    True
            false   False
            5       True
            1       True
            0       False
            0.1     True
            
        
        """
        # If Input is a variable, get variables
        v = self.getValue(v)
        
        # Define value and type of variable
        vv = v["value"]
        vt = v["type"]

        if vt == "bool":
            # Input is a boolean
            if vv == "true":
                # if true
                return True
            elif vv == "false":
                # if false
                return False
            
                
        elif vt == "int" or vt == "float":
            # Input is a number
            vv = float(vv)
            if vv != 0:
                return True
            else:
                return False

        else:
            self.error.error("Invalid condition", v)

    def checkCondition(self, cond):
        """
        This function takes a condition, for example
            [
                {"type": "int", "value": "5"},
                {"type": "symbol", "value": ">"},
                {"type": "int", "value": "2"}
            ]
        and returns False or True based on the condition.
        """
        if len(cond) == 1:
            """
            Condition is just a single variable or number
            Examples:
                if true         {...}
                if false        {...}
                if doSomething  {...}
                if 5            {...}
            """
            c = checkVarBool(cond[0])
            return c

        elif len(cond) == 3:
            a, op, b = cond
            a = self.getValue(a)
            b = self.getValue(b)
            ops = [">", "<"]
            if op["type"] == "symbol" or op["value"] in ops:
                if a["type"] != "float" and a["type"] != "int":
                    self.error.error("Can only compare sizes with integers or floats", a["value"] + " ("+a["type"]+")")
                elif b["type"] != "float" and b["type"] != "int":
                    self.error.error("Can only compare sizes with integers or floats", b["value"] + " ("+b["type"]+")")
                
                if op["value"] == ">":
                    if float(a["value"]) > float(b["value"]):
                        return True
                    else:
                        return False
                
                elif op["value"] == "<":
                    if float(a["value"]) < float(b["value"]):
                        return True
                    else:
                        return False
                
            else:
                self.error.error("Invalid operation in condition", op["value"])

        elif len(cond) == 4:
            a, op1, op2, b = cond
            a = self.getValue(a)
            b = self.getValue(b)
            
            ops = [">=", "<=", "!=", "=="]
            op = {"type": "symbol", "value": op1["value"] + op2["value"]}
            if op["type"] == "symbol" or op["value"] in ops:
                if op["value"] == "==":
                    if a == b:
                        return True
                    else:
                        return False

                elif op["value"] == "!=":
                    if a != b:
                        return True
                    else:
                        return False
                
                else:
                    if a["type"] != "float" and a["type"] != "int":
                        self.error.error("Can only compare sizes with integers or floats", a["value"] + " ("+a["type"]+")")
                    elif b["type"] != "flofat" and b["type"] != "int":
                        self.error.error("Can only compare sizes with integers or floats", b["value"] + " ("+b["type"]+")")
                    
                    if op["value"] == ">=":
                        if float(a["value"]) >= float(b["value"]):
                            return True
                        else:
                            return False

                    elif op["value"] == "<=":
                        if float(a["value"]) <= float(b["value"]):
                            return True
                        else:
                            return False
                    
                
                
            else:
                self.error.error("Invalid operation in condition", op["value"])
