from django.test import TestCase, Client

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
