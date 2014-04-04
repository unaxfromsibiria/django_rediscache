'''
Created on 10.03.2012

@author: unax
'''

from config import LazySettings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from queryset import get_query_set
from invalidation import CacheInvalidator
from related import CachedReverseSingleRelatedObjectDescriptor


def _foreign_key_field_setup(model):
    for (field, _) in model._meta.get_fields_with_model():
        if isinstance(field, (models.ForeignKey,)):
            setattr(
                model,
                field.name,
                CachedReverseSingleRelatedObjectDescriptor(field))


def install():
    config = LazySettings()
    if not config.create():
        return
    scheme = config.scheme
    DEBUG = settings.DEBUG
    if len(scheme) < 1:
        if DEBUG:
            print 'DJANGO_REDISCACHE not used'
        return
    from django.db.models import get_models
    for model in get_models(include_auto_created=True):
        model_path = "{0}.{1}".format(
            model.__module__, model.__name__)
        model_scheme = scheme.get(model_path)

        if isinstance(model_scheme, dict):
            setattr(
                model.objects.__class__,
                'get_query_set',
                get_query_set)
            setattr(
                model._default_manager.__class__,
                'get_query_set',
                get_query_set)
            # in new django get_query_set => get_queryset why?
            setattr(
                model.objects.__class__,
                'get_queryset',
                get_query_set)
            setattr(
                model._default_manager.__class__,
                'get_queryset',
                get_query_set)
            if isinstance(model_scheme.get('reference'), int) or isinstance(model_scheme.get('all'), int):
                _foreign_key_field_setup(model)

            post_delete.connect(CacheInvalidator.post_delete, sender=model)
            post_save.connect(CacheInvalidator.post_save, sender=model)

        if DEBUG:
            print "Cache for model {0} used: {1}".format(
                model.__name__, {True: 'on', False: 'off'}.get(
                    isinstance(model_scheme, dict)))
