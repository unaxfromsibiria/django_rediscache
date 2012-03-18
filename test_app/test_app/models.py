# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
# Create your models here.

class TestModel1(models.Model):
    num = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=32, blank=True)
    about = models.TextField(null=True, blank=False)

    class Meta:
        verbose_name = u'Test model 1'
        verbose_name_plural = u'Test model 1'
    
    def __unicode__(self):
        return u"%s %d" % (self.name, self.num)

class TestModel1Admin(admin.ModelAdmin):
    list_display = ('num', 'date', 'name', 'about' )

class TestModel2(models.Model):
    model = models.ForeignKey(TestModel1)
    date = models.DateTimeField()
    name = models.CharField(max_length=32, blank=True)
    about = models.TextField(null=True, blank=False)

    class Meta:
        verbose_name = u'Test model 2'
        verbose_name_plural = u'Test model 2'

class TestModel2Admin(admin.ModelAdmin):
    list_display = ('model', 'date', 'name', 'about' )

class TestModel3(models.Model):
    model_list = models.ManyToManyField(TestModel1)
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=32, blank=True)
    about = models.TextField(null=True, blank=False)

    class Meta:
        verbose_name = u'Test model 3'
        verbose_name_plural = u'Test model 3'

class TestModel3Admin(admin.ModelAdmin):
    list_display = ( 'date', 'name', 'about' )
