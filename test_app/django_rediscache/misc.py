# -*- coding: utf-8 -*-
'''
Created on 08.03.2012

@author: unax
'''

from config import LazySettings
from datetime import datetime
from django.db import models
from django.db.models.query import QuerySet
from django.utils.encoding import smart_str
from hashlib import sha1, md5
from re import _pattern_type
from zlib import crc32


hash_func = {
    'md5': lambda st: md5(st).hexdigest(),
    'sha1': lambda st: sha1(st).hexdigest(),
    'crc': lambda st: hex(crc32(st))}


config = LazySettings()


class CacheNameMixer(object):
    __line = None
    __keyhashed = None

    @property
    def content(self):
        return str(self)

    def __init__(self, query_dict=None):
        self.__keyhashed = config.keyhashed
        self.__line = self.__parse(query_dict)

    def __str__(self):
        return self.hash

    def __unicode__(self):
        return self.hash

    @property
    def hash(self):
        hash_method = hash_func.get(self.__keyhashed)
        if hash_method:
            return hash_method(self.__line)
        return self.__line

    @property
    def line(self):
        return str(self)

    @property
    def exist(self):
        return self.__line is not None and len(self.__line) > 0

    def __create_str(self, query_obj):
        if isinstance(query_obj, basestring):
            return smart_str(query_obj)
        elif isinstance(query_obj, (int, float)):
            return str(query_obj)
        elif isinstance(query_obj, datetime):
            return query_obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(query_obj, models.Model):
            return str(query_obj.pk)
        elif isinstance(query_obj, _pattern_type):
            return "regex({0})".format(query_obj.pattern)
        elif isinstance(query_obj, dict):
            return self.__parse(query_obj)
        elif isinstance(query_obj, tuple):
            return "({0})".format(
                ",".join([self.__create_str(obj) for obj in query_obj]))
        elif isinstance(query_obj, list) or isinstance(query_obj, QuerySet):
            return "[{0}]".format(
                ",".join([self.__create_str(obj) for obj in query_obj]))
        else:
            try:
                return str(query_obj)
            except:
                pass
        return 'unknown_type'

    def __parse(self, query_dict):
        if isinstance(query_dict, dict) and query_dict.keys() > 0:
            query_line = []
            for key in query_dict:
                query_line.append(u'{0}={1}'.format(
                    key, self.__create_str(query_dict.get(key))))
            return (u"|".join(query_line)).encode('utf8')
        elif isinstance(query_dict, tuple) or isinstance(query_dict, list):
            return (u"({0})".format(
                u",".join([self.__create_str(key)
                    for key in query_dict]))).encode('utf8')
        return None

    def append(self, query_dict):
        new_line = self.__parse(query_dict).replace(' ', '')
        if self.__line is not None and new_line is not None:
            self.__line += '|{0}'.format(new_line)
        elif new_line is not None:
            self.__line = new_line
