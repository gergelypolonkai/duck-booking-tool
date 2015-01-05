from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class ReverseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_reverse_js(self):
        response = self.client.get(reverse('api:js_reverse'))
        self.assertEqual(response.status_code, 200)
