from stack import Stack
import objects

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
            "nconst":self._ins_nconst,
            "print":self._ins_print,
            "gstore":self._ins_gstore,
            "gload":self._ins_gload,
            "add":self._ins_add,
        }
        self._halt = False
        self.output = ""

    def _ins_gload(self, args):
        var = self._globals[args[0]]
        value = var[1]
        self._operands.push(value)
        # if type(value) == objects.Number:
        #     self._operands.push(value.value)
        # elif type(value) == objects.String:
        #     self._operands.push(value.s)
        # else:
        #     raise Exception("Error in gload instruction: unknown object type.")

    def _ins_gstore(self, args):
        value = self._operands.pop()
        self._globals[args[0]][1] = value
        
    def _ins_halt(self, args):
        self._halt = True
    
    def _ins_sconst(self, args):
        operand = self._cstpool.get(args[0])
        self._operands.push(operand)
    
    def _ins_nconst(self, args):
        x = args[0]
        self._operands.push(objects.Number(x))

    def _ins_add(self, args):
        right = self._operands.pop()
        left = self._operands.pop()
        if type(right) != objects.Number or type(left) != objects.Number:
            raise Exception("add instruction error: one or both operand is not a number.")
        result = left.value + right.value
        self._operands.push(objects.Number(result))
        
    def _ins_print(self, args):
        # Number of the actual argument strings to print
        n = args[0]
        # The strings are on the operand stack
        strs = []
        for i in range(n):
            s = self._operands.pop()
            strs.append(str(s))
        # Print in the output
        self.output += " ".join(strs) + "\n"
        
    def run(self):
        self._halt = False
        self.output = ""
        while not self._halt and self._ip < len(self._code):
            # Decode instruction and arguments
            ins = self._code[self._ip]
            args = ins[1:]
            # Execute the instruction
            self._instructions[ins[0]](args)
            # Point to the next instruction
            self._ip += 1