from django.db import models

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
