# -*- coding: utf-8 -*-
"""
Models for the Duck Booking Tool
"""

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from fuzzywuzzy import fuzz

from .ducklevel import minutes_to_level

@python_2_unicode_compatible
class Species(models.Model):
    """
    Model to hold the Ducks’ species
    """

    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Location(models.Model):
    """
    Model to hold the possible locations of the Ducks
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Competence(models.Model):
    """
    Model to hold Duck competences
    """

    name = models.CharField(max_length=255, unique=True)
    added_at = models.DateTimeField(default=timezone.now)
    added_by = models.ForeignKey(User)

    def __str__(self):
        return self.name

    @classmethod
    def get_similar_comps(cls, name):
        """
        Get competence names similar to name
        """

        comps = cls.objects.values_list('name', flat=True)
        ret = ()

        for competence in comps:
            similarity = fuzz.ratio(name.lower(), competence.lower())

            # This ratio is subject to change
            if similarity > settings.MIN_FUZZY_SIMILARITY:
                ret = ret + (competence,)

        return ret

@python_2_unicode_compatible
class Duck(models.Model):
    """
    Model to hold Duck data
    """

    name = models.CharField(max_length=80, null=True, blank=True)
    color = models.CharField(max_length=6)
    species = models.ForeignKey(Species)
    location = models.ForeignKey(Location)
    comps = models.ManyToManyField(Competence, through='DuckCompetence')
    donated_by = models.ForeignKey(User)
    donated_at = models.DateTimeField(default=timezone.now)
    adopted_by = models.ForeignKey(User, related_name='adopted_ducks', null=True, blank=True)
    adopted_at = models.DateTimeField(null=True, blank=True)
    bookings = models.ManyToManyField(User, through='Booking', related_name='+')
    on_holiday_since = models.DateTimeField(null=True, blank=True)
    on_holiday_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.name == None or self.name == '':
            return 'Unnamed :('

        return self.name

    def age(self):
        """
        Get the age of the duck (time since the duck has been registered
        in the tool)
        """

        seconds_d = timezone.now() - self.donated_at
        seconds = seconds_d.total_seconds()

        if seconds < 0:
            return -1

        return seconds

    def dpx(self):
        """
        Get the Duck Popularity indeX for this duck
        """

        all_time = Booking.total_booking_time()
        duck_time = Booking.duck_booking_time(self)

        if (all_time == None) or (duck_time == None):
            return 0

        return Booking.duck_booking_time(self) / Booking.total_booking_time()

    def booked_by(self):
        """
        Get the user who is currently using the duck
        """

        booking_list = self.booking_set.filter(end_ts=None)

        if len(booking_list) == 0:
            return None

        if len(booking_list) > 1:
            raise RuntimeError(u"Duck is booked more than once!")

        return booking_list[0].user

@python_2_unicode_compatible
class DuckName(models.Model):
    """
    Model to hold name suggestions for Ducks
    """

    duck = models.ForeignKey(Duck)
    name = models.CharField(max_length=60)
    suggested_by = models.ForeignKey(User)
    suggested_at = models.DateTimeField(default=timezone.now)
    closed_by = models.ForeignKey(User, related_name='+')
    closed_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{0}, suggested by {1}".format(self.name,
                                              self.suggested_by)

@python_2_unicode_compatible
class DuckNameVote(models.Model):
    """
    Model to hold votes to Duck names
    """

    duck_name = models.ForeignKey(DuckName)
    vote_timestamp = models.DateTimeField(default=timezone.now)
    voter = models.ForeignKey(User)
    upvote = models.BooleanField(default=True)

    def __str__(self):
        return "{0} voted {1} for {2}".format(self.voter,
                                              "up" if upvote else "down",
                                              self.duck_name)

@python_2_unicode_compatible
class DuckCompetence(models.Model):
    """
    Duck competence governor table
    """

    duck = models.ForeignKey(Duck, related_name='competences')
    comp = models.ForeignKey(Competence, related_name='ducks')
    up_minutes = models.IntegerField(default=0)
    down_minutes = models.IntegerField(default=0)

    def level(self):
        """
        Return the actual level of a duck
        """

        return minutes_to_level(self.up_minutes, self.down_minutes)

    def __str__(self):
        return "{0} with +{1}/-{2} minutes in {3}".format(self.duck,
                                                          self.up_minutes,
                                                          self.down_minutes,
                                                          self.comp)

    class Meta:
        unique_together = ('duck', 'comp')

@python_2_unicode_compatible
class Booking(models.Model):
    """
    Duck booking governor table
    """

    duck = models.ForeignKey(Duck)
    user = models.ForeignKey(User)
    comp_req = models.ForeignKey(Competence)
    start_ts = models.DateTimeField(default=timezone.now)
    end_ts = models.DateTimeField(null=True, blank=True)
    successful = models.BooleanField(default=True)

    @classmethod
    def total_booking_time(cls):
        """
        Get the sum of booked hours for all ducks
        """

        return cls.objects.filter(
            start_ts__isnull=False,
            end_ts__isnull=False).extra(
                select={
                    'amount': 'sum(strftime(%s, end_ts) - strftime(%s, start_ts))'
                },
                select_params=('%s', '%s'))[0].amount

    @classmethod
    def duck_booking_time(cls, duck):
        """
        Get the sum of booked hours of a duck
        """

        return cls.objects.filter(
            start_ts__isnull=False,
            end_ts__isnull=False, duck=duck).extra(
                select={
                    'amount': 'sum(strftime(%s, end_ts) - strftime(%s, start_ts))'
                },
                select_params=('%s', '%s'))[0].amount

    def __str__(self):
        return "{0} booked by {1} since {2}".format(self.duck,
                                                    self.user,
                                                    self.start_ts)
