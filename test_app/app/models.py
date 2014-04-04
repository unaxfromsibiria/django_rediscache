# -*- coding: utf-8 -*-
'''
Created on 15.08.2013

@author: Michael Vorotyntsev (https://github.com/unaxfromsibiria/)
'''

from django.db import models
from django.conf import settings
from django.utils.timezone import now as datetime_now
from random import randint


class Model1(models.Model):
    name = models.CharField(u"Name", max_length=32)
    number = models.IntegerField(u"Number")
    created = models.DateTimeField(u"Created", default=datetime_now)

    class Meta:
        app_label = 'app'
        db_table = 'app_model_1'
        verbose_name = u'Test model 1'
        verbose_name_plural = u'Test models 1'
        ordering = ['created']

    def __unicode__(self):
        return self.name


class Model2(models.Model):
    name = models.CharField(u"Name", max_length=32)
    number = models.IntegerField(u"Number")
    model = models.ForeignKey(Model1)
    created = models.DateTimeField(u"Created", default=datetime_now)

    class Meta:
        app_label = 'app'
        db_table = 'app_model_2'
        verbose_name = u'Test model 2'
        verbose_name_plural = u'Test models 2'
        ordering = ['created']

    def __unicode__(self):
        return self.name


class Model3(models.Model):
    name = models.CharField(u"Name", max_length=32)
    number = models.IntegerField(u"Number")
    model_list = models.ManyToManyField(Model1)
    created = models.DateTimeField(u"Created", default=datetime_now)

    class Meta:
        app_label = 'app'
        db_table = 'app_model_3'
        verbose_name = u'Test model 3'
        verbose_name_plural = u'Test models 3'
        ordering = ['created']

    def __unicode__(self):
        return self.name
