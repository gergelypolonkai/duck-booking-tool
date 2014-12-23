from django.shortcuts import render, get_object_or_404

from booking.models import Duck

def duck_comp_list(request, duck_id):
    duck = get_object_or_404(Duck, pk = duck_id)

    context = {
        'duck': duck
    }

    return render(request, 'api/duck_comp_list.json', context)
