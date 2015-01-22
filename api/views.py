from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.conf import settings
from django.views.decorators.http import require_POST

import json

from booking.models import Duck, Booking, Competence

class DuckCompListView(generic.ListView):
    template_name = 'api/duck_comp_list.json'
    context_object_name = 'comp_list'

    def get_queryset(self):
        duck_id = self.kwargs['duck_id']
        duck = get_object_or_404(Duck, pk = duck_id)

        return duck.duckcompetence_set.all()

@require_POST
def duck_book(request):
    """Book a duck to the logged in user.

    Return value:
    HttpResponse with status_code = 400 if response.jsondata misses
                                        duck_id or comp_id
    HttpResponse with status_code = 401 if the user is not authenticated
    HttpResponse with status_code = 404 if the duck or comp is not found
    response.jsondata.success = 0 if the duck is already booked
    response.jsondata.success = 1 if the duck's competence is too low
                                  (use request.jsondata.force = True
                                  to force)
    response.jsondata.success = 2 if the booking was successful"""

    user = request.user

    # Check if user is authenticated; if not, return HTTP 401
    if not user.is_authenticated():
        res = HttpResponse()
        res.status_code = 401

        return res

    # Decode the request body
    encoding = settings.DEFAULT_CHARSET if request.encoding == None else request.encoding
    json_content = request.body.decode(encoding)
    j = json.loads(json_content)

    # If there is no duck_id or no comp_id in the request, return HTTP 400
    if 'duck_id' not in  j or 'comp_id' not in j:
        res = HttpResponse()
        res.status_code = 400

        return res

    duck_id = j['duck_id']
    comp_id = j['comp_id']

    # Find the duck and the competence; if any of them non-existant,
    # return HTTP 404
    duck = get_object_or_404(Duck, pk = duck_id)
    comp = get_object_or_404(Competence, pk = comp_id)

    # If the duck is already booked, return 0 as the result
    if duck.booked_by() != None:
        return JsonResponse({'success': 0})

    # Result 0 means a problem
    result = 0
    comp_level = 0

    # Check if the duck has the requested competence
    dcomp_list = duck.duckcompetence_set.filter(comp = comp)

    if len(dcomp_list) < 1:
        comp_level = 0
    else:
        comp_level = dcomp_list[0].level()

    # If the competence level is too low, set result to 1
    if comp_level <= settings.COMP_WARN_LEVEL:
        result = 1

    # If the duck has high enough competence or the booking is forced,
    # return success (2)
    if result != 1 or 'force' in j:
        result = 2

        booking = Booking(duck = duck, user = user, comp_req = comp)
        booking.save()

    return JsonResponse({'success': result})
