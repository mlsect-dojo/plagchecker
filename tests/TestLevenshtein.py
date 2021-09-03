import unittest

from models.levenshtein.levenshtein import distance


class TestLevenshteinDistance(unittest.TestCase):
    def test_distance(self):
        self.assertEqual(distance('Hello', 'Hello'), 0)
        self.assertEqual(distance('Privet','Hello'), 6)
        self.assertNotEqual(distance('Arq','SuS'), 0)
        self.assertNotEqual((distance('Spisannaya laba', 'written by himself')), 10)
        self.assertEqual((distance('Spisannayalaba', 'Spisannaya laba')), 1)
        self.assertNotEqual((distance('Spisannaya laba','spisannaya_laba')), 0)
        self.assertEqual((distance('Nastoyawaya laba', 'nastoyawaya_laba')), 2)


if __name__ == "__main__":
    unittest.main()