import unittest


class Tescik(unittest.TestCase):
    def test_good(self):
        self.assertEquals(0, 0)

    def test_good2(self):
        self.assertEquals(1, 1)


if __name__ == '__main__':
    unittest.main()
