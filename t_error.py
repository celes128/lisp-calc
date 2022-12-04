import unittest
import error

class TestError(unittest.TestCase):

    def test_error_new(self):
        err = error.new("Failed.", -1)

        self.assertTrue(err)
        self.assertEqual(err.message, "Failed.")
        self.assertEqual(err.code, -1)

if __name__ == '__main__':
    unittest.main()