from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^accounts/', include('accounts.urls', namespace = 'accounts')),
    url('',            include('booking.urls',  namespace = 'booking')),
)
