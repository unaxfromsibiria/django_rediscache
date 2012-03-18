'''
Created on 06.03.2012

@author: unax
'''
from django.db import models
from misc import CacheNameMixer, _queryset_list
from django.db.models.query import QuerySet
from django.conf import settings
from cache import _internal_cache as cache
import journal

class CachedQuerySet(QuerySet):
    __cache_scheme=None
    __table=None
    def __init__(self, model=None, query=None, using=None):
        self.__cache_scheme=settings.DJANGO_REDISCACHE.get('scheme').get(str(model.__module__).replace('models',model.__name__))
        super(CachedQuerySet, self).__init__(model, query, using)
        self.__table=self.model._meta.db_table
            
    def cache_scheme(self):
        return self.__cache_scheme
    
    def __timeout(self, request):
        if request and self.__cache_scheme:
            res=self.__cache_scheme.get(request)
            if res is None: res=self.__cache_scheme.get('all')
            return res
        return None

    def core_cache_name(self):
        return str( CacheNameMixer(str(self.query)) )

    def cache(self):
        timeout=self.__timeout('list')
        if timeout and timeout>0:
            
            cache_key="%s:list:%s"%(self.__table, str(CacheNameMixer(self.core_cache_name())) )
            res=cache.get(cache_key)
            if res is None:
                res=_queryset_list([m for m in self])
                cache.set(cache_key, res, timeout)
                journal.add_find_record(cache_key,self.__table,timeout)
            del cache_key
            return res
        else:
            raise Exception("This model %s hasn't settings for 'list' in DJANGO_REDISCACHE" )

    def get(self, *args, **kwargs):
        timeout=self.__timeout('get')
        if timeout and timeout>0:
            cache_key="%s:get:%s"%(self.__table, str(CacheNameMixer(kwargs)) )
            res=cache.get(cache_key)
            if res is None:
                res=super(CachedQuerySet, self).get(*args,**kwargs)
                for fl in res._meta.fields:
                    field=getattr(res, fl.name, None)
                    if isinstance(fl,models.ForeignKey) or isinstance(fl,models.OneToOneField) and field:
                        self.model._django_rediscache[fl.name]={ 'class' : field.__class__.__name__, 'pk' : field.pk }
                cache.set(cache_key, res, timeout)
                journal.add_get_record(res.id, cache_key,self.__table,timeout)
            elif isinstance(self.model._django_rediscache, dict):
                for fl in res._meta.fields:
                    obj=self.model._django_rediscache.get(fl.name)
                    if obj:
                        try:
                            cached_field=None
                            exec('cached_field=%s.objects.get(pk=%)' % (obj.get('class'),obj.get('pk')) )
                            if cached_field: setattr(res, fl.name, cached_field)
                        except:
                            pass
            del cache_key
            return res
        else:
            return super(CachedQuerySet, self).get(*args,**kwargs)

    def count(self):
        timeout=self.__timeout('count')
        if timeout and timeout>0:
            cache_key="%s:count:%s"%(self.__table, self.core_cache_name())
            res=cache.get(cache_key)
            if res is None:
                res=super(CachedQuerySet, self).count()
                cache.set(cache_key, res, timeout)
                journal.add_count_record(cache_key,self.__table,timeout)
            del cache_key
            return res
        else:
            return super(CachedQuerySet, self).count()

def get_query_set(self):
    return CachedQuerySet(self.model, using=self._db)
