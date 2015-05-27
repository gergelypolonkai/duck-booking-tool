from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
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
