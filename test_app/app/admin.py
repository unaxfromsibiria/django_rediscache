# -*- coding: utf-8 -*-
'''
Created on 15.08.2013

@author: Michael Vorotyntsev (https://github.com/unaxfromsibiria/)
'''

from models import (
    Model1, Model2, Model3
)
from django.contrib import admin

admin.site.register(Model1)
admin.site.register(Model2)
admin.site.register(Model3)
