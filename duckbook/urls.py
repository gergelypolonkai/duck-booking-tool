from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url('^$', TemplateView.as_view(template_name = 'front_template.html'), name = 'index'),
    url('',   include('booking.urls', namespace = 'booking')),
)
