# -*- coding: utf-8
"""
Administration site definition for the Duck Booking Tool
"""

from django.contrib import admin
from booking.models import Species, Location, Competence, Duck, \
                           Booking, DuckCompetence, DuckName, \
                           DuckNameVote

admin.site.register(Species)
admin.site.register(Location)
admin.site.register(Competence)
admin.site.register(Duck)
admin.site.register(Booking)
admin.site.register(DuckCompetence)
admin.site.register(DuckName)
admin.site.register(DuckNameVote)
