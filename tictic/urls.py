from django.conf.urls import url

from tictic.views import StartGameView

urlpatterns = [
    url(r'^start/?$', StartGameView.as_view(), name='index'),
]
