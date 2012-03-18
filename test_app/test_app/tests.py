"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import TestModel1, TestModel2, TestModel3
from random import Random
import time

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

def run_test(n=20000):
    res=''
    from django.conf import settings
    use=settings.DJANGO_REDISCACHE.get('used')
    
    if use:
        res+='Cache used\n'
    else:
        res+='Cache is off\n'

    res+='-- get random model %d times --\n' % n

    rand=Random()
    all_ids=[mod.id for mod in TestModel1.objects.all()]
    for id in all_ids:
        mod=TestModel1.objects.get(pk=id)
    
    sum=0
    start_time=time.time()
    for i in range(n):
        model=TestModel1.objects.get(pk= rand.choice(all_ids) )
        sum+=model.num
    
    res+='operations time: %s\n' % str(time.time()-start_time)
    
    all_ids=[mod.id for mod in TestModel2.objects.all()]
    for id in all_ids:
        mod=TestModel2.objects.get(pk=id)
    
    res+='-- get reference model %d times --\n' % n
    sum=0
    start_time=time.time()
    for i in range(n):
        model=TestModel2.objects.get(pk= rand.choice(all_ids) )
        sum+=model.model.num
    res+='operations time: %s\n' % str(time.time()-start_time)

    res+='-- get reference list of model %d times (m2m test) --\n' % n
    sum=0
    all_ids=[mod.id for mod in TestModel3.objects.all()]
    for id in all_ids:
        mod=TestModel3.objects.get(pk=id)
    element_count=0
    start_time=time.time()
    for i in range(n):
        model=TestModel3.objects.get(pk= rand.choice(all_ids) )
        if use:
            all=model.model_list.all().cache()
        else:
            all=model.model_list.all()
            
        for mod in all:
            element_count+=1
            sum+=mod.num
    res+='operations time: %s selected object count: %d \n' % (str(time.time()-start_time), element_count)
    
    from datetime import datetime, timedelta
    now=datetime.now()
    date_variants=[ now-timedelta(days=i) for i in range(14) ]
    access_chars=u'_abcde'
    
    name_part=u"".join([ rand.choice(access_chars) for i in range(2) ])
    res+='-- select one list %d times --\n' % n
    element_count=0
    sum=0
    rand_date=rand.choice(date_variants)
    start_time=time.time()
    for i in range(n):
        if use:
            all=TestModel1.objects.filter( name__contains=name_part, num__lt=500000, date__gt=rand_date).cache()
        else:
            all=TestModel1.objects.filter( name__contains=name_part, num__lt=500000, date__gt=rand_date)
        element_count+=all.count()
        for obj in all:
            sum+=obj.id
    res+='operations time: %s selected object count: %d\n' % ( str(time.time()-start_time), element_count)
 
    res+='-- select different lists --\n'
    element_count=0
    start_time=time.time()
    sum=0
    for i in range(n):
        name_part=u"".join([ rand.choice(access_chars) for i in range(2) ])
        if rand.randint(0,10)>5:
            all=TestModel1.objects.filter( name__contains=name_part, num__gt=500000, date__gt=rand.choice(date_variants))
        else:
            all=TestModel1.objects.filter( name__contains=name_part, num__lt=500000, date__gt=rand.choice(date_variants))
        
        if use: all=all.cache()
        element_count+=all.count()
        for obj in all:
            sum+=obj.id
    
    res+='operations time: %s selected object count: %d\n' % ( str(time.time()-start_time), element_count)

    return res
