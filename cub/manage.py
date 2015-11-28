#!/usr/bin/env python
import os
import sys

from mongoengine import connect

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cub.settings")

    from django.core.management import execute_from_command_line

    if 'runserver' in sys.argv or 'shell' in sys.argv:
        connect('cub')

    execute_from_command_line(sys.argv)
