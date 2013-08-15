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
    name = models.CharField(u"Имя", max_length=32)
    number = models.IntegerField(u"Число")
    created = models.DateTimeField(u"Создан", default=datetime_now)

    class Meta:
        app_label = 'app'
        db_table = 'app_model_1'
        verbose_name = u'Модель 1'
        verbose_name_plural = u'Модель 1'
        ordering = ['created']

    def __unicode__(self):
        return self.name


class Model2(models.Model):
    name = models.CharField(u"Имя", max_length=32)
    number = models.IntegerField(u"Число")
    model = models.ForeignKey(Model1)
    created = models.DateTimeField(u"Создан", default=datetime_now)

    class Meta:
        app_label = 'app'
        db_table = 'app_model_2'
        verbose_name = u'Модель 2'
        verbose_name_plural = u'Модель 2'
        ordering = ['created']

    def __unicode__(self):
        return self.name


class Model3(models.Model):
    name = models.CharField(u"Имя", max_length=32)
    number = models.IntegerField(u"Число")
    models = models.ManyToManyField(Model1)
    created = models.DateTimeField(u"Создан", default=datetime_now)

    class Meta:
        app_label = 'app'
        db_table = 'app_model_3'
        verbose_name = u'Модель 3'
        verbose_name_plural = u'Модель 3'
        ordering = ['created']

    def __unicode__(self):
        return self.name
