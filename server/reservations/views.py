import json
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from . import tasks


def reserve(request):
    req = json.loads(request.body)
    aware_datetime = datetime.strptime(req.get(
        'dateTimeString').replace("GMT", "+00:00"), "%a, %d %b %Y %H:%M:%S %z")
    if request.method == 'POST':
        tasks.scheduler.add_job(tasks.process_reservation, 'date', misfire_grace_time=None, run_date=aware_datetime, args=(
            req.get('firstName'),
            req.get('lastName'),
            req.get('confirmation'),
            req.get('email')
        ))
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)