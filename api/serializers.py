# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers

from booking.models import Duck

class NamespacedSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        if not hasattr(self.Meta, 'url_namespace') or self.Meta.url_namespace is None:
            raise ImproperlyConfigured("namespace must be set!")

        self.url_namespace = self.Meta.url_namespace

        if not self.url_namespace.endswith(':'):
            self.url_namespace += ':'

        return super(NamespacedSerializer, self).__init__(*args, **kwargs)

    def build_url_field(self, field_name, model_class):
        field_class, field_kwargs = super(NamespacedSerializer, self) \
                                    .build_url_field(field_name,
                                                     model_class)

        view_name = field_kwargs.get('view_name')

        if not view_name.startswith(self.url_namespace):
            field_kwargs['view_name'] = self.url_namespace + view_name

        return field_class, field_kwargs

class DuckSerializer(NamespacedSerializer):
    class Meta:
        url_namespace = 'api'
        model = Duck
        fields = ('url', 'name', 'color',)
