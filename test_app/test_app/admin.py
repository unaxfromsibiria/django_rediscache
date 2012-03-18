'''
Created on 07.03.2012

@author: unax
'''

from django.contrib import admin

from models import TestModel1, TestModel1Admin, \
 TestModel2, TestModel2Admin, \
 TestModel3, TestModel3Admin

admin.site.register(TestModel1, TestModel1Admin)
admin.site.register(TestModel2, TestModel2Admin)
admin.site.register(TestModel3, TestModel3Admin)
