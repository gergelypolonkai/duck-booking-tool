from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
from django_js_reverse.views import urls_js

urlpatterns = patterns(
    '',
    url(r'^reverse.js$', cache_page(3600)(urls_js), name = 'js_reverse'),
)
