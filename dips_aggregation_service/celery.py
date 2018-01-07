import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dips_aggregation_service.settings')

app = Celery('dips_aggregation_service')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
