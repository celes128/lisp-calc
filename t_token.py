import unittest
import lex

class TestToken(unittest.TestCase):

    def test_TokenCtor(self):
        # Test case: [token type, token value]
        tests = [
            ["(", 0],
            [")", 0],
            ["+", 0],
            ["-", 0],
            ["*", 0],
            ["/", 0],
            ["num", 10.0],
        ]

        for t in tests:
            tok = lex.Token(t[0], t[1])
            self.assertEqual(tok.type, t[0])
            self.assertEqual(tok.value, t[1])

if __name__ == '__main__':
    unittest.main()