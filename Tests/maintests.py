import unittest


class Tescik(unittest.TestCase):
    def good(self):
        self.assertEquals(0, 0)

    def good2(self):
        self.assertEquals(1, 1)


if __name__ == '__main__':
    unittest.main()
