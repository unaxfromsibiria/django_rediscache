About
==========

:Info: Simple tools for caching models of Django ORM.

:Author: Michael


Dependencies
============
- django
- python-redis

Usage
=====

Allows you to cache Django ORM models.

In general, this project is analog  of `mongoengine <https://github.com/unaxfromsibiria/mongoengine_rediscache>`_

How to use?

Creating models as usual::

	from django.db import models
	
	class Model1(models.Model):
	    volume  = models.IntegerField(default=0)
	    created = models.DateTimeField()
	    name    = models.CharField(max_length=32, blank=True)
	
	    class Meta:
	        verbose_name = u'Test model 1'
	        verbose_name_plural = u'Test model 1'
	    
	    def __unicode__(self):
	        return u"%s %d" % (self.name, self.volume)
	
	class Model2(models.Model):
	    model1  = models.ForeignKey(Model1)
	    created = models.DateTimeField()
	    name    = models.CharField(max_length=32, blank=True)
	    count   = models.IntegerField(default=0)
	
	    class Meta:
	        verbose_name = u'Test model 2'
	        verbose_name_plural = u'Test model 2'

	class Model3(models.Model):
	    model1  = models.ManyToManyField(Model1)
	    created = models.DateTimeField()
	    name    = models.CharField(max_length=32, blank=True)
	    count   = models.IntegerField(default=0)
	
	    class Meta:
	        verbose_name = u'Test model 3'
	        verbose_name_plural = u'Test model 3'

You must append 'django_rediscache' to INSTALLED_APPS in last position::

	INSTALLED_APPS = (
	  'test_application',
	  'django_rediscache', 
	)

And create configuration section 'DJANGO_REDISCACHE' in Django settings::

	DJANGO_REDISCACHE = {
	    'scheme' : {'test_application.models.Model1' : {'all' : 3600},
	                'test_application.models.Model2' : {'all' : 3600},
	                'test_application.models.Model3' : {'all' : 3600},
	                },
	    'redis' : {
	        'host': 'localhost',
	        'port': 6379,
	        'db'  : 2,
	        'socket_timeout': 5,
	    },
	    'used'      : True,
	    'keyhashed' : 'crc',
	}

'list' - accept use cache for all filter, exclude, order_by operation.

'get' - all get operation.

'reference' - cached all ForeignKey and OneToOne field.

'count' - all count request will be cached.

'all' - all request operations

Option 'keyhashed' needed for hashing key in keyspace of redis.

It is known that the optimal length of a redis keys (30-80 bytes) and key hashing usefull for it.

Such values are available: 'md5', 'crc', 'sha1', 'off'

How to simple flush cahce? It is not necessary run FLUSHALL in redis-cli.

You only can change version of needed collection. For flush cache of Model1 you can::

	redis 127.0.0.1:6379> SELECT 1
	OK
	redis 127.0.0.1:6379[1]> INCRBY "version:model1" 1
	(integer) 12

If you want flush cache for all collection try this::

	$redis-cli -n 1 keys '*version:*' | grep '^version:[a-z0-9]\{1,32\}$' | xargs redis-cli -n 1 incr


Simple tests
=====
OS and soft::

	os: Debian GNU/Linux 3.2.0-3-amd64 x86_64
	cpu: Intel(R) Pentium(R) CPU P6200  @ 2.13GHz
	ram: 5657mb
	redis-server 2.4.14-1
	python 2.7.3rc2
	redis-py 2.4.13
	django 1.4.1-2
	postgresql 9.1.6-1
	psycopg2 2.4.5-1

