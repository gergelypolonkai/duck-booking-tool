# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers

from booking.models import Duck, Competence, DuckCompetence

class NamespacedSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        if not hasattr(self.Meta, 'url_namespace') or self.Meta.url_namespace is None:
            raise ImproperlyConfigured("namespace must be set!")

        self.url_namespace = self.Meta.url_namespace

        self.url_namespace = kwargs.pop('url_namespace',
                                        self.url_namespace)

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

class CompetenceSerializer(NamespacedSerializer):
    class Meta:
        url_namespace = 'api'
        model = Competence
        fields = ('url', 'name',)

class DuckCompetenceSerializer(NamespacedSerializer):
    comp = CompetenceSerializer()

    class Meta:
        url_namespace = 'api'
        model = DuckCompetence
        fields = ('comp', 'up_minutes', 'down_minutes',)

class DuckSerializer(NamespacedSerializer):
    competences = DuckCompetenceSerializer(many=True)

    class Meta:
        url_namespace = 'api'
        model = Duck
        fields = ('url', 'name', 'color', 'competences',)
