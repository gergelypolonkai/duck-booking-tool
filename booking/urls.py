from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from .views import DuckListView

urlpatterns = patterns(
    '',
    url(r'^$', DuckListView.as_view(), name = 'list'),
    url(
        r'^vocabulary.html$',
        TemplateView.as_view(template_name = 'booking/vocabulary.html'),
        name = 'vocabulary'
    ),
    url(
        r'^terms.html$',
        TemplateView.as_view(template_name = 'booking/terms.html'),
        name = 'terms'
    ),
    url(
        r'^disclaimer.html$',
        TemplateView.as_view(template_name = 'booking/disclaimer.html'),
        name = 'disclaimer'
    ),
)
