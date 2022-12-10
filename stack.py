class Stack():

    def __init__(self):
        # The actual stack
        self._s = []
        # Points to the next empty slot; the actual top item is at index _top - 1
        self._top = 0

    def size(self):
        return self._top

    def empty(self):
        return self.size() == 0

    def push(self, x):
        if self._top < len(self._s):
            self._s[self._top] = x
        else:
            self._s.append(x)
        
        self._top += 1

    def top(self):
        return self._s[self._top - 1]

    def pop(self):
        self._top -= 1
        return self._s[self._top]
