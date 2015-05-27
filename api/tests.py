from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.conf import settings

import json

from booking.ducklevel import level_to_up_minutes
from booking.models import Species, Location, Duck, Competence, DuckCompetence

def get_response_encoding(response):
    encoding = settings.DEFAULT_CHARSET

    if response.has_header('content-encoding'):
        encoding = response['content-encoding']

    return encoding

class ApiTest(TestCase):
    def setUp(self):
        self.client = Client()

        species = Species(name = 'duck')
        species.save()

        loc = Location(name = 'test')
        loc.save()

        user = User()
        user.save()

        self.duck = Duck(
            species = species,
            location = loc,
            donated_by = user)
        self.duck.save()

        comp = Competence(name = 'test', added_by = user)
        comp.save()

        duckcomp = DuckCompetence(duck = self.duck, comp = comp)
        duckcomp.save()

    def test_duck_comp_list(self):
        response = self.client.get('/api/duck/1/competence.json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['comp_list']), 1)

class DuckBookingTest(TestCase):
    username = 'admin'
    password = 'password'

    def setUp(self):
        good_minutes = level_to_up_minutes(settings.COMP_WARN_LEVEL + 1)
        bad_minutes = level_to_up_minutes(settings.COMP_WARN_LEVEL)
        self.duck_id = 1
        self.comp_id = 1

        self.admin = User.objects.create_user(
            username = self.username,
            password = self.password)
        self.admin.save()

        spec = Species(name = 'duck')
        spec.save()

        loc = Location(name = 'temp')
        loc.save()

        self.comp_bad = Competence(
            pk = self.comp_id,
            name = 'test1',
            added_by = self.admin)
        self.comp_id += 1
        self.comp_bad.save()

        self.comp_good = Competence(
            pk = self.comp_id,
            name = 'test2',
            added_by = self.admin)
        self.comp_id += 1
        self.comp_good.save()

        self.duck = Duck(
            pk = self.duck_id,
            species = spec,
            location = loc,
            donated_by = self.admin)
        self.duck_id += 1
        self.duck.save()

        dcomp = DuckCompetence(
            duck = self.duck,
            comp = self.comp_bad,
            up_minutes = bad_minutes,
            down_minutes = 0)
        dcomp.save()

        dcomp = DuckCompetence(
            duck = self.duck,
            comp = self.comp_good,
            up_minutes = good_minutes,
            down_minutes = 0)
        dcomp.save()

        self.client = Client()

    def send_booking_json(self, json_data):
        return self.client.post(
            '/api/duck/book/',
            json.dumps(json_data),
            HTTP_X_REQUESTED_WITH = 'XMLHttpRequest',
            content_type = 'application/json')

    def test_book_nonlogged(self):
        self.client.logout()

        response = self.send_booking_json({
            "duck_id": self.duck.pk,
            "comp_id": self.comp_good.pk
        })

        self.assertEqual(response.status_code, 401)

    def test_book_nonexist(self):
        self.client.login(username = self.username, password = self.password)

        # Try to book a non-existing Duck
        response = self.send_booking_json({
            "duck_id": self.duck.pk + 1,
            "comp_id": self.comp_good.pk
        })
        self.assertEqual(response.status_code, 404)

        # Try to book an existing Duck for a non-existing competence
        response = self.send_booking_json({
            "duck_id": self.duck.pk,
            "comp_id": 3
        })
        self.assertEqual(response.status_code, 404)

    def test_book_warn(self):
        test_data = {
            "duck_id": self.duck.pk,
            "comp_id": self.comp_bad.pk
        }
        self.client.login(username = self.username, password = self.password)

        response = self.send_booking_json(test_data)
        self.assertEqual(response.status_code, 200)

        j = json.loads(response.content.decode(get_response_encoding(response)))
        self.assertIn('success', j)
        self.assertEquals(j['success'], 1)

        test_data['force'] = 1

        response = self.send_booking_json(test_data)
        self.assertEqual(response.status_code, 200)

        j = json.loads(response.content.decode(get_response_encoding(response)))
        self.assertIn('success', j)
        self.assertEquals(j['success'], 2)

    def test_book_good(self):
        test_data = {
            "duck_id": self.duck.pk,
            "comp_id": self.comp_good.pk
        }
        self.client.login(username = self.username, password = self.password)

        # Book the duck
        response = self.send_booking_json(test_data)
        self.assertEqual(response.status_code, 200)

        j = json.loads(response.content.decode(get_response_encoding(response)))
        self.assertIn('success', j)
        self.assertEqual(j['success'], 2)

        # Try to book again, it should fail
        response = self.send_booking_json(test_data)
        self.assertEqual(response.status_code, 200)

        j = json.loads(response.content.decode(get_response_encoding(response)))
        self.assertIn('success', j)
        self.assertEqual(j['success'], 0)
