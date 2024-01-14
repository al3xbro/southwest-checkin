from django.http import HttpResponse
from . import tasks


def reserve(request):
    if request.method == 'POST':
        tasks.process_reservation(
            request.POST.get('firstName'),
            request.POST.get('lastName'),
            request.POST.get('confirmation'),
            request.POST.get('email')
        )
        # add to queue
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
