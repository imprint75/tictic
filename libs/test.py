import unittest

from libs.gameplay import make_move, post_move, flatten_board


class TestGamePlay(unittest.TestCase):

    def test_flatten_board(self):
        self.assertEqual(flatten_board([]), [])
        self.assertEqual(flatten_board([[1],[2,3],[4]]), [1,2,3,4])
        self.assertEqual(flatten_board([1,2,[3,4]]), [1,2,3,4])
