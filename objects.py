class String():
    def __init__(self, s=""):
        self.s = s
    
    def __str__(self):
        return self.s

class Number():
    def __init__(self, value = 0):
        self.value = value

    def __str__(self):
        return str(self.value)