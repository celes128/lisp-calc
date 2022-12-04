from lex import Token
from lex import TokenStream

def eval_token_list_remainder(s):
    """
    eval_list_remainder takes a stream of token as input and evaluates until a closing parenthesis is found.
    The parsing starts at the current position of the read pointer in the stream.
    The result of each evaluation is stored in a list and returned to the caller.

    INPUT
        s (TokenStream) The stream to parse.
    RETURN VALUE
        values (list of numbers) The list containing the result of all expressions.
    """

    values = []
    while (not s.eof()) and (s.get().type != ")"):
        if s.get().type == "(":
            values.append(eval_token_list(s))
        elif s.get().type == "num":
            values.append(s.get().value)
            s.next()
        else:
            raise Exception("Syntax error. Expecting a list or a number but got " + str(s.get()) + ".")
    
    return values

def eval_token_list(s):
    """
    eval_token_list takes a stream of token as input and evaluates it.
    The function expects the stream to have a syntax of a list.
    An exception is raised in case of any syntax error.

    INPUT
        s (TokenStream) The stream to parse.
    RETURN VALUE
        result (number) The result of evaluating the list.
    """

    assert type(s) == TokenStream
    
    s.match(Token("("))

    operators = [Token(c) for c in "+-*/"]
    op = s.match_one(*operators)
    values = eval_token_list_remainder(s)
    result = operator_compute(op.type, values)
    s.match(Token(")"))
    
    return result

def operator_compute(op, values):
    return 1