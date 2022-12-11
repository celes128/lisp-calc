class ConstantPool():

    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def get(self, i):
        return self._items[i]