from ASTNodes import *


class CodeGenerator:
    def __init__(self, ast_root, out_file):
        self.ast_root = ast_root
        self.out_file = out_file

    def _traverse(self, node):
        if isinstance(node, Program):
            self._traverse(node.functionn)
        elif isinstance(node, Function):
            self._generate_function_asm(node.name)
            self._traverse(node.statement)
        elif isinstance(node, Return):
            self._traverse(node.val)
            print("\tret", file=self.out_file)
        elif isinstance(node, Expression):
            self._traverse(node.expr)
        elif isinstance(node, UnaryOperator):
            self._traverse(node.expr)
            self._generate_unary_op_asm(node.name)
        elif isinstance(node, Constant):
            self._generate_const_asm(node.integer)

    def generate_code(self):
        self._traverse(self.ast_root)

    def _generate_function_asm(self, name):
        print(f"\t.globl {name}", file=self.out_file)
        print(f"{name}:", file=self.out_file)

    def _generate_const_asm(self, val):
        print(f"\tmovl ${val}, %eax", file=self.out_file)

    def _generate_unary_op_asm(self, operator_name):
        if operator_name == "Negation":
            print(f"\tneg %eax", file=self.out_file)
        elif operator_name == "Bitwise complement":
            print(f"\tnot %eax", file=self.out_file)
        else:  # Logical Negation
            print(f"\tcmpl $0, %eax", file=self.out_file)  # comparing eax with 0, this will set zero-flag(ZF) in flag register to 1 is eax == 0
            print(f"\tmovl $0, %eax", file=self.out_file)  # set eax to 0 means all bytes of eax is set to 0
            print(f"\tsete %al", file=self.out_file)  # al is lower byte of eax so we set it to the value of ZF through 'sete' instruction
