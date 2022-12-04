# I use this file to quickly test some Python code.

def f(*args):
    for arg in args:
        print(arg, end=', ')

f(1,2,3,4,5)