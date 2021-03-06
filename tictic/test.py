import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from libs.tictactoe import Tic, get_enemy
from libs.gameplay import (make_move, flatten_board, determine,
                           GID_ERROR, MOVE_INPUT_ERROR,
                           MOVE_UNAVAILABLE_ERROR, WINNER_MSG)


class TestGamePlay(TestCase):

    def setUp(self):
        response = self.client.get(reverse('tictic.index'))
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(str(response.content, encoding='utf8'))
        self.assertIn('gid', response_content.keys())
        self.gid = response_content['gid']
        self.board = response_content['board']

    def test_post_to_start(self):
        response = self.client.post(reverse('tictic.index'))
        self.assertEqual(response.status_code, 405)

    def test_get_to_move(self):
        response = self.client.get(reverse('tictic.move'))
        self.assertEqual(response.status_code, 405)

    def test_flatten_board(self):
        self.assertEqual(flatten_board([]), [])
        self.assertEqual(flatten_board([[1], [2, 3], [4]]), [1, 2, 3, 4])
        self.assertNotEqual(flatten_board([1, 2, [3, 4]]), [1, 2, 3, 4])
        self.assertIn('error', flatten_board([1, 2, [3, 4]]))

    def test_make_move_input(self):
        # nonexistent gid
        badmove = make_move(42, 20)
        self.assertEqual(type(badmove), dict)
        self.assertIn('error', badmove.keys())
        self.assertIn(GID_ERROR, badmove.values())

        # move out of range
        badmove = make_move(self.gid, 20)
        self.assertEqual(type(badmove), dict)
        self.assertIn('error', badmove.keys())
        self.assertIn(MOVE_INPUT_ERROR, badmove.values())

        # should be a good move
        goodmove = make_move(self.gid, 0)
        self.assertEqual(type(goodmove), dict)
        self.assertNotIn('error', goodmove.keys())
        # save the board after making the good move
        self.board = goodmove['board']

        # repeat the same move a second time
        badmove = make_move(self.gid, 0)
        self.assertEqual(type(badmove), dict)
        self.assertIn(MOVE_UNAVAILABLE_ERROR, badmove.values())

    def test_determine(self):
        complete_board = [['O', 'X', 'X'], ['X', 'X', 'O'], ['O', 'O', 'X']]
        game = Tic(flatten_board(complete_board))
        next_move = determine(game, 'X')
        self.assertEqual(next_move, None)

    def test_winning(self):
        player = 'X'
        goodmove = {}
        while 'winner' not in goodmove.keys():
            game = Tic(flatten_board(self.board))
            next_move = determine(game, get_enemy(player))
            if next_move is not None:
                print('next_move is {}'.format(next_move))
                goodmove = make_move(self.gid, next_move)
                self.board = goodmove['board']

        self.assertIn('winner', goodmove)
        game = Tic(flatten_board(self.board))
        self.assertEqual(game.complete(), True)
        self.assertIn(game.winner(), ['X', 'O', None])
        self.assertEqual(game.complete(), True)
        message = WINNER_MSG.format(game.winner())
        self.assertEqual(goodmove['winner'], message)
