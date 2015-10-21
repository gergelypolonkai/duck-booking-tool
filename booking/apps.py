# -*- coding: utf-8
"""
App config for the booking module of the Duck Booking Tool. This module
is currently needed for the MAX_DUCK_LEVEL system check.
"""

from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error, register
from django.core.exceptions import ImproperlyConfigured

@register()
def max_level_check(app_configs, **kwargs):
    """
    System check to see if MAX_DUCK_LEVEL has a sane value (non-zero,
    positive integer)
    """

    errors = []

    if not hasattr(settings, 'MAX_DUCK_LEVEL'):
        errors.append(
            Error(
                'MAX_DUCK_LEVEL is not set!',
                id='booking.E001'
            )
        )
    else:
        if settings.MAX_DUCK_LEVEL <= 0:
            errors.append(
                Error(
                    'MAX_DUCK_LEVEL should be greater than zero!',
                    id='booking.E002'
                )
            )

        if not isinstance(settings.MAX_DUCK_LEVEL, int):
            errors.append(
                Error(
                    'MAX_DUCK_LEVEL must be an integer!',
                    id='booking.E003'
                )
            )

    return errors

class BookingConfig(AppConfig):
    name = 'booking'
