from stack import Stack

class Interpreter():

    HALT = 0
    CONTINUE = 1

    def __init__(self, cstpool, code, globals):
        self._cstpool = cstpool
        self._code = code
        self._globals = globals
        # Stack frame
        self._calls = Stack()
        # Operands stacks
        self._operands = Stack()
        # Instruction pointer
        self._ip = 0
        # Load the instruction dictionary
        self._instructions = {
            "halt":self._ins_halt,
            "sconst":self._ins_sconst,
            "print":self._ins_print,
        }
        self._halt = False
        self.output = ""

    def _ins_halt(self, args):
        self._ip += 1
        self._halt = True
    
    def _ins_sconst(self, args):
        operand = self._cstpool.get(args[0])
        self._operands.push(operand)
        self._ip += 1
        
    def _ins_print(self, args):
        # Number of the actual argument strings to print
        n = args[0]
        # The strings are on the operand stack
        strs = []
        for i in range(n):
            s = self._operands.pop()
            strs.append(s)
        # Print in the output
        self.output += " ".join(strs) + "\n"
        # Point to the next instruction
        self._ip += 1
        
    def run(self):
        self._halt = False
        self.output = ""
        while not self._halt and self._ip < len(self._code):
            ins = self._code[self._ip]
            args = ins[1:]
            self._instructions[ins[0]](args)