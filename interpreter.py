from stack import Stack
import objects
from func_desc import FunctionDescriptor

class StackFrame():

    def __init__(self, fd: FunctionDescriptor, ret_addr: int, locals: list):
        # Function descriptor
        self.fd = fd
        # Return address
        self.ret_addr = ret_addr
        # Local variables (function arguments at the front followed by the "real" local variables)
        self.locals = locals
        
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
            "call":self._ins_call,
            "ret":self._ins_ret,
            "load":self._ins_load,
        }
        self._halt = False
        self.output = ""

    def _ins_call(self, args):
        # Compute the arguments for constructing a StackFrame object.

        # Get the function description
        fd = self._cstpool.get(args[0])
        if type(fd) != FunctionDescriptor:
            raise Exception("Instruction call: constant #" + str(args[0]) + " is not a function.")

        # Collect (and remove) the function arguments from the operand stack
        fargs = []
        for i in range(fd.nargs):
            fargs.append(self._operands.pop())

        # Return address
        ret_addr = self._ip + 1

        # Create and push the stack frame
        self._calls.push(StackFrame(fd, ret_addr, fargs))

        # Point to the first instruction of the function
        self._ip = fd.address

    def _ins_ret(self, args):
        frame = self._calls.pop()
        self._ip = frame.ret_addr

    def _ins_load(self, args):
        """
        Instruction: load
        Description: push the local variable from the current stack frame onto the operand stack.
        """
        # Get the local variable's value from the stack frame
        value = self._calls.top().locals[args[0]]
        # Push its value onto the operand stack
        self._operands.push(value)
        # Point to the next instruction
        self._ip += 1

    def _ins_gload(self, args):
        var = self._globals[args[0]]
        value = var[1]
        self._operands.push(value)
        self._ip += 1

    def _ins_gstore(self, args):
        value = self._operands.pop()
        self._globals[args[0]][1] = value
        self._ip += 1
        
    def _ins_halt(self, args):
        self._halt = True
        self._ip += 1
    
    def _ins_sconst(self, args):
        operand = self._cstpool.get(args[0])
        self._operands.push(operand)
        self._ip += 1
    
    def _ins_nconst(self, args):
        x = args[0]
        self._operands.push(objects.Number(x))
        self._ip += 1

    def _ins_add(self, args):
        right = self._operands.pop()
        left = self._operands.pop()
        if type(right) != objects.Number or type(left) != objects.Number:
            raise Exception("add instruction error: one or both operand is not a number.")
        result = left.value + right.value
        self._operands.push(objects.Number(result))
        self._ip += 1
        
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
        self._ip += 1
        
    def run(self):
        self._halt = False
        self.output = ""
        while not self._halt and self._ip < len(self._code):
            # Decode instruction and arguments
            ins = self._code[self._ip]
            args = ins[1:]
            # Execute the instruction
            self._instructions[ins[0]](args)