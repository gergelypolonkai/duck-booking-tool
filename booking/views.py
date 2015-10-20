# -*- coding: utf-8
"""
Views for the Duck Booking Tool frontend
"""

from django.views import generic

from .models import Duck

class DuckListView(generic.ListView):
    """
    View for duck listing (the main page)
    """

    template_name = 'booking/duck_list.html'
    context_object_name = 'duck_list'

    def get_queryset(self):
        return Duck.objects.all()
