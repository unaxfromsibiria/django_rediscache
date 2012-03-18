'''
Created on 10.03.2012

@author: unax
'''
from django.conf import settings
from queryset import get_query_set
from django.db.models.signals import post_save, post_delete
from invalidation import model_change

def _post_save(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        model_change(instance.pk, instance._meta.db_table)

def _post_delete(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        model_change(instance.pk, instance._meta.db_table)

def install():
    if not bool(settings.DJANGO_REDISCACHE.get('used')): return
    from django.db.models import get_models
    for model in get_models(include_auto_created=True):
        scheme=settings.DJANGO_REDISCACHE.get('scheme').get(str(model.__module__).replace('models',model.__name__))
        if isinstance(scheme, dict):
            model._django_rediscache={}
            setattr(model.objects.__class__, 'get_query_set', get_query_set)
            setattr(model._default_manager.__class__, 'get_query_set', get_query_set)
            post_delete.connect(_post_delete, sender=model)
            post_save.connect(_post_save, sender=model)
