from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Species(models.Model):
    """Model to hold the Ducks’ species"""

    name = models.CharField(max_length = 40, unique = True)

    def __str__(self):
        return self.name

class Location(models.Model):
    """Model to hold the possible locations of the Ducks"""

    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class Competence(models.Model):
    """Model to hold Duck competences"""

    name = models.CharField(max_length = 255, unique = True)
    added_at = models.DateTimeField(default = timezone.now)
    added_by = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Duck(models.Model):
    """Model to hold Duck data"""

    name = models.CharField(max_length = 80, null = True, blank = True)
    color = models.CharField(max_length = 6)
    species = models.ForeignKey(Species)
    location = models.ForeignKey(Location)
    donated_by = models.ForeignKey(User)
    donated_at = models.DateTimeField(default = timezone.now)
    adopted_by = models.ForeignKey(User, related_name = 'adopted_ducks', null = True)
    adopted_at = models.DateTimeField(null = True)
    on_holiday_since = models.DateTimeField(null = True)
    on_holiday_until = models.DateTimeField(null = True)

    def __str__(self):
        if self.name == None or self.name == '':
            return 'Unnamed :('

        return self.name
