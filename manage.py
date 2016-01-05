#!/usr/bin/env python
import os
import sys

from mongoengine import connect

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cub.settings")

    if 'runserver' in sys.argv or 'shell' in sys.argv:
        from cub.settings import MONGO_CONFIG
        connect(MONGO_CONFIG['NAME'], host=MONGO_CONFIG['HOST'],
            username=MONGO_CONFIG['USER'], password=MONGO_CONFIG['PASSWORD'],
            port=MONGO_CONFIG['PORT'])

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
