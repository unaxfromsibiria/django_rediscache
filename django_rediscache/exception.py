# -*- coding: utf-8 -*-
'''
Created on 31 марта 2014 г.

@author:  Michael Vorotyntsev
@email: linkofwise@gmail.com
'''


class ConfigurationFormatError(ValueError):
    u"""
    Configuration format error.
    """

    def __init__(self, msg=None):
        if not msg:
            msg = u"Check settings section DJANGO_REDISCACHE"
        return super(ConfigurationFormatError, self).__init__(msg)
