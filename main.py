#!/usr/bin/python3
import sys
import os

from lexer import Lexer
from parser import Parser
from gen_code import CodeGenerator

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} c_file.c")
        exit(1)
    try:
        # for path in os.listdir("tests/stage_1/valid"):
        c_file = open(sys.argv[1])
        # c_file = open("tests/stage_1/valid/" + path)
        src_code = c_file.read()
        c_file.close()
        # print(src_code)

        lexer = Lexer(src_code)
        lexer.print_all_tokens()

        parser = Parser(lexer)
        ast_root = parser.parse_program()
        # print("parsing successful")
        # exit(0)

        out = open("assembly.s", "w")  # sys.stdout
        CodeGenerator(ast_root, out).generate_code()
        out.close()
        # print("Code Generated.\nto get executable use this:")
        # print(f"\tgcc -m32 {out.name}")
        # print("then execute by ./a.out")
        # print("to verify the return value run echo $?")
    except Exception as ex:
        print(ex)
