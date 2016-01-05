"""
WSGI config for cub2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cub.settings")

from cub.settings import APP_ENVIRONMENT
if APP_ENVIRONMENT == 'PROD':
    application = Cling(MediaCling(get_wsgi_application()))
else:
    application = get_wsgi_application()
