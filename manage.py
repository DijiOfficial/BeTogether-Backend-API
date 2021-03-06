#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
from decouple import config

# python3 -m pip freeze > requirements.txt when installing new packages

try:
    DB_URI = config("DB_URI")
    print("Connected successfully!!!")
except Exception as e:
    logging.critical(e, exc_info=True)
    print("Could not connect to MongoDB")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'betogetherAPI.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
