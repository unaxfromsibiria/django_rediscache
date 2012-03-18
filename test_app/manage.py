#!/usr/bin/env python
import os, sys

if __name__ == "__main__":
    from ConfigParser import SafeConfigParser
    parser = SafeConfigParser()
    parser.read('/etc/django_rediscache.conf')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",  parser.get('uwsgi','django_settings') )
    del parser
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
