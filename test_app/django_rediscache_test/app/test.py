# -*- coding: utf-8 -*-
'''
Created on 15.08.2013

@author: Michael Vorotyntsev (https://github.com/unaxfromsibiria/)
'''
import sys
import time
from .models import Model1, Model2, Model3
from random import Random
from datetime import datetime, timedelta
rand = Random()


def random_hex(size=rand.randint(8, 32)):
    return u"".join([rand.choice('023456789abcdef')
        for _ in range(size)])


def random_date(interval=(datetime(2013, 8, 1), datetime(2013, 8, 30))):
    s = int((interval[1] - interval[0]).total_seconds())
    return interval[0] + timedelta(seconds=rand.randint(1, s - 1))


def create_models(n=100, only=[1, 2, 3]):
    if 1 in only:
        print 'will be created {0} Model1'.format(n)
        for _ in range(n):
            m = Model1(
               name=random_hex(),
               number=rand.randint(1, n),
               created=random_date())
            m.save()

    if 2 in only:
        print 'will be created {0} Model2'.format(n)
        for _ in range(n):
            m = Model2(
               name=random_hex(),
               model=Model1.objects.all().order_by('?')[0],
               number=rand.randint(1, n),
               created=random_date())
            m.save()

    if 3 in only:
        print 'will be created {0} Model3'.format(n)
        for _ in range(n):
            m = Model3(
               name=random_hex(),
               number=rand.randint(1, n),
               created=random_date())
            m.save()
            m.model_list = list(Model1.objects.all()\
                .order_by('?')[:rand.randint(1, n / 10)])
            m.save()


def get_test(n=1000):
    pk_list = [m.pk for m in Model1.objects.all()]
    # warmer
    for k in pk_list:
        m = Model1.objects.get(pk=k)

    print 'Get test (operations count: {0}):'.format(n)
    start_time = time.time()
    s = 0
    for _ in range(n):
        k = rand.choice(pk_list)
        m = Model1.objects.get(pk=k)
        s += sys.getsizeof(m)

    print 'time: {0}'.format(str(time.time() - start_time))
    print 'total lists size {0} mb'.format(
        str(float(s) / float(1024 ** 2))[0:5])


dates = [random_date() for i in range(5)]
val = [rand.randint(4000, 5000) for i in range(5)]
chars = [u"{0}{1}".format(
    rand.choice('023456789abcdef'),
    rand.choice('023456789abcdef')) for i in range(5)]


def list_and_count_test(n=1000):
    pk_list = [m.pk for m in Model1.objects.all()]
    # warmer
    for k in pk_list:
        m = Model1.objects.get(pk=k)

    m = 0
    s = 0
    print 'Count&List test (operations count: {0}):'.format(n)
    start_time = time.time()
    for i in range(n):
        models = Model1.objects.filter(created__lt=rand.choice(dates))
        if rand.randint(0, 10) > 5:
            models.filter(number__gt=rand.choice(val))
        if rand.randint(0, 10) > 5:
            models.filter(name__contains=rand.choice(chars))
        if models.count() > 0:
            if models.__class__.__name__ == 'CachedQuerySet':
                l = models[0:20].cache
            else:
                l = models[0:20]
            m += l.count()
            for obj in l:
                if obj.pk:
                    s += sys.getsizeof(obj)

    print 'time: {0}'.format(str(time.time() - start_time))
    print 'object count: {0}'.format(m)
    print 'total lists size {0} mb'.format(
        str(float(s) / float(1024 ** 2))[0:5])


def reference_get_test(n=1000):
    # warmer
    pk_list = [m.pk for m in Model1.objects.all()]
    for k in pk_list:
        m = Model1.objects.get(pk=k)
    pk_list = [m.pk for m in Model2.objects.all()]
    for k in pk_list:
        m = Model2.objects.get(pk=k)

    print 'Reference get test (operations count: {0}):'.format(n)
    start_time = time.time()
    s = 0
    for i in range(n):
        k = rand.choice(pk_list)
        m = Model2.objects.get(pk=k)
        s += sys.getsizeof(m) + sys.getsizeof(m.model1)

    print 'time: {0}'.format(str(time.time() - start_time))
    print 'total lists size {0} mb'.format(
        str(float(s) / float(1024 ** 2))[0:5])


def reference_list_test(n=1000):
    # warmer
    pk_list = [m.pk for m in Model1.objects.all()]
    for k in pk_list:
        m = Model1.objects.get(pk=k)
    pk_list = [m.pk for m in Model3.objects.all()]
    for k in pk_list:
        m = Model3.objects.get(pk=k)

    print 'Reference list test (operations count: {0}):'.format(n)
    start_time = time.time()
    s = 0
    for i in range(n):
        k = rand.choice(pk_list)
        m = Model3.objects.get(pk=k)
        s += sys.getsizeof(m)
        for m1 in m.model1.all():
            s += sys.getsizeof(m1)

    print 'time: {0}'.format(str(time.time() - start_time))
    print 'total lists size {0} mb'.format(
        str(float(s) / float(1024 ** 2))[0:5])
