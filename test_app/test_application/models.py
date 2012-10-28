# -*- coding: utf-8 -*-
'''
Created on 17.10.2012

@author: unax
'''

from django.db import models
from django.contrib import admin


class Model1(models.Model):
    volume  = models.IntegerField(default=0)
    created = models.DateTimeField()
    name    = models.CharField(max_length=32, blank=True)

    class Meta:
        verbose_name = u'Test model 1'
        verbose_name_plural = u'Test model 1'
    
    def __unicode__(self):
        return u"%s %d" % (self.name, self.volume)

class Model1Admin(admin.ModelAdmin):
    list_display = ('volume', 'created', 'name', )

class Model2(models.Model):
    model1  = models.ForeignKey(Model1)
    created = models.DateTimeField()
    name    = models.CharField(max_length=32, blank=True)
    count   = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'Test model 2'
        verbose_name_plural = u'Test model 2'

class Model2Admin(admin.ModelAdmin):
    list_display = ('model1', 'created', 'name', 'count' )

class Model3(models.Model):
    model1  = models.ManyToManyField(Model1)
    created = models.DateTimeField()
    name    = models.CharField(max_length=32, blank=True)
    count   = models.IntegerField(default=0)

    class Meta:
        verbose_name = u'Test model 3'
        verbose_name_plural = u'Test model 3'

class Model3Admin(admin.ModelAdmin):
    list_display = ( 'created', 'name', 'count' )
