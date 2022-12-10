import unittest
from stack import Stack

class TestStack(unittest.TestCase):

    def test_ANewStackIsEmpty(self):
        s = Stack()

        self.assertTrue(s.empty())
        self.assertEqual(s.size(), 0)

    def test_PushOne(self):
        s = Stack()

        s.push(1)

        self.assertFalse(s.empty())
        self.assertEqual(s.size(), 1)
        self.assertEqual(s.top(), 1)
    
    def test_PushOneThenPop(self):
        s = Stack()

        s.push(1)
        x = s.pop()

        self.assertEqual(x, 1)
        self.assertTrue(s.empty())

    def test_PopTwoItemsThenPopThem(self):
        s = Stack()

        n = 2
        for i in range(n):
            s.push(i)

        got = []
        for i in range(n):
            got.append(s.pop())

        self.assertEqual(got, [i for i in range(n-1, -1, -1)])

    def test_Top(self):
        s = Stack()
        s.push(10)
        x = s.top()

        self.assertEqual(x, 10)
        self.assertEqual(s.size(), 1)

if __name__ == "__main__":
    unittest.main()