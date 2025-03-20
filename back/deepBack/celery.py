from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deepBack.settings")

app = Celery("deepBack")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.broker_url = f"redis://:{os.getenv('REDIS_PASSWORD')}@redis:6379/0"
app.conf.result_backend = f"redis://:{os.getenv('REDIS_PASSWORD')}@redis:6379/0"

app.conf.beat_schedule = {
    "send_newsletter_every_two_weeks": {
        "task": "app.tasks.send_newsletter",
        "schedule": timedelta(weeks=2),
    },
}
