# -*- coding: utf-8 -*-
"""
Tests for the Duck Booking Tool frontend
"""

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.utils import timezone

from .ducklevel import level_to_up_minutes, level_to_down_minutes, minutes_to_level
from .templatetags import booking_tags
from .models import Duck, Competence, DuckCompetence, Species, Location, Booking

class FrontTest(TestCase):
    """
    Test case for the front end
    """

    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        """
        Test for the existence of the main page
        """

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_vocabulary_page(self):
        """
        Test for the existence of the vocabulary page
        """

        response = self.client.get('/vocabulary.html')
        self.assertEqual(response.status_code, 200)

    def test_terms_page(self):
        """
        Test for the existence of the terms page
        """

        response = self.client.get('/terms.html')
        self.assertEqual(response.status_code, 200)

    def test_disclaimer_page(self):
        """
        Test for the existence of the disclaimer page
        """

        response = self.client.get('/disclaimer.html')
        self.assertEqual(response.status_code, 200)

class DuckCompLevelTest(TestCase):
    """
    Test case for competence level calculation
    """

    def setUp(self):
        user = User.objects.create_user(username='test', password='test')

        species = Species.objects.create(name='test species')

        location = Location.objects.create(name='test location')

        duck = Duck.objects.create(species=species,
                                   location=location,
                                   donated_by=user)

        comp = Competence.objects.create(name='testing',
                                         added_by=user)

        self.duckcomp = DuckCompetence.objects.create(duck=duck,
                                                      comp=comp,
                                                      up_minutes=0,
                                                      down_minutes=0)

    def test_sane_max(self):
        """
        Test if the MAX_DUCK_LEVEL setting has a sane value
        """

        self.assertGreater(
            settings.MAX_DUCK_LEVEL, 0,
            msg="MAX_DUCK_LEVEL must be greater than zero!")

    def test_max_minutes(self):
        """
        Test if level can not go above settings.MAX_DUCK_LEVEL)
        """

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
        """
        Test minutes to level conversations
        """

        for i in range(1, settings.MAX_DUCK_LEVEL):
            up_minutes = level_to_up_minutes(i)
            down_minutes = level_to_down_minutes(i)

            up_level = minutes_to_level(up_minutes, 0)
            down_level = minutes_to_level(0, down_minutes)

            self.assertEqual(up_level, i, msg="Test failed for value %d" % i)
            self.assertEqual(
                down_level, i,
                msg="Test failed for value %d" % i)

    def test_level_to_minutes(self):
        """
        Test level to minutes conversations
        """

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

    def test_no_comp(self):
        """
        Test if level equals 0 if minutes count is 0
        """

        self.duckcomp.up_minutes = 0
        self.duckcomp.down_minutes = 0
        self.assertEquals(self.duckcomp.level(), 0)

    def test_comp_levels(self):
        """
        Test competence level calculation
        """

        self.duckcomp.down_minutes = 0

        for lvl in range(1, settings.MAX_DUCK_LEVEL):
            minutes = level_to_up_minutes(lvl)
            self.duckcomp.up_minutes = minutes
            self.assertEqual(self.duckcomp.level(), lvl)

    def test_high_minutes(self):
        """
        Test duck level calculation with a very high amount of minutes
        """

        self.duckcomp.up_minutes = level_to_up_minutes(settings.MAX_DUCK_LEVEL)
        self.duckcomp.down_minutes = level_to_down_minutes(settings.MAX_DUCK_LEVEL)
        self.assertEqual(self.duckcomp.level(), settings.MAX_DUCK_LEVEL)

class DuckAgeTest(TestCase):
    """
    Tests related to duck age
    """

    def test_duck_is_from_the_future(self):
        """
        Test if the duck came from the future (ie. donation time is in
        the future)
        """

        future_duck = Duck(donated_at=timezone.now() + datetime.timedelta(days=2))
        self.assertEqual(future_duck.age(), -1)

    def test_duck_age_formatter(self):
        """
        Test duck age formatter
        """

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

