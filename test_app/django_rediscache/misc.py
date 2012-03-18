# -*- coding: utf-8 -*-
'''
Created on 08.03.2012

@author: unax
'''

from django.db import models
from datetime import datetime
import hashlib
from django.conf import settings
from re import _pattern_type

try:
    HASHED_NAME_ALWAYS=settings.DJANGO_REDISCACHE.get('keyhashed')
except:
    HASHED_NAME_ALWAYS=False

class _queryset_list(list):
    def __init__(self, anylist=None):
        if anylist is None:
            super(_queryset_list, self).__init__()
        else:
            super(_queryset_list, self).__init__(anylist)
    def count(self):
        return len(self)

class CacheNameMixer(object):
    __line=None
    
    def __init__(self, query_dict=None ):
        self.__line=self.__parse(query_dict)
    
    def __str__(self):
        if HASHED_NAME_ALWAYS:
            return self.hash
        return self.__line
    
    def __unicode__(self):
        return u"%s"%self.__line
    
    @property
    def hash(self):
        md5=hashlib.md5()
        md5.update(self.__line)
        return md5.hexdigest()
    
    @property
    def line(self):
        return str(self)
    
    @property
    def exist(self):
        return self.__line is not None and len(self.__line)>0

    def __create_str(self, query_obj ):
        if isinstance(query_obj, unicode) or isinstance(query_obj, str):
            return query_obj.encode('utf8')
        elif isinstance(query_obj, int):
            return str(query_obj)
        elif isinstance(query_obj, float):
            return str(query_obj)
        elif isinstance(query_obj, datetime):
            return query_obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(query_obj, models.Model):
            return str(query_obj.pk)
        elif isinstance(query_obj,  _pattern_type):
            return "regex(%s)" % query_obj.pattern
        elif isinstance(query_obj, dict):
            return self.__parse(query_obj)
        elif isinstance(query_obj, tuple):
            return "(%s)" % (",".join( [ self.__create_str(obj) for obj in query_obj ] ))
        else:
            try:
                return str(query_obj)
            except:
                pass
        return 'unknown_type'

    def __parse(self, query_dict ): # query_dict is dict, list or tuple
        if isinstance(query_dict,dict) and query_dict.keys()>0:
            query_line=[]
            for key in query_dict:
                query_line.append('%s=%s' % (key, self.__create_str(query_dict.get(key))) )
            return "|".join(query_line)
        elif isinstance(query_dict,tuple) or isinstance(query_dict,list):
            return "(%s)" % ( ",".join( [ self.__create_str(key) for key in query_dict ] ) )
        elif isinstance(query_dict,str) or isinstance(query_dict,unicode):
            return "request='%s'" % self.__create_str(query_dict)
        return None

    def append(self, query_dict ):
        new_line=self.__parse(query_dict).replace(' ','')
        if self.__line is not None and new_line is not None:
            self.__line += '|%s' % new_line
        elif new_line is not None:
            self.__line  = new_line