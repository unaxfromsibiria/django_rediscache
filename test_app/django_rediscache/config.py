# -*- coding: utf-8 -*-
'''
Created on 17.10.2012

@author: unax
'''

DEBUG = False
ABSOLUTE_VERSION_LIMIT = 4294967294

posible_options = ('list',
                   'get',
                   'reference',
                   'count')

class ClassProperty(object):
    def __init__(self, getter, setter):
        self.getter = getter
        self.setter = setter

    def __get__(self, cls, owner):
        return getattr(cls, self.getter)()

    def __set__(self, cls, value):
        getattr(cls, self.setter)(value)

class MetaSettings(type):
    options = ClassProperty('get_options', 'set_options')

class LazySettings(object):
    __metaclass__ = MetaSettings
    __this = None
    __settings = None
    __scheme = None
    __keyhashed = None

    def __new__(cls):
        if cls.__this is None:
            cls.__this = super(LazySettings, cls).__new__(cls)
        return cls.__this
    
    def create(self, **options):
        conf = None
        if len(options) > 1 and 'redis' in options:
            conf = options
        else:
            from django.conf import settings
            conf = getattr(settings, 'DJANGO_REDISCACHE', None)

        if conf:
            scheme = conf.get('scheme')
            self.__class__.__settings = conf
            for model in scheme:
                for_all = scheme[model].get('all')
                if isinstance(for_all, int):
                    for key in posible_options:
                        scheme[model][key] = for_all
            self.__class__.__keyhashed = conf.get('keyhashed')
            if conf.get('used'):
                self.__class__.__scheme = scheme
            else:
                self.__class__.__scheme = {}
            return True
        else:
            return False

    @classmethod
    def get_options(cls):
        return cls().content

    @classmethod
    def set_options(cls, option_dict):
        if isinstance(option_dict, dict):
            cls().create(**option_dict)

    @property
    def content(self):
        if self.__settings is None and not self.create():
            raise Exception('Django rediscache error! No settings.')
        return self.__settings

    @property
    def scheme(self):
        return self.__scheme

    @property
    def keyhashed(self):
        return self.__keyhashed

    @classmethod
    def timelimit(cls, model_name, operation):
        scheme = cls().simple_scheme.get(model_name)
        if scheme:
            timeout = scheme.get(operation)
            if not isinstance(timeout, int):
                timeout = scheme.get('all')
            return timeout
