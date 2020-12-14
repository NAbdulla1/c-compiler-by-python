class Token:
    def __init__(self, name, value, line_no):
        self.name = name
        self.value = value
        self.lineNo = line_no

    def __str__(self):
        val = "new line" if self.value == '\n' else self.value
        return f"name: {self.name}, val: '{val}', lineNo: {self.lineNo}"

    def __all__(self):
        pass
