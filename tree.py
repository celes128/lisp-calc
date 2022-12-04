from lex import Token

class Node():

    def __init__(self, token, children = []):
        self.token = token
        self.children = children

def print_tree(tree):
    return recur_print_tree(tree, "", 0, True)

def recur_print_tree(tree, prefix, level, last_child):
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
        recur_print_tree(tree.children[i], prefix, level + 1, i + 1 >= len(tree.children))

# def recur_print_tree(tree, prefix):
#     if tree.token.type == "num":
#         print(prefix + str(tree.token))
#     else:
#         # We assume tree.token is an operator.
#         print(prefix + str(tree.token))

#         if len(tree.children) == 0:
#             return
        
#         # Replace the prefix only if not at the root <=> len(prefix) > 0
#         if len(prefix) > 0:
#             prefix = prefix[:-3] + "   "
        
#         # Print each child
#         for i in range(len(tree.children)):
#             # Compute the new prefix for the child
#             new_prefix = prefix
#             if i + 1 < len(tree.children):# non-last child
#                 new_prefix = prefix + "|__ "
#             else:# last child
#                 if len(prefix) > 0:
#                     new_prefix = prefix[:-3] + "   |__ "
#                 else:
#                     new_prefix = "    "
            
#             # Print the child's tree
#             recur_print_tree(tree.children[i], new_prefix)
        