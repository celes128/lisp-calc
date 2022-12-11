import unittest
from interpreter import Interpreter
from constant_pool import ConstantPool

class TestStack(unittest.TestCase):

    def test_PrintHelloWorld(self):
        # The message to print
        msg = "Hello world!"

        # Constant pool with the Hello world string
        cstpool = ConstantPool()
        cstpool.push(msg)
        code = [
            ["sconst", 0],
            ["print", 1],
            ["halt"]
        ]
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
            cstpool.push(msg)
        code = [
            ["sconst", 1],
            ["sconst", 0],
            ["print", 2],
            ["halt"]
        ]
        globals = []
        interp = Interpreter(cstpool, code, globals)
        
        interp.run()

        self.assertEqual(interp.output, messages[0] + " " + messages[1] + "\n")

if __name__ == "__main__":
    unittest.main()