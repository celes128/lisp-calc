import unittest
from lex import Token
from lex import TokenStream

class TestTokenStream(unittest.TestCase):

    def test_eof_if_empty_stream(self):
        ts = TokenStream()

        self.assertTrue(ts.eof())

    def test_get1(self):
        tokens = [Token("num", 5)]
        ts = TokenStream(tokens)

        self.assertEqual(ts.get(), tokens[0])

    def test_next(self):
        tokens = [Token("num", 5), Token("+")]
        ts = TokenStream(tokens)

        self.assertEqual(ts.get(), tokens[0])

        ts.next()
        self.assertEqual(ts.get(), tokens[1])

        ts.next()
        self.assertTrue(ts.eof())

    def test_match1(self):
        tokens = [Token("+")]
        ts = TokenStream(tokens)

        # match does not return anything.
        # It raises an exception if the match failed.
        # So there is no assertion to verify.
        ts.match(Token("+"))

    def test_match_one1(self):
        ts = TokenStream([Token("+")])

        candidates = [Token("-"), Token("+")]
        matched = ts.match_one(candidates)

        self.assertEqual(matched, Token("+"))
    
    # Check that match_one() raises an exception when no token match.
    def test_match_one_failure1(self):
        ts = TokenStream([Token("+")])

        candidates = [Token("-"), Token("*")]
        self.assertRaises(Exception, ts.match_one, candidates)

if __name__ == "__main__":
    unittest.main()