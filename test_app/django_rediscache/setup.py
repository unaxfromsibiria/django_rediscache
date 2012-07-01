'''
Created on 10.03.2012

@author: unax
'''
from queryset import get_query_set
from django.db.models.signals import post_save, post_delete
from invalidation import model_change
from config import get_scheme, is_userd

def _post_save(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        model_change(instance.pk, instance._meta.db_table)

def _post_delete(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        model_change(instance.pk, instance._meta.db_table)

def install():
    if not is_userd():
        return
    from django.db.models import get_models
    for model in get_models(include_auto_created=True):
        scheme=get_scheme(model)
        if isinstance(scheme, dict):
            model._django_rediscache={}
            setattr(model.objects.__class__, 'get_query_set', get_query_set)
            setattr(model._default_manager.__class__, 'get_query_set', get_query_set)
            post_delete.connect(_post_delete, sender=model)
            post_save.connect(_post_save, sender=model)
