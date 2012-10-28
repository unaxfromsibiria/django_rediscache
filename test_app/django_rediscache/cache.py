'''
Created on 10.03.2012

@author: unax
'''

import cPickle as pickle
from functools import wraps
from django.utils.hashcompat import md5_constructor
import redis

DEFAULT_TIMEOUT = 600

class BaseCache(object):
    def cached(self, extra=None, timeout=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                md5 = md5_constructor()
                md5.update('%s.%s' % (func.__module__, func.__name__))
                if extra is not None:
                    md5.update(str(extra))
                if args:
                    md5.update(repr(args))
                if kwargs:
                    md5.update(repr(sorted(kwargs.items())))

                cache_key = 'c:%s' % md5.hexdigest()

                try:
                    result = self.get(cache_key)
                except:
                    result = func(*args, **kwargs)
                    self.set(cache_key, result, timeout)
                return result
            return wrapper
        return decorator

class RedisCache(BaseCache):
    def __init__(self, conn):
        self.conn = conn

    def get(self, cache_key):
        data = self.conn.get(cache_key)
        if data is None:
            return None
        return pickle.loads(data)

    def pipeline_get(self, cache_key_list):
        if cache_key_list:
            pipe = self.conn.pipeline()
            for key in cache_key_list:
                pipe.get(key)
            data = pipe.execute()
            if data:
                return [ pickle.loads(d) for d in data if d ]
        return None

    def pipeline_delete(self, cache_key_list):
        if isinstance(cache_key_list, list) and len(cache_key_list) > 0:
            pipe = self.conn.pipeline()
            for key in cache_key_list:
                pipe.delete(key)
            data = pipe.execute()
            if data:
                return data
        return None

    def delete(self, cache_key):
        return self.conn.delete(cache_key)

    def set(self, cache_key, data, timeout=DEFAULT_TIMEOUT):
        if self.conn is None:
            return
        pickled_data = pickle.dumps(data)
        if timeout is not None:
            self.conn.setex(cache_key, pickled_data, timeout)
        else:
            self.conn.set(cache_key, pickled_data)
            
    def set_int(self, cache_key, data, timeout=DEFAULT_TIMEOUT):
        if not isinstance(data, int):
            return
        self.conn.setex(cache_key, data, timeout)

    def get_int(self, cache_key):
        try:    return int(self.conn.get(cache_key))
        except: return None

    def incr(self, name, amount=1):
        self.conn.incr(name, amount)

    def flushall(self):
        if self.conn is None:
            return False
        try:    self.conn.flushdb()
        except: return False
        return True

    def append_to_list(self, list_cache_key, data):
        self.conn.rpush(list_cache_key, data)

    def get_all_list(self, list_cache_key):
        return  self.conn.lrange(list_cache_key, 0, -1)

from config import LazySettings
redis_conf = LazySettings().content.get('redis')
_cache = RedisCache(redis.Redis(**redis_conf))
