from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from booking.models import Species, Location, Duck, Competence, DuckCompetence

class ReverseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_reverse_js(self):
        response = self.client.get(reverse('api:js_reverse'))
        self.assertEqual(response.status_code, 200)

class ApiTest(TestCase):
    def setUp(self):
        self.client = Client()

        species = Species(name = 'duck')
        species.save()

        loc = Location(name = 'test')
        loc.save()

        user = User()
        user.save()

        self.duck = Duck(pk = 1, species = species, location = loc, donated_by = user)
        self.duck.save()

        comp = Competence(name = 'test', added_by = user)
        comp.save()

        duckcomp = DuckCompetence(duck = self.duck, comp = comp)
        duckcomp.save()

    def test_duck_comp_list(self):
        response = self.client.get('/api/duck/1/competence.json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['duck'].duckcompetence_set.all()), 1)
