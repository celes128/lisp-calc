import unittest
import lex

class TestTokenize(unittest.TestCase):

    def test_1(self):
        expr = "()+-*/"
        exp = [lex.Token(str(c)) for c in expr]

        tokens, err = lex.tokenize(expr)
        self.assertFalse(err)
        self.assertEqual(tokens, exp)
        
class TestParseNumber(unittest.TestCase):
    
    def test_0_to_9(self):
        for n in range(10):
            x, i, err = lex.parse_number(str(n))

            self.assertFalse(err)
            self.assertEqual(x, n)
            self.assertEqual(i, 1)
    
    def test_minus_0_to_9(self):
        for n in range(10):
            x, i, err = lex.parse_number("-" + str(n))

            self.assertFalse(err)
            self.assertEqual(x, - n)
            self.assertEqual(i, 2)
    
    def test_minus_blank_0_to_9(self):
        for n in range(10):
            x, i, err = lex.parse_number("- " + str(n))

            self.assertFalse(err)
            self.assertEqual(x, - n)
            self.assertEqual(i, 3)

    # Checks that the function skips the leading blanks and successfully parse the following number.
    def test_leading_blanks(self):
        x, i, err = lex.parse_number(" 128")

        self.assertFalse(err)
        self.assertEqual(x, 128)
        self.assertEqual(i, 4)

    def test_1_2(self):
        x, i, err = lex.parse_number("1.2")

        self.assertFalse(err)
        self.assertEqual(x, 1.2)
        self.assertEqual(i, 3)

    def test_minus_1_2(self):
        x, i, err = lex.parse_number("-1.2")

        self.assertFalse(err)
        self.assertEqual(x, -1.2)
        self.assertEqual(i, 4)

    def test_point_2(self):
        x, i, err = lex.parse_number(".2")

        self.assertFalse(err)
        self.assertEqual(x, 0.2)
        self.assertEqual(i, 2)
    
    def test_minus_point_2(self):
        x, i, err = lex.parse_number("-.2")

        self.assertFalse(err)
        self.assertEqual(x, -0.2)
        self.assertEqual(i, 3)

    def test_point(self):
        x, i, err = lex.parse_number(".")

        self.assertTrue(err)
        self.assertEqual(i, 0)

class TestParseIdentifier(unittest.TestCase):

    def test_x(self):
        ident, i, err = lex.parse_identifier("x", 0)

        self.assertFalse(err)
        self.assertEqual(ident, "x")
        self.assertEqual(i, 1)

    def test_underscore(self):
        ident, i, err = lex.parse_identifier("_", 0)

        self.assertFalse(err)
        self.assertEqual(ident, "_")
        self.assertEqual(i, 1)
    
    def test_with_digits(self):
        ident, i, err = lex.parse_identifier("x1", 0)

        self.assertFalse(err)
        self.assertEqual(ident, "x1")
        self.assertEqual(i, 2)
        
    def test_with_minus(self):
        ident, i, err = lex.parse_identifier("my-name", 0)

        self.assertFalse(err)
        self.assertEqual(ident, "my-name")
        self.assertEqual(i, 7)

if __name__ == '__main__':
    unittest.main()