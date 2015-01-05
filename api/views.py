from django.shortcuts import render, get_object_or_404
from django.views import generic

from booking.models import Duck

class DuckCompListView(generic.ListView):
    template_name = 'api/duck_comp_list.json'
    context_object_name = 'comp_list'

    def get_queryset(self):
        duck_id = self.kwargs['duck_id']
        duck = get_object_or_404(Duck, pk = duck_id)

        return duck.duckcompetence_set.all()
