import unittest

from models.levenshtein.levenshtein import distance


class TestLevenshteinDistance(unittest.TestCase):
    def test_distance(self):
        self.assertEqual(distance('Hello', 'Hello'), 0)


