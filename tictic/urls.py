from django.conf.urls import url

import tictic.views

urlpatterns = [
    url(r'^start/?$', tictic.views.StartGameView.as_view(), name='index'),
]
