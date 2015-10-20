# -*- coding: utf-8
"""
URL patterns for the accounts module
"""

from django.conf.urls import url

from .views import RegistrationFormView

urlpatterns = [
    url(
        r'^register$',
        RegistrationFormView.as_view(),
        name='register'
    ),
    url(
        r'^login$',
        'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'},
        name='login'
    ),
    url(
        r'^logout$',
        'django.contrib.auth.views.logout',
        {'next_page': 'booking:list'},
        name='logout'
    ),
]