class BookingTimeTest(TestCase):
    """
    Test case for calculating booking time and popularity
    """

    def setUp(self):
        user = User()
        user.save()

        species = Species.objects.create(name='duck')
        location = Location.objects.create(name='start')

        self.duck1 = Duck.objects.create(species=species,
                                         location=location,
                                         donated_by=user)

        competence = Competence.objects.create(name='test',
                                               added_by=user)

        now = timezone.now()
        Booking.objects.create(duck=self.duck1,
                               start_ts=now - datetime.timedelta(days=2),
                               end_ts=now - datetime.timedelta(days=1),
                               user=user,
                               comp_req=competence)

        self.duck2 = Duck.objects.create(species=species,
                                         location=location,
                                         donated_by=user)

        Booking.objects.create(duck=self.duck2,
                               start_ts=now - datetime.timedelta(days=3),
                               end_ts=now - datetime.timedelta(days=2),
                               user=user,
                               comp_req=competence)

        Booking.objects.create(duck=self.duck2,
                               start_ts=now - datetime.timedelta(days=2),
                               end_ts=now - datetime.timedelta(days=1),
                               user=user,
                               comp_req=competence)

    def test_total_booking_time(self):
        """
        Test total booking time
        """

        self.assertEqual(259200, Booking.total_booking_time())

    def test_duck_booking_time(self):
        """
        Test duck booking time
        """

        self.assertEqual(86400, Booking.duck_booking_time(self.duck1))
        self.assertEqual(172800, Booking.duck_booking_time(self.duck2))

    def test_dpx(self):
        """
        Test Duck Popularity indeX calculation
        """

        self.assertEqual(1/3, self.duck1.dpx())
        self.assertEqual(2/3, self.duck2.dpx())

class TestListing(TestCase):
    """
    Test case for duck listing
    """

    def setUp(self):
        self.client = Client()

        species = Species.objects.create()
        loc = Location.objects.create()
        user = User.objects.create_user(username='test',
                                        password='test')

        self.duck = Duck.objects.create(species=species,
                                        location=loc,
                                        donated_by=user)

    def test_front_page(self):
        """
        Test existence of the front page
        """

        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

        self.assertEqual(1, len(response.context['duck_list']))

class SimilarCompTest(TestCase):
    """
    Test case for competence name fuzzy search
    """

    def setUp(self):
        admin = User.objects.create_user(username='admin',
                                         password='test')

        competence_list = (
            'Creativity',
            'Administration',
            'Perl',
            'Python',
            'TCSH',
        )

        for competence in competence_list:
            Competence.objects.create(name=competence,
                                      added_by=admin)

    def test_good_similar_competences(self):
        """
        Test similar competence list with different inputs
        """

        comp_list = Competence.get_similar_comps('perl')
        self.assertEquals(1, len(comp_list))

        comp_list = Competence.get_similar_comps('pzthon')
        self.assertEquals(1, len(comp_list))

        comp_list = Competence.get_similar_comps(u'kreativitás')
        self.assertEqual(1, len(comp_list))

    def test_bad_similar_competence(self):
        """
        Test similar competence list with a totally new and unmatching
        competence name
        """

        comp_list = Competence.get_similar_comps('development')
        self.assertEqual(0, len(comp_list))

class BookingTest(TestCase):
    """
    Test duck booking functionality
    """

    def setUp(self):
        self.spec = Species.objects.create(name='test')
        self.loc = Location.objects.create(name='test')
        self.user = User.objects.create_user(username='test')
        self.booked_duck = Duck.objects.create(species=self.spec,
                                               location=self.loc,
                                               donated_by=self.user)
        self.comp = Competence.objects.create(name='test',
                                              added_by=self.user)

        Booking.objects.create(duck=self.booked_duck,
                               user=self.user,
                               comp_req=self.comp)

    def test_booked_duck(self):
        """
        Test if booked duck returns the booking user from booked_by()
        """

        self.assertNotEqual(self.booked_duck.booked_by(), None)

    def test_unbooked_duck(self):
        """
        Test if unbooked duck returns None from booked_by()
        """

        unbooked_duck = Duck.objects.create(species=self.spec,
                                            location=self.loc,
                                            donated_by=self.user)
        self.assertEqual(unbooked_duck.booked_by(), None)

    def test_multiple_booking(self):
        """
        Test error presence in case of multiple bookings for the same
        duck
        """

        Booking.objects.create(duck=self.booked_duck,
                               user=self.user,
                               comp_req=self.comp)

        with self.assertRaises(RuntimeError):
            self.booked_duck.booked_by()
