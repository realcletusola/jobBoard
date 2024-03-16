from __future__ import absolute_import, unicode_literals
from celery import Celery 
import os 


# set default django settings module for celery program 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JobBoard.settings')

app = Celery('JobBoard')

# configuration object to child processes.
app.config_from_objects('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

