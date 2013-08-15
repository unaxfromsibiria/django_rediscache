# -*- coding: utf-8 -*-
'''
Created on 28.10.2012

@author: unax
'''
from django.db import router
from django.db.models.fields.related import ReverseSingleRelatedObjectDescriptor
from queryset import CachedQuerySet


class CachedReverseSingleRelatedObjectDescriptor(ReverseSingleRelatedObjectDescriptor):

    def get_query_set(self, **db_hints):
        return CachedQuerySet(self.field.rel.to).using(\
                router.db_for_read(self.field.rel.to, **db_hints))
