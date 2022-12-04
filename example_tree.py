# This file shows an example of printing a tree that represen the following expression:
#
#           (+ 1 2 (* 3 (+ 4 5) 6))

from lex import Token
from tree import Node
from tree import print_tree

b = Node(Token("num", 1))
c = Node(Token("num", 2))

d = Node(Token("num", 3))
y = Node(Token("num", 10))
w = Node(Token("num", 20))
x = Node(Token("*"), [y, w])

e = Node(Token("num", 4))
f = Node(Token("*"), [d, x, e])

g = Node(Token("num", 5))

a = Node(Token("+"), [b, c, f, g])

print_tree(a)