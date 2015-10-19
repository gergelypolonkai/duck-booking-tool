# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import DuckSerializer, CompetenceSerializer
from booking.models import Duck, Competence, Booking

class DuckViewSet(viewsets.ModelViewSet):
    serializer_class = DuckSerializer
    queryset = Duck.objects.all()

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        duck = self.get_object()
        competence = get_object_or_404(Competence, pk=request.data['competence'])
        force = request.data.get('force', False)

        # If the duck is already booked, return 'already-booked' as the
        # result
        if duck.booked_by() != None:
            return Response({'status': 'already-booked'})

        # Result 'fail' means a problem
        result = 'fail'
        comp_level = 0

        # Check if the duck has the requested competence
        dcomp_list = duck.duckcompetence_set.filter(comp=competence)

        if len(dcomp_list) < 1:
            comp_level = 0
        else:
            comp_level = dcomp_list[0].level()

        # If the competence level is too low, set result to 'bad-comp'
        if comp_level <= settings.COMP_WARN_LEVEL:
            result = 'bad-comp'

        # If the duck has high enough competence or the booking is
        # forced, return status 'success'
        if result != 'bad-comp' or force:
            result = 'ok'

            booking = Booking(duck=duck, user=request.user, comp_req=competence)
            booking.save()

        return Response({'status': result})

    @list_route(methods=['post'], permission_classes=[IsAuthenticated])
    def donate(self, request):
        return Response({'Woot!'})
