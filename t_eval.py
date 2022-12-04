import unittest
from lex import Token
from lex import TokenStream
import eval

class TestEvalRest(unittest.TestCase):

    def test_plus_1(self):
        tokens = [
            Token("("),
            Token("+"),
            Token("num", 1),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens))

        self.assertEqual(result, 1)

    def test_plus_2(self):
        tokens = [
            Token("("),
            Token("+"),
            Token("num", 1),
            Token("num", 2),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens))

        self.assertEqual(result, 3)

    def test_plus_zero_arg(self):
        tokens = [
            Token("("),
            Token("+"),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens))

        self.assertEqual(result, 0)

    def test_mult_1(self):
        tokens = [
            Token("("),
            Token("*"),
            Token("num", 1),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens))

        self.assertEqual(result, 1)

    def test_mult_2(self):
        tokens = [
            Token("("),
            Token("*"),
            Token("num", 2),
            Token("num", 3),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens))

        self.assertEqual(result, 6)

    def test_mult_zero_arg(self):
        tokens = [
            Token("("),
            Token("*"),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens))

        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()