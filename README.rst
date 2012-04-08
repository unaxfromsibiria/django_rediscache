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
You do not need any special descriptions in the models (for example look at models.py of application "test_app")::

	class TestModel1(models.Model):
	    num = models.IntegerField(default=0)
	    date = models.DateTimeField(auto_now=True)
	    name = models.CharField(max_length=32, blank=True)
	    about = models.TextField(null=True, blank=False)
	
	class TestModel2(models.Model):
	    model = models.ForeignKey(TestModel1)
	    date = models.DateTimeField()
	    name = models.CharField(max_length=32, blank=True)
	    about = models.TextField(null=True, blank=False)
	
	class TestModel3(models.Model):
	    model_list = models.ManyToManyField(TestModel1)
	    date = models.DateTimeField(auto_now=True)
	    name = models.CharField(max_length=32, blank=True)
	    about = models.TextField(null=True, blank=False)

You need set configuration only.

Configuration
=====
Create section DJANGO_REDISCACHE in django settings::

	DJANGO_REDISCACHE = {
	    'scheme' : {'test_app.TestModel1' : { 'list' : 1200, 'count' : 1200, 'get' : 1800 },
	                'test_app.TestModel2' : { 'all' : 1200 },
	                'test_app.TestModel3' : { 'all' : 1200 },
	               },
	    'redis' : {
	        'host': 'localhost',
	        'port': 6379,
	        'db'  : 2,
	        'socket_timeout': 5,
	    },               
	    'used' : True,
	    'keyhashed' : True,
	}

- `'count' - use cache for count() method of QuerySet`
- `'list' - use cache in QuerySet, you just need to call method ".cache()" after of all "filter" and "order_by"`
- `'get' - use cache in QuerySet for all get request`

And don't forget add 'django_rediscache' in INSTALLED_APPS. All simple and can sometimes be effective, look at test results.
There is analog project if it will be usefull https://github.com/Suor/django-cacheops
Sincerely, Michael Vorotyntsev.
