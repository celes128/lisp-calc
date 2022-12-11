import unittest
from interpreter import Interpreter
from constant_pool import ConstantPool
import objects

# Utility functions
def assemble(s: str):
    """assemble parses a source code string and generate a list of instructions."""
    code = []
    for line in s.splitlines():
        # Instruction
        ins = line.split()
        if len(ins) > 0:
            # Convert the integers to strings
            for i in range(len(ins)):
                if ins[i].isdigit():
                    ins[i] = int(ins[i])
            
            code.append(ins)
    return code
    
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
        code = assemble(source)
        globals = []
        interp = Interpreter(cstpool, code, globals)
        
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
        code = assemble(source)
        globals = []
        interp = Interpreter(cstpool, code, globals)
        
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
        code = assemble(source)
        globals = [["x", objects.Number(0)]]
        interp = Interpreter(cstpool, code, globals)
        
        interp.run()

        self.assertEqual(interp.output, "30" + "\n")

if __name__ == "__main__":
    unittest.main()