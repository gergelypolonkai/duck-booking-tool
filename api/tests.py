# -*- coding: utf-8
"""
Test cases for API calls
"""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, RequestFactory
from django_webtest import WebTest

import json

from .serializers import NamespacedSerializer
from booking.ducklevel import level_to_up_minutes
from booking.models import Species, Location, Duck, Competence, DuckCompetence

class MetalessNamespacedSerializer(NamespacedSerializer):
    pass

class MissingNamespacedSerializer(NamespacedSerializer):
    class Meta:
        pass

class NoneNamespacedSerializer(NamespacedSerializer):
    class Meta:
        url_namespace = None

class EmptyNamespacedSerializer(NamespacedSerializer):
    class Meta:
        url_namespace = ''

class TestNamespacedSerializer(TestCase):
    """
    Test namespaced Serializer
    """

    def test_no_namespace(self):
        with self.assertRaises(ImproperlyConfigured):
            serializer = MetalessNamespacedSerializer()

        with self.assertRaises(ImproperlyConfigured):
            serializer = MissingNamespacedSerializer()

        with self.assertRaises(ImproperlyConfigured):
            serializer = NoneNamespacedSerializer()

        with self.assertRaises(ImproperlyConfigured):
            serializer = EmptyNamespacedSerializer()

    def test_namespacing(self):
        class MySerializer(NamespacedSerializer):
            class Meta:
                model = Competence
                fields = ('url',)
                url_namespace = 'api'

        competence = Competence.objects.create(
            added_by=User.objects.create())
        serializer = MySerializer(competence,
                                  context={
                                      'request': RequestFactory().get('/')
                                  })

        self.assertIsNotNone(serializer.data['url'])

class DuckClassTest(WebTest):
    """
    Test case for duck related API calls
    """

    csrf_checks = False

    def setUp(self):
        good_minutes = level_to_up_minutes(settings.COMP_WARN_LEVEL + 1)
        bad_minutes = level_to_up_minutes(settings.COMP_WARN_LEVEL)

        self.user = User.objects.create_user(username='test',
                                             password='test')

        self.species = Species.objects.create(name='duck')
        self.location = Location.objects.create(name='temp')
        self.comp_bad = Competence.objects.create(name='test1',
                                                  added_by=self.user)
        self.comp_good = Competence.objects.create(name='test2',
                                                   added_by=self.user)
        self.duck = Duck.objects.create(species=self.species,
                                        name='test duck',
                                        location=self.location,
                                        donated_by=self.user,
                                        color='123456')

        DuckCompetence.objects.create(duck=self.duck,
                                      comp=self.comp_bad,
                                      up_minutes=bad_minutes,
                                      down_minutes=0)

        DuckCompetence.objects.create(duck=self.duck,
                                      comp=self.comp_good,
                                      up_minutes=good_minutes,
                                      down_minutes=0)

    def test_book_nonlogged(self):
        """
        Test booking without logging in
        """

        page = self.app.post('/api/v1/ducks/1/book/', expect_errors=True)
        self.assertEqual(page.status_code, 403)

    def test_book_nonexist(self):
        """
        Test booking a non-existing duck
        """

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
        """
        Test duck booking for a competence the duck is not good at
        """

        url = '/api/v1/ducks/%d/book/' % self.duck.pk
        comp_none = Competence.objects.create(name='test3',
                                              added_by=self.user)

        # Book for a competence the duck doesn’t have at all
        test_data = {
            'competence': comp_none.pk,
        }

        page = self.app.post(url, params=test_data, user=self.user)
        self.assertEquals(200, page.status_code)

        page_json = json.loads(page.content)
        self.assertEquals(page_json['status'], 'bad-comp')

        # Book for a competence with low level
        test_data = {
            'competence': self.comp_bad.pk,
        }

        page = self.app.post(url, params=test_data, user=self.user)
        self.assertEquals(200, page.status_code)

        page_json = json.loads(page.content)
        self.assertEquals(page_json['status'], 'bad-comp')

        # Forcibly book for a competence with low level
        test_data['force'] = 1

        page = self.app.post(url, params=test_data, user=self.user)
        self.assertEqual(200, page.status_code)

        page_json = json.loads(page.content)
        self.assertEquals(page_json['status'], 'ok')

    def test_book_good(self):
        """
        Test duck booking for a competence the duck is good at
        """

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

    def test_incomplete_donation(self):
        """
        Test duck donation with incomplete data
        """

        params = {
            # No parameters
            'none': '',
            # Empty parameter set
            'empty': {},
            # Species omitted
            'species-omit': {
                'location': self.location.pk,
                'color': '123456',
            },
            # Missing species
            'species-notfound': {
                'location': self.location.pk,
                'species': 9999,
                'color': '123456',
                'expected-code': 404,
                'expected-error': 'bad-species',
            },
            # Location omitted
            'location-omit': {
                'species': self.species.pk,
                'color': '123456',
            },
            # Missing location
            'location-notfound': {
                'location': 9999,
                'species': self.species.pk,
                'color': '123456',
                'expected-code': 404,
                'expected-error': 'bad-location',
            },
            # Color omitted
            'color-omit': {
                'location': self.location.pk,
                'species': self.species.pk,
            },
            # Invalid color
            'color-invalid': {
                'location': self.location.pk,
                'species': self.species.pk,
                'color': 'red',
                'expected-error': 'bad-color',
                'expected-code': 400,
            },
        }

        url = '/api/v1/ducks/donate/'

        for name, param in params.items():
            if param == '':
                expected_code = 400
                expected_error = 'incomplete-request'
            else:
                expected_code = param.pop('expected-code', 400)
                expected_error = param.pop('expected-error',
                                           'incomplete-request')

            page = self.app.post(url,
                               params=param,
                               expect_errors=True,
                               user=self.user)

            self.assertEquals(
                expected_code,
                page.status_code,
                msg="Got unexpected status code ({}) for parameter set {}".format(
                    page.status_code,
                    name))
            page_json = json.loads(page.content)

            self.assertEquals(
                expected_error,
                page_json['status'],
                msg="Got unexpected status code ({}) for parameter set {}".format(
                    page.status_code,
                    name))

    def test_duck_donation(self):
        """
        Test duck donating functionality
        """

        # Duck donation should not be allowed without logging in
        page = self.app.get('/api/v1/ducks/donate/', expect_errors=True)
        self.assertEquals(page.status_code, 403)

        # Duck donation should not be allowed withoud logging in
        page = self.app.post('/api/v1/ducks/donate/', expect_errors=True)
        self.assertEquals(page.status_code, 403)

        color = '123456'
        page = self.app.post(
            '/api/v1/ducks/donate/',
            params={
                'species': self.species.pk,
                'location': self.location.pk,
                'color': color,
            },
            user=self.user)
        self.assertEquals(200, page.status_code)
        page_json = json.loads(page.content)

        self.assertIn('id', page_json)

        duck = Duck.objects.get(pk=page_json['id'])

        self.assertEquals(color, duck.color)

    def test_duck_details(self):
        """
        Test duck details view
        """

        url = '/api/v1/ducks/%d/' % self.duck.pk
        page = self.app.get(url)
        self.assertEqual(200, page.status_code)

        page_json = json.loads(page.content)

        self.assertEquals('test duck', page_json['name'])
        self.assertEquals('123456', page_json['color'])
        self.assertEqual(2, len(page_json['competences']))
