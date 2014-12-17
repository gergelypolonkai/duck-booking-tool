from django.test import TestCase, Client
from django.utils import timezone

import datetime

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
