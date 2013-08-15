'''
Created on 10.03.2012

@author: unax
'''

from .cache import _internal_cache as cache
from .config import SERVICE_TIME
from .misc import CacheNameMixer


def model_change(**params):
    pk = params.get('pk')
    collection = params.get('collection')
    document = params.get('document')
    if document:
        pk = document.pk
        collection = document._meta.db_table
    key = "{0}:get:{1}".format(
        collection, CacheNameMixer({'pk': pk}))
    if document:
        cache.set(key, document, SERVICE_TIME)
    if params.get('delete'):
        cache.delete(key)
    cache.incr("version:{0}".format(collection), 1)


class CacheInvalidator:
    @classmethod
    def post_save(cls, sender, **kwargs):
        instance = kwargs.get('instance')
        model_change(
            pk=instance.pk,
            collection=instance._meta.db_table,
            delete=True)

    @classmethod
    def post_delete(cls, sender, **kwargs):
        instance = kwargs.get('instance')
        model_change(
            pk=instance.pk,
            collection=instance._meta.db_table,
            delete=True)
