# -*- coding: utf-8
"""
URL definitions for version 1 of the Duck Booking Tool API
"""

from rest_framework import routers

from . import views

rest_router = routers.DefaultRouter()
rest_router.register(r'ducks', views.DuckViewSet)
rest_router.register(r'competences', views.CompetenceViewSet)

urlpatterns = rest_router.urls
