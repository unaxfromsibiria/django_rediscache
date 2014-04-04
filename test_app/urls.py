# -*- coding: utf-8 -*-
'''
Created on 15.08.2013

@author: Michael Vorotyntsev (https://github.com/unaxfromsibiria/)
'''

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = staticfiles_urlpatterns()\
+ patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
