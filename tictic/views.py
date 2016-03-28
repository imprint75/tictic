import logging
from uuid import uuid4

from django.http import JsonResponse
from django.views.generic import View
from django.core.cache import cache

from libs.tictactoe import Tic
from libs.gameplay import make_move

logger = logging.getLogger(__name__)
PARAM_EMPTY = 'Submit a gid and a move # if you want to make a move'


class StartGameView(View):
    def get(self, request, *args, **kwargs):
        tic = Tic()
        gid = uuid4()
        board = tic.show()
        cache.set(gid, board, timeout=None)
        return JsonResponse({'gid': gid, 'board': board})


class GameMoveView(View):
    def post(self, request, *args, **kwargs):
        gid = request.POST.get('gid')
        move = request.POST.get('move')

        if not all([gid, move]):
            return JsonResponse({'error': PARAM_EMPTY})

        return JsonResponse(make_move(gid, move))
