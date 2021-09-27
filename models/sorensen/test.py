import unittest
from sorensens_dice import comparison


class TestComparison(unittest.TestCase):

    def test_positive(self):
        self.assertEqual(comparison('sun', 'sun'), 1.0)
        self.assertEqual(comparison('', ''), 1.0)
        self.assertEqual(comparison('abc', 'cba'), 1.0)
        self.assertEqual(comparison('sunflower', 'sun'), 0.5)
        self.assertEqual(comparison('sun sun sun sun', 'sun'), 0.3333333333333333)
        self.assertEqual(comparison('abc', 'mnl'), 0.0)

    def test_types(self):
        self.assertRaises(TypeError, comparison, 42)
        self.assertRaises(TypeError, comparison, True)
        self.assertRaises(TypeError, comparison, ['59.3333333', '12.5'])
        self.assertRaises(TypeError, comparison, 3 + 4j)
        self.assertRaises(TypeError, comparison, {1: 2})
        self.assertRaises(TypeError, comparison, (3, 4))

    def test_negative(self):
        self.assertNotEqual(comparison('sunsun', 'sun'), 1.0)
        self.assertNotEqual(comparison('nsu', 'sun'), 0.0)
        self.assertNotEqual(comparison('ssuunn', 'sun'), 1.0)
        self.assertNotEqual(comparison('s u n', 'sun'), 1.0)
        self.assertNotEqual(comparison('abc', 'def'), 1.0)
