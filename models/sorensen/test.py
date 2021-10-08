import unittest
from sorensens_dice import comparison


class TestComparison(unittest.TestCase):

    def test_positive(self):
        self.assertEqual(comparison(['sun'], ['sun']), 1.0)
        self.assertEqual(comparison(['a', '+', 'b'], ['b', '+', 'a']), 1.0)
        self.assertEqual(comparison(['int', 'input', '()'], ['int', 'input', '(":")']), 2/3)
        self.assertEqual(comparison(['int', 'input', '()'], ['str', 'input', '(":")']), 1/3)
        self.assertEqual(comparison(['_init_'], ['__init__']), 0.0)

    def test_negative(self):
        self.assertNotEqual(comparison(['openspace'], ['open_space']), 1.0)
        self.assertNotEqual(comparison(['openspace'], ['open', 'space']), 1.0)
        self.assertNotEqual(comparison(['openspace'], ['"openspace"']), 1.0)
        self.assertNotEqual(comparison(['openspace'], [' openspace']), 1.0)
        self.assertNotEqual(comparison(['openspace'], ["openspace"]), 0.0)

    def test_types(self):
        self.assertRaises(TypeError, comparison, 42, 15)
        self.assertRaises(TypeError, comparison, True, True)
        self.assertRaises(TypeError, comparison, '3', [25])
        self.assertRaises(TypeError, comparison, (1, 2), ["25"])
        self.assertRaises(TypeError, comparison, [3], '25')
