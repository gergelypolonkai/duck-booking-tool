from django.test import TestCase, Client
from django_webtest import WebTest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class FrontTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_user(
            username = 'admin',
            password = 'password')
        self.admin.save()

    def test_login_page(self):
        response = self.client.get('/accounts/login')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/accounts/login', {
            'next': '/',
            'username': 'admin',
            'password': 'password'})

        self.assertRedirects(response, '/')

    def test_logout(self):
        self.client.login(username = 'admin', password = 'aeou')

        response = self.client.get('/accounts/logout')
        self.assertRedirects(response, '/')

    def test_registration_page(self):
        response = self.client.get('/accounts/register')
        self.assertEqual(response.status_code, 200)

class RegFormTest(WebTest):
    def test_valid_data(self):
        form_data = {
            'username': 'test',
            'password1': 'password',
            'password2': 'password'
        }

        form = UserCreationForm(form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, 'test')
        # The password must be encrypted by now
        self.assertNotEqual(user.password, 'password')

    def test_empty(self):
        form_data = {}
        form = UserCreationForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['This field is required.'],
            'password1': ['This field is required.'],
            'password2': ['This field is required.'],
        })

    def test_form_error(self):
        page = self.app.get('/accounts/register')
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_form_success(self):
        page = self.app.get('/accounts/register')
        page.form['username'] = 'test'
        page.form['password1'] = 'password'
        page.form['password2'] = 'password'
        page = page.form.submit()
        self.assertRedirects(page, '/')
