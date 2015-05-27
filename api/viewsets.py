# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework import viewsets, permissions

from .serializers import DuckSerializer
from booking.models import Duck

class DuckViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Duck.objects.all()
    serializer_class = DuckSerializer
