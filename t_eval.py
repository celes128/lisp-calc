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

    def test_eval_complex_if_1(self):
        env = Environment()
        # (if 1 (setq x 5) (setq x 10))
        tokens = [
            Token("("),
            Token("if"),

            Token("num", 1),

            Token("("),
            Token("setq"),
            Token("id", "x"),
            Token("x", 5),
            Token(")"),
            
            Token("("),
            Token("setq"),
            Token("id", "x"),
            Token("x", 10),
            Token(")"),

            Token(")"),
            ]
        
        s = TokenStream(tokens)
        
        result = eval.eval_if(s, env)
        
        self.assertTrue(s.eof())
        self.assertTrue(env.contains("x", 5))
        self.assertEqual(result, 5)
        
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

class TestSkipAtom(unittest.TestCase):

    def test_identifier(self):
        tokens = [
            Token("("),
            Token("id", "x"),
            Token("num", 5),
            Token(")"),
            ]
        s = TokenStream(tokens)
        # Point to x
        s.next()

        atom = eval.skip_atom(s)        
        self.assertEqual(atom, Token("id", "x"))
        self.assertEqual(s.get(), Token("num", 5))

    def test_number(self):
        tokens = [
            Token("("),
            Token("id", "x"),
            Token("num", 5),
            Token(")"),
            ]
        s = TokenStream(tokens)
        # Point to 5
        s.next()
        s.next()

        atom = eval.skip_atom(s)        
        self.assertEqual(atom, Token("num", 5))
        self.assertEqual(s.get(), Token(")"))

    def test_not_atom(self):
        tokens = [
            Token("("),
            Token("id", "x"),
            Token(")"),
            ]
        s = TokenStream(tokens)

        self.assertRaises(Exception, eval.skip_atom, s)

class TestSkipList(unittest.TestCase):

    def test_one_empty_list(self):
        tokens = [
            Token("("),
            Token(")"),
            ]
        s = TokenStream(tokens)

        eval.skip_list(s)

        self.assertTrue(s.eof())

    def test_one_list_with_one_identifier(self):
        tokens = [
            Token("("),
            Token("id", "foo"),
            Token(")"),
            ]
        s = TokenStream(tokens)

        eval.skip_list(s)

        self.assertTrue(s.eof())

    def test_one_list_with_one_number(self):
        tokens = [
            Token("("),
            Token("num", 5),
            Token(")"),
            ]
        s = TokenStream(tokens)

        eval.skip_list(s)

        self.assertTrue(s.eof())
    
    def test_two_nested_list(self):
        tokens = [
            Token("("),
            Token("("),
            Token(")"),
            Token(")"),
            ]
        s = TokenStream(tokens)

        eval.skip_list(s)

        self.assertTrue(s.eof())

if __name__ == "__main__":
    unittest.main()