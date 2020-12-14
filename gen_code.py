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
            self.asm_print(f"\tpopl %eax")
            self.asm_print("\tret")
        elif isinstance(node, Expression):
            self._traverse(node.expr)
        elif isinstance(node, UnaryOperator):
            self._traverse(node.expr)
            self._generate_unary_op_asm(node.name)
        elif isinstance(node, Constant):
            self._generate_const_asm(node.integer)
        elif isinstance(node, BinaryOp):
            self._traverse(node.expr_left)
            self._traverse(node.expr_right)
            self._generate_binary_op_asm(node.name)

    def generate_code(self):
        self._traverse(self.ast_root)

    def _generate_function_asm(self, name):
        self.asm_print(f"\t.globl {name}")
        self.asm_print(f"{name}:")

    def _generate_const_asm(self, val):
        self.asm_print(f"\tpushl ${val}\n")

    def _generate_unary_op_asm(self, operator_name):
        self.asm_print(f"\tpopl %eax")
        if operator_name == "Negation":
            self.asm_print(f"\tneg %eax")
        elif operator_name == "Bitwise complement":
            self.asm_print(f"\tnot %eax")
        else:  # Logical Negation
            self.asm_print(f"\tcmpl $0, %eax")  # this will set zero-flag(ZF) in to 1 if eax == 0
            self.asm_print(f"\tmovl $0, %eax")  # set eax to 0 means all bytes of eax is set to 0
            self.asm_print(f"\tsete %al")  # 'sete' sets al to 1 if ZF is 1
        self.asm_print(f"\tpushl %eax\n")

    def _generate_binary_op_asm(self, operator_name):
        self.asm_print("\tpopl %ecx /* right_operand */")
        self.asm_print("\tpopl %eax /* left_operand */")
        if operator_name == "Addition":
            self.asm_print("\taddl %ecx, %eax")
        elif operator_name == "Negation":
            self.asm_print("\tsubl %ecx, %eax")
        elif operator_name == "Multiplication":
            self.asm_print("\timul %ecx, %eax")
        elif operator_name == "Division":
            self.asm_print("\tcdq")
            self.asm_print("\tidivl %ecx")
        self.asm_print("\tpushl %eax /* push the result in stack */\n")

    def asm_print(self, asm_code):
        print(asm_code, file=self.out_file)
