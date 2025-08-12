from __future__ import absolute_import
import os
from celery import Celery

# Celery app setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payment_gateway.settings')
app = Celery('payment_gateway')
app.config_from_object('django.conf:settings', namespace='CELERY')
# Auto discover all celery tasks
app.autodiscover_tasks()