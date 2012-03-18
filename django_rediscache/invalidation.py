'''
Created on 10.03.2012

@author: unax
'''

from journal import records
from cache import _internal_cache as cache

def model_change(pk, collection):
    cache.pipeline_delete(records('list', collection))
    cache.pipeline_delete(records('count', collection))
    cache.pipeline_delete(records('get',collection,'pk=%s' % str(pk) ))
    cache.delete("%s:get:journal:pk=%s" % (collection, str(pk)))
    cache.delete("%s:list:journal:" % collection )
    cache.delete("%s:count:journal:" % collection )
