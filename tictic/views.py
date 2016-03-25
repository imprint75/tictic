import logging
from uuid import uuid4

from django.http import JsonResponse
from django.views.generic import View
from django.core.cache import cache

from libs.tictactoe import Tic

logger = logging.getLogger(__name__)


class StartGameView(View):
    def get(self, request, *args, **kwargs):
        tic = Tic()
        gid = uuid4()
        board = tic.show()
        cache.set(gid, board, timeout=None)
        return JsonResponse({'gid': gid, 'board': board})


class GameMoveView(View):
    def post(self, request, *args, **kwargs):
        gid = request.POST.get('gid', '')
        res = {'gid': gid}

        board = cache.get(gid)
        if not board:
            res['error'] = 'No existing game matches this gid!'
            return JsonResponse(res)
        res['board'] = board

        return JsonResponse(res)
