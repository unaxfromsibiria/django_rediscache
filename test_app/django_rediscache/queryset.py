'''
Created on 06.03.2012

@author: unax
'''
from django.db import models
from misc import CacheNameMixer
from helper import _queryset_list, SecondaryKey
from invalidation import model_change
from django.db.models.query import QuerySet
from cache import _cache as cache
from config import LazySettings, ABSOLUTE_VERSION_LIMIT

class CachedQuerySet(QuerySet):
    __cache_scheme = None
    __table = None

    def __init__(self, model=None, query=None, using=None):
        QuerySet.__init__(self, model, query, using)
        self.__cache_scheme = LazySettings().scheme.get("%s.%s" % (model.__module__, model.__name__))
        self.__table = self.model._meta.db_table

    @property
    def cache_scheme(self):
        return self.__cache_scheme
    
    @property
    def cache_version(self):
        version = cache.get_int("version:%s" % self.__table)
        if not isinstance(version, int) or version > ABSOLUTE_VERSION_LIMIT:
            version = 1
            cache.set_int("version:%s" % self.__table,
                          version,
                          max([ v for k, v in self.__cache_scheme.iteritems() ]) + 1)
        return version

    def _timeout(self, operation):
        return self.__cache_scheme.get(operation)
    
    @property
    def core_cache_name(self):
        return str(CacheNameMixer({'sql' : str(self.query)}))

    @property
    def cache(self):
        timeout = self.cache_scheme.get('list')
        if isinstance(timeout, int):
            core = (self.__table, self.core_cache_name)
            cache_key = "%s:list:%s" % core
            version = cache.get_int("version:%s:%s" % core)
            if isinstance(version, int):
                v = self.cache_version
                cached_list = cache.get(cache_key)
            else:
                v = None
                cached_list = None

            if isinstance(cached_list, list) and version == v:
                del cache_key
                return _queryset_list(cache.pipeline_get(cached_list))
            else:
                # creating cache
                if self.count() > 0:
                    keys = list()
                    for obj in self:
                        obj_cache_key = "%s:get:%s" % (self.__table, CacheNameMixer({ 'pk' : obj.pk }))
                        keys.append(obj_cache_key)
                        cache.set(obj_cache_key, obj, timeout)
                    cache.set(cache_key, keys, timeout - 1)
                    cache.set_int("version:%s:%s" % core, self.cache_version, timeout - 1)
                del cache_key
        return self

    def exists(self):
        timeout = self._timeout('count')
        if isinstance(timeout, int):
            return self.count() > 0
        return QuerySet.exists(self)

    def count(self):
        timeout = self._timeout('count')
        if isinstance(timeout, int):
            core = (self.__table, self.core_cache_name)
            cache_key = "%s:count:%s" % core
            version = cache.get_int("version:%s:%s" % core)
            if version:
                v = self.cache_version
                n = cache.get_int(cache_key)
            else:
                v = None
                n = None

            if not isinstance(n, int) or version < v:
                n = QuerySet.count(self)
                if n > 0:
                    cache.set_int("version:%s:%s" % core, self.cache_version, timeout)
                    cache.set_int(cache_key, n, timeout)
            del cache_key
            return n
        return QuerySet.count(self)

    def get(self, *args, **kwargs):
        timeout = self.cache_scheme.get('get')
        document = None
        if isinstance(timeout, int):
            core_cache_name = CacheNameMixer(kwargs)
            cache_key = "%s:get:%s" % (self.__table, core_cache_name)
            document = cache.get(cache_key)
            if isinstance(document, SecondaryKey):
                v = document.version
                document = cache.get(document.key)
                if not isinstance(document, models.Model) or v < self.cache_version:
                    document = None

            if not isinstance(document, models.Model):
                document = QuerySet.get(self, *args, **kwargs)
                original_cache_key = "%s:get:%s" % (self.__table, CacheNameMixer({ 'pk' : document.pk }))
                if original_cache_key != cache_key:
                    cache.set(cache_key,
                              SecondaryKey(original_cache_key, document.pk, self.cache_version),
                              timeout)

                cache.set(original_cache_key, document, timeout)
        else:
            document = QuerySet.get(self, *args, **kwargs)
        return document

    def update(self, **kwargs):
        res = QuerySet.update(self, **kwargs)
        model_change(collection=self.__table, delete=True)
        return res
    
    def delete(self):
        res = QuerySet.delete(self)
        model_change(collection=self.__table, delete=True)
        return res

def get_query_set(self):
    return CachedQuerySet(self.model, using=self._db)
