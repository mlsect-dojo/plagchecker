import unittest

from models.Jaccard.jaccard import JaccardIndex


class TestJaccardIndex(unittest.TestCase):
    def test_index_positive(self):
        self.assertEqual(JaccardIndex("Spisannaya laba", "written by himself"), 0.4117647058823529)
        self.assertEqual(JaccardIndex('0123334', '765443'), 0.25)
        self.assertEqual(JaccardIndex('his thought process was on so many levels that he gave himself a phobia of '
                                      'heights',
                                      'there is an art to getting your way and throwing bananas on to the street is '
                                      'not it '
                                      ), 0.6818181818181818)
        self.assertEqual(JaccardIndex('there is an art to getting your way and throwing bananas on to the street is '
                                      'not it',
                                      'it is not often you find soggy bananas on the street'
                                      ), 0.8823529411764706)

    def test_index_negative(self):
        self.assertNotEqual(JaccardIndex('SuS', 'Arq'), 1.0)
        self.assertNotEqual(JaccardIndex('12345', '54321'), 0)


if __name__ == "__main__":
    unittest.main()
