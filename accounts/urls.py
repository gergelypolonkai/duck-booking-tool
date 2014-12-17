from django.conf.urls import patterns, url

from .views import RegistrationFormView

urlpatterns = patterns(
    '',
    url(
        r'^register$',
        RegistrationFormView.as_view(),
        name = 'register'
    ),
    url(
        r'^login$',
        'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'},
        name = 'login'
    ),
    url(
        r'^logout$',
        'django.contrib.auth.views.logout',
        {'next_page': 'booking:list'},
        name = 'logout'
    ),
)
