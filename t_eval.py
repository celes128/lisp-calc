import unittest
from lex import Token
from lex import TokenStream
import eval

class TestEvalRest(unittest.TestCase):

    def test_1(self):
        # Create the stream of tokens from an expression.
        tokens = [
            Token("("),
            Token("+"),
            Token("num", 1),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens))

        self.assertEqual(result, 1)

if __name__ == "__main__":
    unittest.main()