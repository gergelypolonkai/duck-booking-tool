from django.conf.urls import patterns, url

from .views import RegistrationFormView

urlpatterns = patterns(
    '',
    url(
        r'^register$',
        RegistrationFormView.as_view(),
        name = 'register'
    ),
)
