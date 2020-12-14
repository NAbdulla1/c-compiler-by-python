class Constant:
    def __init__(self, val):
        self.integer = val


class UnaryOperator:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class Return:
    def __init__(self, expr):
        self.val = expr


class Expression:
    def __init__(self, expr):
        self.expr = expr


class Function:
    def __init__(self, identifier, statement):
        self.name = identifier
        self.statement = statement


class Program:
    def __init__(self, functionn):
        self.functionn = functionn
