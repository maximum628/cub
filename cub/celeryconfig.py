from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cub.settings')

from django.conf import settings

app = Celery('cub', broker=settings.MONGO_CONFIG['HOST'])
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
