from django.shortcuts import render
from django.views import generic

from .models import Duck

class DuckListView(generic.ListView):
    template_name = 'booking/duck_list.html'
    context_object_name = 'duck_list'

    def get_queryset(self):
        return Duck.objects.all()
