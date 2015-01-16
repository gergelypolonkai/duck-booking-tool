from django.test import TestCase, Client
from django.utils import timezone
from django.conf import settings

import datetime

from .ducklevel import level_to_up_minutes, level_to_down_minutes, minutes_to_level
from .templatetags import booking_tags
from .models import Duck

class FrontTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_vocabulary_page(self):
        response = self.client.get('/vocabulary.html')
        self.assertEqual(response.status_code, 200)

    def test_terms_page(self):
        response = self.client.get('/terms.html')
        self.assertEqual(response.status_code, 200)

    def test_disclaimer_page(self):
        response = self.client.get('/disclaimer.html')
        self.assertEqual(response.status_code, 200)

class DuckCompLevelTest(TestCase):
    def test_sane_max(self):
        self.assertGreater(
            settings.MAX_DUCK_LEVEL, 0,
            msg = "MAX_DUCK_LEVEL must be greater than zero!")

    def test_max_minutes(self):
        """Test if level can not go above settings.MAX_DUCK_LEVEL)"""

        max_up_minutes = level_to_up_minutes(settings.MAX_DUCK_LEVEL)
        double_minutes = level_to_up_minutes(settings.MAX_DUCK_LEVEL * 2)
        max_down_minutes = level_to_down_minutes(settings.MAX_DUCK_LEVEL)

        level = minutes_to_level(max_up_minutes, 0)
        self.assertEqual(level, settings.MAX_DUCK_LEVEL)

        level = minutes_to_level(max_up_minutes + 1, 0)
        self.assertEqual(level, settings.MAX_DUCK_LEVEL)

        level = minutes_to_level(double_minutes, 0)
        self.assertEqual(level, settings.MAX_DUCK_LEVEL)

        level = minutes_to_level(0, max_down_minutes)
        self.assertEqual(level, settings.MAX_DUCK_LEVEL)

        level = minutes_to_level(0, max_down_minutes + 1)
        self.assertEqual(level, settings.MAX_DUCK_LEVEL)

    def test_conversions(self):
        for i in range(1, settings.MAX_DUCK_LEVEL):
            up_minutes = level_to_up_minutes(i)
            down_minutes = level_to_down_minutes(i)

            up_level = minutes_to_level(up_minutes, 0)
            down_level = minutes_to_level(0, down_minutes)

            self.assertEqual(up_level, i, msg = "Test failed for value %d" % i)
            self.assertEqual(
                down_level, i,
                msg = "Test failed for value %d" % i)

    def test_level_to_minutes(self):
        self.assertEqual(level_to_up_minutes(0), 0)
        self.assertEqual(level_to_up_minutes(1), 20)
        self.assertEqual(level_to_up_minutes(2), 200)
        self.assertEqual(level_to_up_minutes(3), 2000)
        self.assertEqual(level_to_up_minutes(4), 20000)
        self.assertEqual(level_to_up_minutes(5), 200000)

        self.assertEqual(level_to_down_minutes(0), 0)
        self.assertEqual(level_to_down_minutes(1), 200)
        self.assertEqual(level_to_down_minutes(2), 2000)
        self.assertEqual(level_to_down_minutes(3), 20000)
        self.assertEqual(level_to_down_minutes(4), 200000)
        self.assertEqual(level_to_down_minutes(5), 2000000)

class DuckAgeTest(TestCase):
    def test_duck_is_from_the_future(self):
        future_duck = Duck(donated_at = timezone.now() + datetime.timedelta(days = 2))
        self.assertEqual(future_duck.age(), -1)

    def test_duck_age_formatter(self):
        self.assertEqual(booking_tags.age_format("aoeu"), "aoeu")
        self.assertEqual(booking_tags.age_format(0), "a few moments")
        self.assertEqual(booking_tags.age_format(1), "1 second")
        self.assertEqual(booking_tags.age_format(2), "2 seconds")
        self.assertEqual(booking_tags.age_format(60), "1 minute")
        self.assertEqual(booking_tags.age_format(61), "1 minute 1 second")
        self.assertEqual(booking_tags.age_format(62), "1 minute 2 seconds")
        self.assertEqual(booking_tags.age_format(120), "2 minutes")
        self.assertEqual(booking_tags.age_format(3600), "1 hour")
        self.assertEqual(booking_tags.age_format(3601), "1 hour 1 second")
        self.assertEqual(booking_tags.age_format(3660), "1 hour 1 minute")
        self.assertEqual(booking_tags.age_format(3720), "1 hour 2 minutes")
        self.assertEqual(booking_tags.age_format(7200), "2 hours")
        self.assertEqual(booking_tags.age_format(86400), "1 day")
        self.assertEqual(booking_tags.age_format(86401), "1 day 1 second")
        self.assertEqual(booking_tags.age_format(86460), "1 day 1 minute")
        self.assertEqual(booking_tags.age_format(90000), "1 day 1 hour")
        self.assertEqual(booking_tags.age_format(93600), "1 day 2 hours")
        self.assertEqual(booking_tags.age_format(172800), "2 days")
        self.assertEqual(booking_tags.age_format(2592000), "1 month")
        self.assertEqual(booking_tags.age_format(2592001), "1 month 1 second")
        self.assertEqual(booking_tags.age_format(2592060), "1 month 1 minute")
        self.assertEqual(booking_tags.age_format(2595600), "1 month 1 hour")
        self.assertEqual(booking_tags.age_format(2678400), "1 month 1 day")
        self.assertEqual(booking_tags.age_format(2764800), "1 month 2 days")
        self.assertEqual(booking_tags.age_format(5184000), "2 months")
        self.assertEqual(booking_tags.age_format(31536000), "1 year")
        self.assertEqual(booking_tags.age_format(31536001), "1 year 1 second")
        self.assertEqual(booking_tags.age_format(31536060), "1 year 1 minute")
        self.assertEqual(booking_tags.age_format(31539600), "1 year 1 hour")
        self.assertEqual(booking_tags.age_format(31622400), "1 year 1 day")
        self.assertEqual(booking_tags.age_format(34128000), "1 year 1 month")
        self.assertEqual(booking_tags.age_format(36720000), "1 year 2 months")
        self.assertEqual(booking_tags.age_format(63072000), "2 years")
