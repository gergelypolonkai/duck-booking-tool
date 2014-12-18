from django.test import TestCase, Client
from django.utils import timezone

import datetime

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
