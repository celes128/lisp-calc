from lex import Token

class Node():

    def __init__(self, token, children = []):
        self.token = token
        self.children = children

def print_tree(tree):
    return _recur_print_tree(tree, "", 0, True)

def _recur_print_tree(tree, prefix, level, last_child):
    if level != 0:
        print(prefix + "|__ " + str(tree.token))
    else:
        print(str(tree.token))
    
    if tree.token.type == "num" or len(tree.children) == 0:
        return

    if level != 0:
        if last_child:
            prefix += "    "
        else:
            prefix += "|   "

    for i in range(len(tree.children)):
        _recur_print_tree(tree.children[i], prefix, level + 1, i + 1 >= len(tree.children))