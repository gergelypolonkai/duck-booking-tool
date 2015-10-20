# -*- coding: utf-8
"""
Main URL definitions file
"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}
    ),
    url(
        r'^admin/',
        include(admin.site.urls)),
    url(
        r'^accounts/',
        include('accounts.urls', namespace='accounts')),
    url(
        r'^api/v1/',
        include('api.urls', namespace='api')),
    url(
        '',
        include('booking.urls', namespace='booking')),
]
