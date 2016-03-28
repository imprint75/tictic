import logging
import random

from django.core.cache import cache

from libs.tictactoe import Tic, get_enemy
from libs.exceptions import MoveOutOfRangeError

logger = logging.getLogger(__name__)
GID_ERROR = 'No existing game with this gid'
MOVE_INPUT_ERROR = 'Move must be a number between 0-8'
MOVE_UNAVAILABLE_ERROR = 'Select an available move'
WINNER_MSG = 'winner is {}'


def make_move(gid, move):
    player1 = 'X'
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

    # initialize the cached board
    tic = Tic(flatten_board(board))

    # if there's already a winner, just return
    if tic.complete():
        res['winner'] = WINNER_MSG.format(tic.winner())
        return res

    if move not in tic.available_moves():
        res['error'] = MOVE_UNAVAILABLE_ERROR
        return res

    tic.make_move(move, player1)
    res.update(post_move(tic, gid))
    if 'winner' in res.keys():
        return res
    player2 = get_enemy(player1)
    computer_move = determine(tic, player2)
    tic.make_move(computer_move, player2)
    res.update(post_move(tic, gid))

    return res


def post_move(game, gid):
    """
    after making a move, we should:
    get updated board state, cache it and check for winner

    """

    res = {}
    board = game.show()
    res['board'] = board
    # cache the new board state
    cache.set(gid, board, timeout=None)
    if game.complete():
        res['winner'] = WINNER_MSG.format(game.winner())
    return res


def flatten_board(board):
    """
    game logic requires a flat list

    """

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
