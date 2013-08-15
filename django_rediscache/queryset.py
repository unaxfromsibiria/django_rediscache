'''
Created on 06.03.2012

@author: unax
'''
from .cache import _internal_cache as cache
from .config import LazySettings, ABSOLUTE_VERSION_LIMIT
from .helper import _queryset_list, SecondaryKey
from .invalidation import model_change
from .misc import CacheNameMixer
from django.db import models
from django.db.models.query import QuerySet


class CachedQuerySet(QuerySet):
    __cache_scheme = None
    __table = None

    def __init__(self, model=None, query=None, using=None):
        super(CachedQuerySet, self).__init__(
            model=model, query=query, using=using)
        self.__cache_scheme = LazySettings().scheme.get(
            "{0}.{1}".format(model.__module__, model.__name__)) or {}
        self.__table = self.model._meta.db_table

    @property
    def cache_scheme(self):
        return self.__cache_scheme

    @property
    def cache_version(self):
        version = cache.get_int("version:{0}".format(self.__table))
        if not isinstance(version, int) or version > ABSOLUTE_VERSION_LIMIT:
            version = 1
            cache.set_int(
                "version:{0}".format(self.__table),
                version,
                max([v for k, v in self.__cache_scheme.iteritems()]) + 1)
        return version

    def _timeout(self, operation):
        return self.__cache_scheme.get(operation)

    @property
    def core_cache_name(self):
        return CacheNameMixer(
            {'sql': self.query}).hash

    @property
    def cache(self):
        timeout = self.cache_scheme.get('list')
        if isinstance(timeout, int):
            core = (self.__table, self.core_cache_name)
            cache_key = "{0}:list:{1}".format(*core)
            version_key = "version:{0}:{1}".format(*core)
            version = cache.get_int(version_key)
            if isinstance(version, int):
                v = self.cache_version
                cached_list = cache.get(cache_key)
            else:
                v = cached_list = None

            if isinstance(cached_list, list) and version == v:
                self._result_cache = _queryset_list(
                    cache.pipeline_get(cached_list))
                del cache_key
                del cached_list
                return self
            else:
                # creating cache
                if self.count() > 0:
                    keys = list()
                    for obj in self:
                        obj_cache_key = "{0}:get:{1}".format(
                            self.__table, CacheNameMixer({'pk': obj.pk}))
                        keys.append(obj_cache_key)
                        cache.set(obj_cache_key, obj, timeout)
                    cache.set(
                        cache_key, keys, timeout - 1)
                    cache.set_int(
                        version_key, self.cache_version, timeout - 1)
                del cache_key
        return self

    def exists(self):
        timeout = self._timeout('count')
        if isinstance(timeout, int):
            return self.count() > 0
        return super(CachedQuerySet, self).exists()

    def count(self):
        timeout = self._timeout('count')
        if isinstance(timeout, int):
            core = (self.__table, self.core_cache_name)
            cache_key = "{0}:count:{1}".format(*core)
            version_key = "version:{0}:{1}".format(*core)
            version = cache.get_int(version_key)
            if version:
                v = self.cache_version
                n = cache.get_int(cache_key)
            else:
                v = n = None

            if not isinstance(n, int) or version < v:
                n = super(CachedQuerySet, self).count()
                if n > 0:
                    cache.set_int(version_key, self.cache_version, timeout)
                    cache.set_int(cache_key, n, timeout)
            del cache_key
            return n
        return super(CachedQuerySet, self).count()

    def get(self, *args, **kwargs):
        timeout = self.cache_scheme.get('get')
        document = None
        if isinstance(timeout, int):
            cache_key = "{0}:get:{1}".format(
                self.__table, CacheNameMixer(kwargs))
            document = cache.get(cache_key)
            if isinstance(document, SecondaryKey):
                v = document.version
                document = cache.get(document.key)
                if not isinstance(document, models.Model) or v < self.cache_version:
                    document = None

            if not isinstance(document, models.Model):
                document = super(CachedQuerySet, self).get(*args, **kwargs)

                original_cache_key = "{0}:get:{1}".format(
                    self.__table, CacheNameMixer({'pk': document.pk}))
                if original_cache_key != cache_key:
                    cache.set(
                        cache_key,
                        SecondaryKey(
                            original_cache_key,
                            document.pk,
                            self.cache_version),
                        timeout)
                cache.set(original_cache_key, document, timeout)
        else:
            document = super(CachedQuerySet, self).get(*args, **kwargs)
        return document

    def update(self, *args, **kwargs):
        res = super(CachedQuerySet, self).update(*args, **kwargs)
        model_change(collection=self.__table, delete=True)
        return res

    def delete(self):
        res = super(CachedQuerySet, self).delete()
        model_change(collection=self.__table, delete=True)
        return res


def get_query_set(self):
    return CachedQuerySet(self.model, using=self._db)
