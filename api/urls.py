from django.conf.urls import patterns, url, include

from rest_framework import routers

from . import views
from . import viewsets

rest_router = routers.DefaultRouter()
rest_router.register(r'ducks', viewsets.DuckViewSet)

urlpatterns = patterns(
    '',
    url(
        r'^',
        include(rest_router.urls)
    ),
    url(
        r'^duck/book/$',
        views.duck_book,
        name = 'book'
    ),
    url(
        r'^duck/(?P<duck_id>\d+)/competence.json$',
        views.DuckCompListView.as_view(),
        name = 'complist'
    ),
)
