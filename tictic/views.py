import logging
from uuid import uuid4

from django.http import JsonResponse
from django.views.generic import View

logger = logging.getLogger(__name__)


class StartGameView(View):
    def get(self, request, *args, **kwargs):
        gid = uuid4()
        return JsonResponse({'gid': gid})
