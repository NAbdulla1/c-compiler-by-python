import re

from constants import token_patterns
from tkon import Token


class Lexer:
    def __init__(self, source_code):
        self.src_code = source_code
        self.line = 1
        self.tokens = []
        self.next_token_index = 0
        # generate all tokens
        # print(self.src_code)
        while len(self.src_code) != 0:
            token_found = False
            for name, pat in token_patterns:
                # print("\t",name)
                m = re.match(pat, self.src_code)
                if m:
                    length = m.span()[1] - m.span()[0]

                    t = Token(name, self.src_code[:length].strip(), self.line)
                    self.src_code = self.src_code[length:]
                    if "\n" in t.value:
                        self.line += 1
                    # print(t)
                    if t.name == "white space":
                        token_found = True
                        continue
                    self.tokens.append(t)
                    token_found = True
                    break
            if not token_found:
                print("error occurred while lexing.")
                print("still remaining")
                print(self.src_code)
                print("exiting...")
                exit(1)
        self.tokens.append(None)  # to be compatible with previous codes

    def get_next_token(self):
        tok = self.tokens[self.next_token_index]
        self.next_token_index += 1
        return tok

    def peek_next_token(self):
        while self.tokens[self.next_token_index].name == "white space":
            self.next_token_index += 1
        return self.tokens[self.next_token_index]

    def print_all_tokens(self):
        tok = self.get_next_token()
        while tok is not None:
            print(tok)
            tok = self.get_next_token()
        exit(0)
