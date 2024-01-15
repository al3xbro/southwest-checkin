from django.http import HttpResponse
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
