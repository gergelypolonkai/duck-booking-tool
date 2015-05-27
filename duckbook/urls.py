from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.decorators.cache import cache_page

from django_js_reverse.views import urls_js

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}
    ),
    url(
        r'^reverse.js$',
        cache_page(3600)(urls_js),
        name = 'js_reverse'
    ),
    url(r'^admin/',    include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls', namespace = 'accounts')),
    url(r'^api/',      include('api.urls',      namespace = 'api')),
    url('',            include('booking.urls',  namespace = 'booking')),
)
