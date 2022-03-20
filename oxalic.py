import sys
functional_operators = [">>", "??", "!?","|?","&","#"]

class Errors():
    def usageError():
        print("Usage: oxalic <file_name>.oxa")

class Lexer():
    def token(file):
        file    = [i for i in file]
        objects = list()
        string  = str()
        for i in file:
            if i.isalnum():
                string += i
            else:
                if not string:
                    objects.append(i)
                else:
                    objects.append(string)
                    objects.append(i)
                    string = str()
        combined_objects = list()
        counter = 0
        for i in objects:
            if i.isalnum():
                combined_objects.append([counter,i])
            else:
                combined_objects.append([counter,i])
            counter += 1
        token_list = list()
        for i in combined_objects:
            if i not in token_list:
                token_list.append(i)
        tokens = list()
        counter = 0 
        for i in token_list:
            if i[1] == "":
                pass
            elif i[1].isalnum():
                counter += 1 
                if any(char.isalpha() for char in i[1]):
                    tokens.append([counter, i[1], "iden"])
                else:
                    tokens.append([counter, i[1], "int"])
            else:
                counter += 1
                tokens.append([counter, i[1], "optr"])
        return tokens
            
            

class Main():
    def start(filename_argument):
        file = str()
        if filename_argument.endswith(".oxa"):
            with open(filename_argument, "r") as oxa:
                for line in oxa:
                    if line.endswith("\n"):
                        line = line[:-1]
                    if line.startswith("#"):
                        line = ""
                    file += line
            tokens = Lexer.token(file)
            print(tokens)
        else:
            Errors.usageError()

if len(sys.argv) == 2:
    Main.start(sys.argv[1])
else:
    Errors.usageError()