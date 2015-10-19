# -*- coding: utf-8 -*-
from rest_framework import serializers

from booking.models import Duck

class DuckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Duck
        fields = ('url', 'name', 'color',)
        extra_kwargs = {
            'url': {
                'view_name': 'api:duck-detail',
            }
        }
