from django.http import HttpResponse
from django.http import JsonResponse
from django.middleware.csrf import get_token
from datetime import datetime
from . import tasks


def reserve(request):
    aware_datetime = datetime.strptime(request.POST.get(
        'dateTimeString').replace("GMT", "+00:00"), "%a, %d %b %Y %H:%M:%S %z")
    if request.method == 'POST':
        tasks.scheduler.add_job(tasks.process_reservation, 'date', misfire_grace_time=None, run_date=aware_datetime, args=(
            request.POST.get('firstName'),
            request.POST.get('lastName'),
            request.POST.get('confirmation'),
            request.POST.get('email')
        ))
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'token': csrf_token})