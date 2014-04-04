'''
Created on 10.03.2012

@author: unax
'''
import cPickle as pickle
import importlib
import logging
import redis
from .config import LazySettings, DEFAULT_LOGGER, DEFAULT_TIMEOUT
from .exception import ConfigurationFormatError
from .pool import BaseConnectionPool
from django_rediscache.pool import OnceConnectionPool
from functools import wraps
from hashlib import md5 as md5_constructor


class BaseCache(object):
    pool = None
    conn = None

    def cached(self, extra=None, timeout=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                md5 = md5_constructor()
                md5.update('{}.{}'.format(func.__module__, func.__name__))
                if extra:
                    md5.update(str(extra))
                if args:
                    md5.update(repr(args))
                if kwargs:
                    md5.update(repr(sorted(kwargs.items())))

                cache_key = 'c:{}'.format(md5.hexdigest())

                try:
                    result = self.get(cache_key)
                except (ValueError, TypeError):
                    result = func(*args, **kwargs)
                    self.set(cache_key, result, timeout)
                return result
            return wrapper
        return decorator


class RedisCache(BaseCache):
    def __init__(self, connection=None, pool=None):
        if isinstance(pool, BaseConnectionPool):
            self.pool = pool
        else:
            # fake pool
            self.pool = OnceConnectionPool(
                size=1, connection=connection)

    def connection_installer(self, method, *args, **kwargs):
        index, self.conn = self.pool.use_connection()
        try:
            result = method(*args, **kwargs)
        except Exception as err:
            raise err
        finally:
            self.conn = None
            self.pool.free(index)

        return result

    def _iface_get(self, cache_key):
        data = self.conn.get(cache_key)
        if data:
            data = pickle.loads(data)
        return data

    def _iface_pipeline_get(self, cache_key_list):
        if cache_key_list:
            pipe = self.conn.pipeline()
            for key in cache_key_list:
                pipe.get(key)
            data = pipe.execute()
            if data:
                return [pickle.loads(d) for d in data if d]
        return None

    def _iface_pipeline_delete(self, cache_key_list):
        if isinstance(cache_key_list, list) and len(cache_key_list) > 0:
            pipe = self.conn.pipeline()
            for key in cache_key_list:
                pipe.delete(key)
            data = pipe.execute()
            if data:
                return data
        return None

    def _iface_delete(self, cache_key):
        return self.conn.delete(cache_key)

    def _iface_set(self, cache_key, data, timeout=DEFAULT_TIMEOUT):
        if not self.conn:
            return
        assert isinstance(timeout, int)
        pickled_data = pickle.dumps(data)
        if timeout > 0:
            self.conn.setex(cache_key, pickled_data, timeout)
        else:
            self.conn.set(cache_key, pickled_data)

    def _iface_set_int(self, cache_key, data, timeout=DEFAULT_TIMEOUT):
        assert isinstance(timeout, int)
        self.conn.setex(cache_key, data, timeout)

    def _iface_get_int(self, cache_key):
        try:
            return int(self.conn.get(cache_key))
        except (AttributeError, TypeError, ValueError):
            return

    def _iface_incr(self, name, amount=1):
        self.conn.incr(name, amount)

    def _iface_flushall(self):
        if self.conn:
            self.conn.flushdb()
            return True
        return False

    def _iface_append_to_list(self, list_cache_key, data):
        self.conn.rpush(list_cache_key, data)

    def _iface_get_all_list(self, list_cache_key):
        return  self.conn.lrange(list_cache_key, 0, -1)

    def get(self, cache_key):
        return self.connection_installer(
            self._iface_get, cache_key)

    def pipeline_get(self, cache_key_list):
        return self.connection_installer(
            self._iface_pipeline_get, cache_key_list)

    def pipeline_delete(self, cache_key_list):
        return self.connection_installer(
            self._iface_pipeline_delete, cache_key_list)

    def delete(self, cache_key):
        return self.connection_installer(self._iface_delete, cache_key)

    def set(self, cache_key, data, timeout=DEFAULT_TIMEOUT):
        return self.connection_installer(
            self._iface_set, cache_key, data, timeout)

    def set_int(self, cache_key, data, timeout=DEFAULT_TIMEOUT):
        return self.connection_installer(
            self._iface_set_int, cache_key, data, timeout)

    def get_int(self, cache_key):
        return self.connection_installer(
            self._iface_get_int, cache_key)

    def incr(self, name, amount=1):
        return self.connection_installer(
            self._iface_incr, name, amount)

    def flushall(self):
        return self.connection_installer(
            self._iface_flushall)

    def append_to_list(self, list_cache_key, data):
        return self.connection_installer(
            self._iface_append_to_list, list_cache_key, data)

    def get_all_list(self, list_cache_key):
        return self.connection_installer(
            self._iface_get_all_list, list_cache_key)


class LazyCache(object):
    __this = None
    __cache = None

    def setup(self):
        if not isinstance(self.__cache, RedisCache):
            conf = LazySettings().content.get('redis')
            pool_conf = conf.get('pool')
            py_redis_conf = dict.fromkeys([
                'host', 'port', 'db', 'socket_timeout'])
            for key in py_redis_conf:
                py_redis_conf[key] = conf.get(key)

            conn = redis.Redis(**py_redis_conf)
            pool = None
            logger = logging.getLogger(DEFAULT_LOGGER)
            if pool_conf:
                try:
                    _module, _cls = (
                        pool_conf.get('class') or '').rsplit('.', 1)
                except ValueError:
                    raise ConfigurationFormatError(
                        u"Set class in pool section! Like this: "
                        u"'class': 'project.path.to.PoolClass'")
                else:
                    _module = importlib.import_module(_module)
                    _cls = getattr(_module, _cls, None)
                    if issubclass(_cls, BaseConnectionPool):
                        pool = _cls(
                            size=pool_conf.get('size'),
                            connection=conn)
                        logger.debug(
                            'Pool used! Size: {size}, class: {class}'.format(
                                **pool_conf))
                    else:
                        raise ConfigurationFormatError(
                            u"{class} must be subclass of"
                            u"BaseConnectionPool".format(**pool_conf))

            self.__cache = RedisCache(connection=conn, pool=pool)
            logger.debug(
                '{}: Cache connection is initialized'.format(
                    self.__class__.__name__))

    def __new__(cls):
        if cls.__this is None:
            cls.__this = super(LazyCache, cls).__new__(cls)
        return cls.__this

    def __getattr__(self, attr):
        try:
            value = self.__dict__[attr]
        except KeyError:
            self.setup()
            value = getattr(self.__cache, attr, None)
        return value

_internal_cache = LazyCache()
