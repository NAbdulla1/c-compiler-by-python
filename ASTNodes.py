class Constant:
    def __init__(self, val):
        self.integer = val


class Return:
    def __init__(self, constant):
        self.val = constant


class Function:
    def __init__(self, identifier, statement):
        self.name = identifier
        self.statement = statement


class Program:
    def __init__(self, functionn):
        self.functionn = functionn