Here primitive test the speed of documents get::

	=== simple get ===
	---- cache: on ----
	Get test (operations count: 50000):
	time: 10.3133158684
	total lists size 3.051 mb
	
	Get test (operations count: 50000):
	time: 9.77332806587
	total lists size 3.051 mb
	
	Get test (operations count: 50000):
	time: 9.83701610565
	total lists size 3.051 mb
	
	Get test (operations count: 50000):
	time: 10.0889670849
	total lists size 3.051 mb
	
	Get test (operations count: 50000):
	time: 10.1228568554
	total lists size 3.051 mb
	
	---- cache: off ----
	Get test (operations count: 50000):
	time: 105.217102051
	total lists size 3.051 mb
	
	Get test (operations count: 50000):
	time: 105.491556883
	total lists size 3.051 mb
	
	Get test (operations count: 50000):
	time: 104.584877968
	total lists size 3.051 mb
	
	Get test (operations count: 50000):
	time: 104.836049795
	total lists size 3.051 mb
	
	=== getting lists and his length ===

	---- cache: on ----
	Count&List test (operations count: 10000):
	time: 32.1580269337
	object count: 200000
	total lists size 12.20 mb
	
	Count&List test (operations count: 10000):
	time: 32.8594300747
	object count: 200000
	total lists size 12.20 mb
	
	Count&List test (operations count: 10000):
	time: 32.5740377903
	object count: 200000
	total lists size 12.20 mb
	
	Count&List test (operations count: 10000):
	time: 33.1423578262
	object count: 200000
	total lists size 12.20 mb

	---- cache: off ----
	Count&List test (operations count: 10000):
	time: 85.3806550503
	object count: 200000
	total lists size 12.20 mb
	
	Count&List test (operations count: 10000):
	time: 84.9257609844
	object count: 200000
	total lists size 12.20 mb
	
	Count&List test (operations count: 10000):
	time: 85.2910299301
	object count: 200000
	total lists size 12.20 mb
	
	Count&List test (operations count: 10000):
	time: 85.112621069
	object count: 200000
	total lists size 12.20 mb
	
	Count&List test (operations count: 10000):
	time: 85.024310112
	object count: 200000
	total lists size 12.20 mb
	
	=== getting reference document ===
	---- cache: on ----
	Reference get test (operations count: 10000):
	time: 7.55072903633
	total lists size 1.220 mb
	
	Reference get test (operations count: 10000):
	time: 7.52473711967
	total lists size 1.220 mb
	
	Reference get test (operations count: 10000):
	time: 7.63484382629
	total lists size 1.220 mb
	
	Reference get test (operations count: 10000):
	time: 7.74575901031
	total lists size 1.220 mb
	
	Reference get test (operations count: 10000):
	time: 7.44755887985
	total lists size 1.220 mb
	
	---- cache: off ----
	Reference get test (operations count: 10000):
	time: 45.0661520958
	total lists size 1.220 mb
	
	Reference get test (operations count: 10000):
	time: 45.2754909992
	total lists size 1.220 mb
	
	Reference get test (operations count: 10000):
	time: 45.3153030872
	total lists size 1.220 mb
	
	Reference get test (operations count: 10000):
	time: 44.9939219952
	total lists size 1.220 mb
	
	Reference get test (operations count: 10000):
	time: 45.4526510239
	total lists size 1.220 mb
	
	=== getting reference list (ManyToMany) ===
	---- cache: on ----
	Reference list test (operations count: 10000):
	time: 37.3141100407
	total lists size 5.747 mb
	
	Reference list test (operations count: 10000):
	time: 37.4080820084
	total lists size 5.665 mb
	
	Reference list test (operations count: 10000):
	time: 37.4431231022
	total lists size 5.673 mb
	
	Reference list test (operations count: 10000):
	time: 37.6082668304
	total lists size 5.760 mb
	
	Reference list test (operations count: 10000):
	time: 37.4190571308
	total lists size 5.693 mb
	
	---- cache: off ----
	Reference list test (operations count: 10000):
	time: 52.8332071304
	total lists size 5.707 mb
	
	Reference list test (operations count: 10000):
	time: 53.0865931511
	total lists size 5.700 mb
	
	Reference list test (operations count: 10000):
	time: 52.8128859997
	total lists size 5.671 mb
	
	Reference list test (operations count: 10000):
	time: 52.6719610691
	total lists size 5.673 mb
	
	Reference list test (operations count: 10000):
	time: 52.7085371017
	total lists size 5.697 mb

profit there..

Sincerely, Michael Vorotyntsev.
