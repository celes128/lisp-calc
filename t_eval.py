import unittest
from lex import Token
from lex import TokenStream
from eval import Environment
import eval

class TestEvalRest(unittest.TestCase):

    def test_plus_1(self):
        env = Environment()

        tokens = [
            Token("("),
            Token("+"),
            Token("num", 1),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens), env)

        self.assertEqual(result, 1)

    def test_plus_2(self):
        env = Environment()
        
        tokens = [
            Token("("),
            Token("+"),
            Token("num", 1),
            Token("num", 2),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens), env)

        self.assertEqual(result, 3)

    def test_plus_zero_arg(self):
        env = Environment()

        tokens = [
            Token("("),
            Token("+"),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens), env)

        self.assertEqual(result, 0)

    def test_mult_1(self):
        env = Environment()
        
        tokens = [
            Token("("),
            Token("*"),
            Token("num", 1),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens), env)

        self.assertEqual(result, 1)

    def test_mult_2(self):
        env = Environment()
        
        tokens = [
            Token("("),
            Token("*"),
            Token("num", 2),
            Token("num", 3),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens), env)

        self.assertEqual(result, 6)

    def test_mult_zero_arg(self):
        env = Environment()
        
        tokens = [
            Token("("),
            Token("*"),
            Token(")")
        ]
        result = eval.eval_token_list(TokenStream(tokens), env)

        self.assertEqual(result, 1)

class TestEvalIf(unittest.TestCase):

    def test_if_true(self):
        env = Environment()
        
        tokens = [
            Token("("),
            Token("if"),
            Token("num", 1),
            Token("num", 2),
            Token(")"),
            ]
        result = eval.eval_if(TokenStream(tokens), env)

        self.assertEqual(result, 2)

    def test_if_false_no_else_clause(self):
        env = Environment()
        
        tokens = [
            Token("("),
            Token("if"),
            Token("num", 0),
            Token("num", 1),
            Token(")"),
            ]
        result = eval.eval_if(TokenStream(tokens), env)

        self.assertEqual(result, None)

    def test_if_false_with_an_else_clause(self):
        env = Environment()
        
        tokens = [
            Token("("),
            Token("if"),
            Token("num", 0),
            Token("num", 1),
            Token("num", 2),
            Token(")"),
            ]
        result = eval.eval_if(TokenStream(tokens), env)

        self.assertEqual(result, 2)

class TestEvalSetq(unittest.TestCase):

    def test_1(self):
        env = Environment()
        tokens = [
            Token("("),
            Token("setq"),
            Token("id", "x"),
            Token("num", 5),
            Token(")"),
            ]
        result = eval.eval_setq(TokenStream(tokens), env)

        self.assertEqual(result, 5)
        self.assertTrue(env.contains("x", 5))

if __name__ == "__main__":
    unittest.main()