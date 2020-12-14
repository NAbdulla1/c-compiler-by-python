# BNF grammar:
# terminals are denoted by quotes and non-terminals are denoted by without quotes
# program = function
# function = "Int keyword" "Identifier" "Open parenthesis" "Close parenthesis" "Open brace" statement "Close brace"
# statement = "Return keyword" expression "Semicolon"
# [we don't use this because of left recursion] expression = expression ("Addition" | "SUBTRACTION") expression | term
# [we don't use this because of left recursion] term = term ("Multiplication" | "Division") term | factor
# expression = term { ("Addition" | "SUBTRACTION") term }  # {} means repetition, we use this instead of rule at line:6
# term = factor { ("Multiplication" | "Division") factor }  # {} means repetition, we use this instead of rule at line:7
# factor = "Open parenthesis" expression "Close parenthesis" | unary_op factor | "Integer literal"
# unary_op = "Negation" | "Bitwise complement" | "Logical negation"

import sys

from ASTNodes import *
from constants import unary_operators


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.last_line = 0

    def parse_program(self):
        func = self.parse_function()
        return Program(func)

    def parse_function(self):
        tok = self.next_token()
        if tok.name != "Int keyword":
            self.fail(tok.lineNo)

        tok = self.next_token()
        if tok.name != "Identifier":
            self.fail(tok.lineNo)

        name = tok.value  # function name

        tok = self.next_token()
        if tok.name != "Open parenthesis":
            self.fail(tok.lineNo)

        tok = self.next_token()
        if tok.name != "Close parenthesis":
            self.fail(tok.lineNo)

        tok = self.next_token()
        if tok.name != "Open brace":
            self.fail(tok.lineNo)

        statement = self.parse_statement()

        tok = self.next_token()
        if tok.name != "Close brace":
            self.fail(tok.lineNo)

        return Function(name, statement)

    def parse_statement(self):
        tok = self.next_token()
        if tok.name != "Return keyword":
            self.fail(tok.lineNo)

        const = self.parse_expression()

        tok = self.next_token()
        if tok.name != "Semicolon":
            self.fail(tok.lineNo)

        return Return(const)

    def parse_expression(self):
        term1 = self.parse_term()
        nxt = self.lexer.peek_next_token()
        while nxt.name == "Addition" or nxt.name == "Negation":
            binary_op = self.next_token()
            term2 = self.parse_term()
            term1 = BinaryOp(binary_op.name, term1, term2)
            nxt = self.lexer.peek_next_token()
        return term1

    def parse_term(self):
        factor1 = self.parse_factor()
        nxt = self.lexer.peek_next_token()
        while nxt.name == "Multiplication" or nxt.name == "Division":
            binary_op = self.next_token()
            factor2 = self.parse_factor()
            factor1 = BinaryOp(binary_op.name, factor1, factor2)
            nxt = self.lexer.peek_next_token()
        return factor1

    def parse_factor(self):
        tok = self.next_token()
        if tok.name == "Integer literal":
            try:
                val = int(tok.value)
            except:
                self.fail(tok.lineNo)
            return Expression(Constant(val))
        elif tok.name in unary_operators:
            operator = tok.name
            sub_expr = self.parse_factor()
            return UnaryOperator(operator, sub_expr)
        elif tok.name == "Open parenthesis":
            expr = self.parse_expression()
            tk = self.next_token()
            if tk.name != "Close parenthesis":
                self.fail(tk.lineNo)
            return expr
        else:
            self.fail(tok.lineNo)

    def fail(self, line_no):
        print("Syntax error on line:", line_no, file=sys.stderr)
        exit(1)

    def next_token(self):
        tok = self.lexer.get_next_token()
        if tok is not None:
            self.last_line = tok.lineNo
        if tok is None:
            self.fail(self.last_line)
        return tok
