from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url('',   include('booking.urls', namespace = 'booking')),
)
