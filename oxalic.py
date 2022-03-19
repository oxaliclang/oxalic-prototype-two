import sys

class Errors():
    def usageError():
        print("Usage: oxalic <file_name>.oxa")

class Lexer():
    def token(file):
        file = [i for i in file]
        print(file)

class Main():
    def start(filename_argument):
        file = str()
        if filename_argument.endswith(".oxa"):
            with open(filename_argument, "r") as oxa:
                for line in oxa:
                    if line.endswith("\n"):
                        line = line[:-1]
                    file += line
            tokens = Lexer.token(file)
        else:
            Errors.usageError()

if len(sys.argv) == 2:
    Main.start(sys.argv[1])
else:
    Errors.usageError()