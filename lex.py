# File: lex.py
# Description:  Lexical analysis functions and the Token.

import error

# Utils
def to_str(tokens):
    """to_str converts a list of token to a string."""
    
    s = "["
    for i in range(len(tokens)):
        s += str(tokens[i])
        if i + 1 < len(tokens):
            s += ", "
    s += "]"
    return s

class Token():

    def __init__(self, _type, _value = 0):
        self.type = _type
        self.value = _value

    def __eq__(self, o):
        return self.type == o.type and self.value == o.value

    def __str__(self):
        if self.type != "num":
            return self.type
        else:
            return str(self.value)

class TokenStream():

    def __init__(self, tokens = []):
        self._tokens = tokens
        # The read pointer - Index in the list of tokens.
        self._i = 0

    def eof(self):
        """eof eturns True iff the read pointer is at the end of the stream."""
        return self._i >= len(self._tokens)

    def get(self):
        """
        get returns the curent token.

        EXCEPTIONS
            Raises an exception if at eof.
        """

        if not self.eof():
            return self._tokens[self._i]
        else:
            raise Exception("Cannot call get when at eof.")

    def next(self):
        """
        next advances the read pointer to the next token (i.e. by one position to the right in the stream).
        
        EXCEPTIONS
            Raises an exception if at eof.
        """

        if not self.eof():
            self._i += 1
        else:
            raise Exception("Cannot call next when at eof.")

    def match(self, tok):
        """match checks that the current token matches the one given as parameter and advances to the next token (by calling next)."""

        if not self.eof():
            if tok == self.get():
                self.next()
            else:
                raise Exception("match failed: expected " + str(tok) + " but got " + str(self.get()) + ".")
        else:
            raise Exception("Cannot call match when at eof.")

    def match_one(self, *tokens):
        """
        match_one checks if the current token matches a token from the ones given as parameter and advances to the next token.
        
        RETURN VALUE
            Returns the token that matched.

        EXCEPTIONS
            Raises an exception if at eof.
        """

        if not self.eof():
            cur = self.get()

            for tok in tokens:
                if tok == cur:
                    self.next()
                    return cur
            
            # Error: none matched.
            raise Exception("match_one failed: expected one of " + to_str(tokens) + " but got " + str(self.get()) + ".")
        else:
            raise Exception("Cannot call match when at eof.")

def tokenize(expr):
    tokens = []

    i = 0

    while i < len(expr):
        c = expr[i]

        if c in "()+-*/":
            tokens.append(Token(str(c)))
            i += 1
        else:
            return [], error.new("Invalid character '" + c + "'.")

    return tokens, None

def parse_number(s, i = 0):
    """
    parse_number parses a number in a string.

    INPUT
        s (string) The string to parse.
        i (integer) The position in the string where the parsing starts.

    RETURN VALUE
        x (number) The number parsed in the string s.
        i (integer) The index of the read cursor in the string positioned right after the number read.
        err (error.Error) An Error object indicating if the parsing failed.

    REMARKS
        Number overflow is not handled.
    """

    # We save the original value of i because in case of a syntax error,
    # we need to return its original value.
    original_i = i

    i = skip_blanks(s, i)
    if i >= len(s):
        return 0, original_i, error.new("No number found.")

    # Read an optional minus sign.
    sign = 1 # We assume there is no minus sign.
    if s[i] == '-':
        sign = -1
        i += 1

    i = skip_blanks(s, i)

    # Read an optional integral part.
    int_str, i = parse_digit_sequence(s, i)
    integer = int(int_str) if len(int_str) >= 1 else 0

    # Read an optional point.
    point = i < len(s) and s[i] == '.'
    if point:
        i += 1

    # At this point we can detect a syntax error.
    if not point:
        if len(int_str) != 0:
            # There is no point but there is an integral part.
            # We successfully parsed an integer.
            return sign * integer, i, None
        else:
            # There is no point and there is no integral part.
            # Hence there was no number to parse.
            return 0, original_i, error.new("No number found.")

    # Read an optional fractional part.
    frac_str, i = parse_digit_sequence(s, i)
    frac = 0.0 if len(frac_str) == 0 else int(frac_str) / 10**len(frac_str)

    # We have to check the case of a single point (with no integral part nor a fractional part).
    if point and len(int_str) == 0 and len(frac_str) == 0:
        return 0, original_i, error.new("Invalid number ssyntax; found only a point.")

    # We are done parsing the floating point number.
    return sign * (integer + frac), i, None

def skip_blanks(s, i):
    """skip_blanks advances the index i in s to skip whitespaces, tabulations, carriage returns and newline characters."""

    while i < len(s) and s[i] in " \t\r\n":
        i += 1

    return i

# def skip_digit_sequence(s, i):
#     """skip_digit_sequence advances the index i to skip any digits 0-9."""

#     while i < len(s) and s[i].isdigit():
#         i += 1

#     return i

def parse_digit_sequence(s, i):
    """
    parse_digit_sequence tries to parse a sequence of digits (0 to 9) in a string s starting at index i.
    If no digit is at index i or if i is out of range then the empty string is returned.

    RETURN VALUE
        sequence (string)
            The longuest sequence of digits starting at index i in s. Can be the empty string.
        i (integer)
            The new position i pointing right after the digit sequence.

    EXAMPLE
        s = "abc128ef"

        # General case
        seq, i = parse_digit_sequence(s, 3)  # seq = "128", i = 6

        # Special case: no digit at i
        seq, i = parse_digit_sequence(s, 0)  # seq = "", i = 3
    """

    begin = i
    while i < len(s) and s[i].isdigit():
        i += 1
    return s[begin:i], i

def parse_identifier(s, i = 0):
    """
    The syntax for valid identifiers is defined by the following rules:
        (1) the first character must either be a letter [a-zA-Z] or an underscore '_' and,
        (2) the remaining characters can be letters, digits, or any characters - _ ! ?.
    """

    original_i = i

    if i >= len(s):
        return "", original_i, error.new("Start index is out of the string bounds.")

    c = s[i]
    valid_start = c.isalpha() or c == '_'
    if not valid_start:
        return "", original_i, error.new("Does not match the syntax of an identifier.")

    # Succes! We keep parsing until the end of the identifier.
    begin = i
    i += 1
    while i < len(s) and (s[i].isalpha() or s[i].isdigit() or s[i] in "-_!?"):
        i += 1
    
    return s[begin:i], i, None