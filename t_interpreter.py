import unittest
from interpreter import Interpreter
from constant_pool import ConstantPool
from func_desc import FunctionDescriptor
import objects

# -------------------
#  Utility functions
# -------------------
def assemble(s: str):
    """assemble parses a source code string and generate a list of instructions."""
    # Each instruction is a list usually of length 1 or 2.
    # Example:
    #   ["halt"]        (halt program execution)
    #   ["sconst", 0]   (push the string constant found at index 0 in the constant pool)
    #
    # The bytecode (or simply code) is a list of instructions.
    bytecode = []
    for line in s.splitlines():
        # Instruction
        ins = line.split()
        # Convert tokens that are integers from str to int
        convert_integer_tokens(ins)
        # Push the instruction
        if len(ins) > 0:# ignore blank lines
            bytecode.append(ins)

    return bytecode

def convert_integer_tokens(ins):
    for i in range(len(ins)):
        if ins[i].isdigit():
            ins[i] = int(ins[i])
    
class TestStack(unittest.TestCase):

    def test_PrintHelloWorld(self):
        # The message to print
        msg = "Hello world!"

        # Constant pool with the Hello world string
        cstpool = ConstantPool()
        cstpool.push(objects.String(msg))
        source = """
            sconst 0
            print 1
            halt
        """
        bytecode = assemble(source)
        globals = []
        interp = Interpreter(cstpool, bytecode, globals)
        
        interp.run()

        self.assertEqual(interp.output, msg + "\n")

    def test_PrintHelloWorld2(self):
        # The messages to print
        messages = ["Hello", "world!"]

        # Constant pool with the Hello world string
        cstpool = ConstantPool()
        for msg in messages:
            cstpool.push(objects.String(msg))
        source = """
            sconst 1
            sconst 0
            print 2
            halt
        """
        bytecode = assemble(source)
        globals = []
        interp = Interpreter(cstpool, bytecode, globals)
        
        interp.run()

        self.assertEqual(interp.output, messages[0] + " " + messages[1] + "\n")

    def test_Addition(self):
        cstpool = ConstantPool()
        source = """
            nconst 10
            nconst 20
            add
            gstore 0
            gload 0
            print 1
            halt
        """
        bytecode = assemble(source)
        globals = [["x", objects.Number(0)]]
        interp = Interpreter(cstpool, bytecode, globals)
        
        interp.run()

        self.assertEqual(interp.output, "30" + "\n")

    def test_Function1(self):
        cstpool = ConstantPool()
        # Create a function decsriptor for f (defined below in the source code)
        # Its address is 7 in the bytecode list because it starts at line 7 in the low-level source
        # and hence is at index 7 in the bytecode list.
        fd = FunctionDescriptor("f", 2, 0, 7)
        cstpool.push(fd)

        # ------------------------
        #  High-level source code
        # ------------------------
        #   def f(a, b) { return a+b; }
        #   x = f(10, 20)
        #   print(x)
        # -----------------------
        #  Low-level source code
        # -----------------------
        source = """
            nconst 20
            nconst 10
            call 0
            gstore 0
            gload 0
            print 1
            halt
            load 0
            load 1
            add
            ret
        """
        # Bytecode (list of instructions)
        bytecode = assemble(source)
        globals = [["x", objects.Number(0)]]
        interp = Interpreter(cstpool, bytecode, globals)
        
        interp.run()

        self.assertEqual(interp.output, "30" + "\n")
if __name__ == "__main__":
    unittest.main()