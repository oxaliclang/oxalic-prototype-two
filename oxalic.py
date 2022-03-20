import sys
import os

from pyrfc3339 import generate
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

class Parser():
    # Okay not a "parser" of sorts but eh it works
    def parse(tokens):
        # Combine strings
        string_parser = list()
        combine_strings = str()
        enable_combine_strings = False
        for i in tokens:
            if enable_combine_strings:
                if i[1] == "\"":
                    enable_combine_strings = False
                    combine_strings += i[1]
                    string_parser.append(combine_strings)
                    combine_strings = str()
                else:
                    combine_strings += i[1]
            else:
                if i[1] == "\"":
                    enable_combine_strings = True
                    combine_strings += i[1]
                else:
                    string_parser.append(i[1])
        operational_parser = list()
        check_double_operator = str()
        for i in string_parser:
            if i == "":
                pass
            elif not check_double_operator:
                check_double_operator += i
            else:
                check_double_operator += i
                if check_double_operator in functional_operators:
                    operational_parser.append(check_double_operator)
                    string_parser[string_parser.index(i)+1] = ""
                    i = ""
                else:
                    operational_parser.append(string_parser[string_parser.index(i)-1])
                    operational_parser.append(i)
                    check_double_operator = str()

        return operational_parser

class Generator():
    def assembly(orig, filename):
        base_assembly = ["global _start", "section .text", "_start:"]
        data_assembly = ["section .rodata"]
        oxa_base_assembly  = list()
        oxa_data_assembly  = list()
        cleanup = list()
        for i in orig:
            if i == "":
                pass
            else:
                cleanup.append(i)
        orig = cleanup
        line_counter = 1
        for i in orig:
            if i == ">>":
                oxa_base_assembly.append("\tmov rax, 1")
                oxa_base_assembly.append("\tmov rdi, 1")
                oxa_base_assembly.append("\tmov rsi, msg" + str(line_counter))
                oxa_base_assembly.append("\tmov rdx, msglen" + str(line_counter))
                oxa_data_assembly.append("\tmsg" + str(line_counter) +": db " + str(orig[orig.index(i)+2] + ", 10"))
                oxa_data_assembly.append("\tmsglen" + str(line_counter) + ": equ $ - msg" + str(line_counter))
            elif i == ";":
                oxa_base_assembly.append("\tsyscall")
                line_counter += 1

        for i in oxa_base_assembly:
            base_assembly.append(i)
        for i in oxa_data_assembly:
            data_assembly.append(i)

        base_assembly.append("\tmov rax, 60")
        base_assembly.append("\tmov rdi, 0")
        base_assembly.append("\tsyscall")

        assembly = list()
        for i in base_assembly:
            assembly.append(i + "\n")
        for i in data_assembly:
            assembly.append(i + "\n")

        print(assembly)

        with open(filename[:-4]+".asm","w") as asm:
            asm.writelines(assembly)
            asm.close()

        os.system("nasm -f elf64 -o " + filename[:-4] + ".o " + filename[:-4]+".asm")
        os.system("ld " + filename[:-4]+".o -o" + filename[:-4])
        os.system("rm -f " + filename[:-4]+".o")
        os.system("rm -f " + filename[:-4]+".asm")

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
            parsed = Parser.parse(tokens)
            Generator.assembly(parsed, filename_argument)
        else:
            Errors.usageError()

if len(sys.argv) == 2:
    Main.start(sys.argv[1])
else:
    Errors.usageError()