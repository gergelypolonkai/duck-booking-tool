from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns(
    '',
    url(
        r'^vocabulary.html$',
        TemplateView.as_view(template_name = 'booking/vocabulary.html'),
        name = 'vocabulary'
    ),
)
