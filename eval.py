from lex import Token
from lex import TokenStream

class Environment():
    # Code to indicate wether a variable was inserted or its value updated.
    VAR_INSERTION = 1
    VAR_UPDATE = 2

    def __init__(self):
        self.vars = {}

    def set_variable(self, name, value):
        """
        set_variable inserts a new variable in the environment or updates its value if it already exists.
        """

        was_in = name in self.vars
        self.vars[name] = value

        if was_in:
            return Environment.VAR_UPDATE
        else:
            return Environment.VAR_INSERTION

    def contains(self, name, value, check_value = True):
        if not name in self.vars:
            return False

        if check_value:
            return self.vars[name] == value

    def var_value(self, name):
        if name in self.vars:
            return self.vars[name]
        else:
            raise Exception("Could not find a variable named " + name + " in the environment.")

def eval_token_list_remainder(s: TokenStream, env: Environment):
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
            values.append(eval_token_list(s, env))
        elif s.get().type == "num":
            values.append(s.get().value)
            s.next()
        else:
            raise Exception("Syntax error. Expecting a list or a number but got " + str(s.get()) + ".")
    
    return values

def eval_token_list(s: TokenStream, env: Environment):
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
    
    s.match("(")

    operators = (c for c in "+-*/")
    op = s.match_one(*operators)
    values = eval_token_list_remainder(s, env)
    result = operator_compute(op.type, values)
    s.match(")")
    
    return result

def operator_compute(op, values):
    if op == "+":
        res = 0
        for x in values:
            res += x
        return res
    elif op == "*":
        res = 1
        for x in values:
            res *= x
        return res
    else:
        raise Exception("In function operator_compute, operator " + op + " is unknown or not yet implemented.")

# Grammar rule
# LIST  ::=  TODO
def parse_list(s: TokenStream, env: Environment, evaluate: bool):
    raise Exception("Error: parse_list() is not yet implemented!")

# Grammar rule
# ATOM  ::=  number
#        |   identifier
def parse_atom(s: TokenStream, env: Environment, evaluate: bool):
    tok = s.match_one("num", "id")

    if not evaluate:
        return None

    if tok.type == "id":
        return env.var_value(tok.value)
    else:
        return tok.value

# Grammar rule
# EXPR  ::=  LIST
#        |   ATOM
def parse_expr(s: TokenStream, env: Environment, evaluate: bool):
    cur = s.get()
    if cur.type == "(":
        return parse_list(s, env, evaluate)
    elif cur.type in ["num", "id"]:
        return parse_atom(s, env, evaluate)
    else:
        raise Exception("Error in parse_expr: expecting a list or atom but got " + cur.type + ".")

def eval_expr(s: TokenStream, env: Environment):
    return parse_expr(s, env, evaluate=True)

# An atom is either a number or an identifier.
def skip_atom(s: TokenStream):
    tok = s.get()
    if tok.type in ["num", "id"]:
        s.next()
        return tok
    else:
        raise Exception("Error in skip_atom: expected an atom but got " + str(tok.type))

def skip_list(s: TokenStream):
    if s.get().type != '(':
        raise Exception("Error in skip_list: expecting ( but got " + str(s.get()) + ".")

    # Advance in the stream until we find the matching closing parenthesis
    # Counter for the current number of open parenthesis not matched
    n = 1
    s.next()
    while n > 0:
        if s.eof():
            raise Exception("Error in skip_list: unbalanced parenthesis found.")
        
        if s.get().type == ')':
            n -= 1
        elif s.get().type == '(':
            n += 1
        
        s.next()
    
def skip_expr(s: TokenStream):
    tok = s.get()
    if tok.type in ["num", "id"]:
        return skip_atom(s)
    elif tok.type == "(":
        return skip_list(s)
    else:
        raise Exception("Error in skip_expr: expecting atom or list but got " + str(tok))

# Grammar rule
# IF  ::=  '('  'if'  expr0  expr1  expr2?  ')'
def eval_if(s: TokenStream, env: Environment):
    """
    eval_if parses and evaluates an 'if' expression.

    RETURN VALUE
        If expr0 evaluates to true, the return value is the value expr1.
        Else...
            ... if there is expr2 (recall that expr2 is optional), the return value is the value of expr2,
            ... else the return value is None.
    """

    # The result of the if expression; return value
    result = None

    s.match("(")
    s.match("if")

    if eval_expr(s, env): # expr0
        result = eval_expr(s, env) # expr1

        # Check if there is the optional expression expr2 for the 'else' part of the if expression
        if s.get().type != ")":
            skip_expr(s) # parse expr2 without evaluating it
    else:
        skip_expr(s) # skip expr1
        
        # Check if there is the optional expression expr2 for the 'else' part of the if expression
        if s.get().type != ")":
            result = eval_expr(s, env) # expr2

    s.match(")")
    return result

def eval_setq(s: TokenStream, env: Environment):
    s.match("(")
    s.match("setq")
    name = s.match("id").value
    value = eval_expr(s, env)
    s.match(")")

    env.set_variable(name, value)

    return value