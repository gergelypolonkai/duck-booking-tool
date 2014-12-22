from django.db import models
from django.contrib.auth.models import User

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
