from django.conf.urls import url

from tictic.views import StartGameView, GameMoveView

urlpatterns = [
    url(r'^start/?$', StartGameView.as_view(), name='index'),
    url(r'^move?$', GameMoveView.as_view(), name='move'),
]
