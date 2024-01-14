import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
app = Celery("server")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "get-headers": {
        "task": "server.tasks.get_headers",
        "schedule": 86400,
    },
}
