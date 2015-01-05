from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
from django_js_reverse.views import urls_js

from . import views

urlpatterns = patterns(
    '',
    url(r'^reverse.js$', cache_page(3600)(urls_js), name = 'js_reverse'),
    url(r'^duck/(?P<duck_id>\d+)/competence.json$', views.DuckCompListView.as_view(), name = 'complist'),
)
