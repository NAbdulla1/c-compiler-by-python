# BNF grammar:
# program = function
# function = "Int keyword" "Identifier" "Open parenthesis" "Close parenthesis" "Open brace" statement "Close brace"
# statement = "Return keyword" expression "Semicolon"
# expression = "Integer literal"

import sys

from ASTNodes import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.last_line = 0

    def parse_program(self):
        func = self.parse_function()
        return Program(func)

    def parse_function(self):
        tok = self.next_token(False)
        if tok.name != "Int keyword":
            self.fail(tok.lineNo)

        tok = self.next_token(True)
        if tok.name != "Identifier":
            self.fail(tok.lineNo)

        name = tok.value  # function name

        tok = self.next_token(False)
        if tok.name != "Open parenthesis":
            self.fail(tok.lineNo)

        tok = self.next_token(False)
        if tok.name != "Close parenthesis":
            self.fail(tok.lineNo)

        tok = self.next_token(False)
        if tok.name != "Open brace":
            self.fail(tok.lineNo)

        statement = self.parse_statement()

        tok = self.next_token(False)
        if tok.name != "Close brace":
            self.fail(tok.lineNo)

        return Function(name, statement)

    def parse_statement(self):
        tok = self.next_token(False)
        if tok.name != "Return keyword":
            self.fail(tok.lineNo)

        const = self.parse_expression()

        tok = self.next_token(False)
        if tok.name != "Semicolon":
            self.fail(tok.lineNo)

        return Return(const)

    def parse_expression(self):
        tok = self.next_token(True)
        if tok.name != "Integer literal":
            self.fail(tok.lineNo)
        try:
            val = int(tok.value)
        except:
            self.fail(tok.lineNo)
        return Constant(val)

    def fail(self, line_no):
        print("Syntax error on line:", line_no, file=sys.stderr)
        exit(1)

    def next_token(self, whitespace_required_before):
        tok = self.lexer.get_next_token()
        if tok is not None:
            self.last_line = tok.lineNo
        has_whitespace = False
        while tok is not None and tok.name == "white space":
            tok = self.lexer.get_next_token()
            has_whitespace = has_whitespace or True
            if tok is not None:
                self.last_line = tok.lineNo
        if tok is None:
            self.fail(self.last_line)
        if whitespace_required_before and not has_whitespace:
            self.fail(tok.lineNo)
        return tok
