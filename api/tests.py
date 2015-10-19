from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.conf import settings
from django_webtest import WebTest

import json

from booking.ducklevel import level_to_up_minutes
from booking.models import Species, Location, Duck, Competence, DuckCompetence

class DuckClassTest(WebTest):
    csrf_checks = False

    def setUp(self):
        good_minutes = level_to_up_minutes(settings.COMP_WARN_LEVEL + 1)
        bad_minutes = level_to_up_minutes(settings.COMP_WARN_LEVEL)

        self.user = User.objects.create_user(username='test',
                                             password='test')

        spec = Species(name = 'duck')
        spec.save()

        loc = Location(name = 'temp')
        loc.save()

        self.comp_bad = Competence(name = 'test1', added_by = self.user)
        self.comp_bad.save()

        self.comp_good = Competence(name = 'test2',
                                    added_by = self.user)
        self.comp_good.save()

        self.duck = Duck(species = spec,
                         location = loc,
                         donated_by = self.user,
                         color='123456')
        self.duck.save()

        dcomp = DuckCompetence(duck = self.duck,
                               comp = self.comp_bad,
                               up_minutes = bad_minutes,
                               down_minutes = 0)
        dcomp.save()

        dcomp = DuckCompetence(duck = self.duck,
                               comp = self.comp_good,
                               up_minutes = good_minutes,
                               down_minutes = 0)
        dcomp.save()

    def test_book_nonlogged(self):
        page = self.app.post('/api/v1/ducks/1/book/', expect_errors=True)
        self.assertEqual(page.status_code, 403)

    def test_book_nonexist(self):
        # Try to book a non-existing duck
        page = self.app.post(
            '/api/v1/ducks/9999/book/',
            params={
                'competence': self.comp_good.pk,
            },
            user=self.user,
            expect_errors=True)
        self.assertEqual(404, page.status_code)

        # Try to book an existing Duck for a non-existing competence
        page = self.app.post(
            '/api/v1/ducks/%d/book/' % self.duck.pk,
            params={
                'competence': 9999
            },
            user=self.user,
            expect_errors=True)
        self.assertEqual(404, page.status_code)

    def test_book_warn(self):
        test_data = {
            'competence': self.comp_bad.pk,
        }
        url = '/api/v1/ducks/%d/book/' % self.duck.pk

        page = self.app.post(url, params=test_data, user=self.user)
        self.assertEquals(200, page.status_code)

        page_json = json.loads(page.content)
        self.assertEquals(page_json['status'], 'bad-comp')

        test_data['force'] = 1

        page = self.app.post(url, params=test_data, user=self.user)
        self.assertEqual(200, page.status_code)

        page_json = json.loads(page.content)
        self.assertEquals(page_json['status'], 'ok')

    def test_book_good(self):
        test_data = {
            "competence": self.comp_good.pk
        }

        url = '/api/v1/ducks/%d/book/' % self.duck.pk
        # Book the duck
        page = self.app.post(url, params=test_data, user=self.user)
        self.assertEquals(200, page.status_code)

        page_json = json.loads(page.content)
        self.assertEqual(page_json['status'], 'ok')

        # Try to book again, it should fail
        page = self.app.post(url, params=test_data, user=self.user)
        self.assertEqual(200, page.status_code)

        page_json = json.loads(page.content)
        self.assertEqual('already-booked', page_json['status'])

    def test_duck_donation(self):
        # Duck donation should not be allowed without logging in
        page = self.app.get('/api/v1/ducks/donate/', expect_errors=True)
        self.assertEquals(page.status_code, 403)

        # Duck donation should not be allowed withoud logging in
        page = self.app.post('/api/v1/ducks/donate/', expect_errors=True)
        self.assertEquals(page.status_code, 403)

        page = self.app.post(
            '/api/v1/ducks/donate/',
            params={
                'species': 1,
                'color': '123456',
            },
            user=self.user)
        page_json = json.loads(page.content)

    def test_duck_details(self):
        url = '/api/v1/ducks/%d/' % self.duck.pk
        page = self.app.get(url)
        self.assertEqual(200, page.status_code)

        page_json = json.loads(page.content)
        self.assertEqual(len(page_json), 3)

        self.assertEquals('123456', page_json['color'])
