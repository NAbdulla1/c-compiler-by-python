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
            print(f"\tpopl %eax", file=self.out_file)
            print("\tret", file=self.out_file)
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
        print(f"\t.globl {name}", file=self.out_file)
        print(f"{name}:", file=self.out_file)

    def _generate_const_asm(self, val):
        print(f"\tpushl ${val}\n", file=self.out_file)

    def _generate_unary_op_asm(self, operator_name):
        print(f"\tpopl %eax", file=self.out_file)
        if operator_name == "Negation":
            print(f"\tneg %eax", file=self.out_file)
        elif operator_name == "Bitwise complement":
            print(f"\tnot %eax", file=self.out_file)
        else:  # Logical Negation
            print(f"\tcmpl $0, %eax", file=self.out_file)  # this will set zero-flag(ZF) in to 1 if eax == 0
            print(f"\tmovl $0, %eax", file=self.out_file)  # set eax to 0 means all bytes of eax is set to 0
            print(f"\tsete %al", file=self.out_file)  # 'sete' sets al to 1 if ZF is 1
        print(f"\tpushl %eax\n", file=self.out_file)

    def _generate_binary_op_asm(self, operator_name):
        print("\tpopl %ecx /* right_operand */", file=self.out_file)
        print("\tpopl %eax /* left_operand */", file=self.out_file)
        if operator_name == "Addition":
            print("\taddl %ecx, %eax", file=self.out_file)
        elif operator_name == "Negation":
            print("\tsubl %ecx, %eax", file=self.out_file)
        elif operator_name == "Multiplication":
            print("\timul %ecx, %eax", file=self.out_file)
        elif operator_name == "Division":
            print("\tcdq", file=self.out_file)
            print("\tidivl %ecx", file=self.out_file)
        print("\tpushl %eax /* push the result in stack */\n", file=self.out_file)
