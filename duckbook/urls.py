from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}
    ),
    url(r'^admin/',    include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls', namespace = 'accounts')),
    url(r'^api/',      include('api.urls',      namespace = 'api')),
    url('',            include('booking.urls',  namespace = 'booking')),
)
