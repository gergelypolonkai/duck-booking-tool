from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/',    include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls', namespace = 'accounts')),
    url(r'^api/',      include('api.urls',      namespace = 'api')),
    url('',            include('booking.urls',  namespace = 'booking')),
)
