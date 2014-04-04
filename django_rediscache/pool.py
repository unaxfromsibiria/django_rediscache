# -*- coding: utf-8 -*-
'''
Created on 31 марта 2014 г.

@author:  Michael Vorotyntsev
@email: linkofwise@gmail.com
'''

from .exception import ConfigurationFormatError


class BaseConnectionPool(object):
    u"""
    Base connection pool.
    This is 'empty implementation'
    """
    _size = None
    _connections = []
    _connection_busy = None

    def get_connection_at(self, index=0):
        return self._connections[index]

    def iter_limit_extended(self, iter_index):
        return False

    def wait(self):
        pass

    def __init__(self, connection, size):
        self._connections = [connection]
        if isinstance(size, int) and size > 0:
            self._size = size
            self._connection_busy = dict.fromkeys(xrange(size), False)
        else:
            raise ConfigurationFormatError(
                u"Size of pool must be a positive digest!")

    def free(self, index):
        if index in self._connection_busy:
            self._connection_busy[index] = False

    def use_connection(self, lock=True):
        iter_index = 0
        connection = None
        while connection is None and not self.iter_limit_extended(iter_index):
            iter_index += 1
            for index in xrange(self._size):
                if not self._connection_busy[index]:
                    self._connection_busy[index] = lock
                    return index, self.get_connection_at(index)
            self.wait()

        return None, None


class OnceConnectionPool(BaseConnectionPool):
    def get_connection_at(self, index=0):
        return super(
            OnceConnectionPool,
            self).get_connection_at(index=0)


class GeventConnectionPool(BaseConnectionPool):
    u"""
    Without this pool geven create
    to many connections to redis server.
    """
    _gevent_wait_method = None
    _time_out = 0.001

    def __init__(self, *args, **kwargs):
        import gevent
        self._gevent_wait_method = gevent.sleep
        return super(GeventConnectionPool, self).__init__(*args, **kwargs)

    def wait(self):
        self._gevent_wait_method(self._time_out)

    def iter_limit_extended(self, iter_index):
        # wait limit - 60 seconds
        return iter_index * self._time_out > 60

    def get_connection_at(self, index=0):
        # actually we need once connection here
        # gevent multiply connection it self,
        # that is what we need limited by this pool
        #print '=======>>>> ', index
        return super(
            GeventConnectionPool,
            self).get_connection_at(index=0)
