# This is how client code uses Error objects.
#
#   # Case 1
#   x, y, z, err = foo()
#   if err:
#       print(err.message)
#       exit(1)
#
#   # Case 2
#   x, y, z, err = foo()
#   if not err:
#       print("Success!")

class Error():

    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __bool__(self):
        return self.code != 0

def new(message, code = -1):
    """new returns an Error object."""
    return Error(message, code)