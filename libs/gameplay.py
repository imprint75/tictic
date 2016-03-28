import logging
import random

from django.core.cache import cache

from libs.tictactoe import Tic, get_enemy
from libs.exceptions import MoveOutOfRangeError

logger = logging.getLogger(__name__)
GID_ERROR = 'No existing game with this gid'
MOVE_INPUT_ERROR = 'Move must be a number between 0-8'
WINNER_MSG = 'winner is {}'


def make_move(gid, move):
    res = {'gid': gid}

    try:
        move = int(move)
        if move > 8:
            raise MoveOutOfRangeError
    except (ValueError, MoveOutOfRangeError):
        res['error'] = MOVE_INPUT_ERROR
        return res

    board = cache.get(gid)
    if not board:
        res['error'] = GID_ERROR
        return res
    res['board'] = board

    try:
        tic = Tic(flatten_board(board))
    except Exception as e:
        logger.exception(e)

    if tic.complete():
        res['winner'] = WINNER_MSG.format(tic.winner())
        return res

    return res


def flatten_board(board):
    flat = []
    try:
        for l in board:
            for space in l:
                flat.append(space)
    except Exception as e:
        logger.exception(e)
    return flat


def determine(board, player):
    a = -2
    choices = []
    if len(board.available_moves()) == 9:
        return 4
    for move in board.available_moves():
        board.make_move(move, player)
        val = board.alphabeta(board, get_enemy(player), -2, 2)
        board.make_move(move, None)
        #print("move:", move + 1, "causes:", board.winners[val + 1])
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)
