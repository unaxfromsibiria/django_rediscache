# -*- coding: utf-8 -*-
from django.conf import settings
from cache import _internal_cache
from setup import install
cache = _internal_cache

def scheme_timelimit(model, request):
    scheme=settings.DJANGO_REDISCACHE.get('scheme').get(str(model.__module__).replace('models',model.__name__))
    if scheme is None: return None
    timeout=scheme.get(request)
    if timeout is None: timeout=scheme.get('all')
    del scheme
    return timeout

install()
