# -*- coding: utf-8 -*-
import  os,sys
from ConfigParser import SafeConfigParser
sys.path.append('/usr/local/lib/python2.7/dist-packages/django/')
sys.path.append('/data/web/django_rediscache/django_rediscache')
parser = SafeConfigParser()
parser.read('/etc/django_rediscache.conf')
os.environ['DJANGO_SETTINGS_MODULE']=parser.get('uwsgi','django_settings')
del parser
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
