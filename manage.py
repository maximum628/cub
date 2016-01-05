#!/usr/bin/env python
import os
import sys

from mongoengine import connect

from cub.settings import MONGO_CONFIG

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cub.settings")

    connect(MONGO_CONFIG['NAME'], host=MONGO_CONFIG['HOST'])

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
