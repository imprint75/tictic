import logging

from django.http import JsonResponse
from django.views.generic import View

logger = logging.getLogger(__name__)


class StartGameView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'success': 'works'})
