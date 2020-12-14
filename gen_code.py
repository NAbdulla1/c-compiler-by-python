class CodeGenerator:
    def __init__(self, ast_root, out_file):
        self.ast_root = ast_root
        self.out_file = out_file

    def _generate_function_asm(self, name):
        print(f"\t.globl {name}", file=self.out_file)
        print(f"{name}:", file=self.out_file)

    def traverse(self, node):
        if "Program" in str(type(node)):
            self.traverse(node.functionn)
        elif "Function" in str(type(node)):
            self._generate_function_asm(node.name)
            self.traverse(node.statement)
        elif "Return" in str(type(node)):
            val = node.val.integer
            print(f"\tmovl ${val}, %eax", file=self.out_file)
            print("\tret", file=self.out_file)

    def generate_code(self):
        self.traverse(self.ast_root)
