import re

from constants import token_patterns
from tkon import Token


class Lexer:
    def __init__(self, source_code):
        self.src_code = source_code
        self.line = 1

    def get_next_token(self):
        # print(self.src_code)
        if len(self.src_code) == 0:
            return None
        for name, pat in token_patterns:
            # print("\t",name)
            m = re.match(pat, self.src_code)
            if m:
                l = m.span()[1] - m.span()[0]

                t = Token(name, self.src_code[:l], self.line)
                self.src_code = self.src_code[l:]
                if "\n" in t.value:
                    self.line += 1
                # print(t)
                return t
        return Token("error", "error", -1)
