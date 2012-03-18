'''
Created on 15.03.2012

@author: unax
'''

from models import TestModel1, TestModel2, TestModel3
from random import Random
from datetime import datetime, timedelta

def create(n):
    rand=Random()
    access_chars=u'_abcde'
    chars=u'abcde 1234567890'
    all_ids=[]
    for i in range(n):
        x=rand.randint(0,30)
        model=TestModel1(num=rand.randint(0,n*1000),
                         name=u"".join( [ rand.choice(access_chars) for i in range(rand.randint(6,24)) ] ),
                         about=u"".join( [ rand.choice(chars) for i in range(rand.randint(6,64)) ]) )
        if rand.randint(1,10)>5:
            model.date=datetime.now() - timedelta(days=x)
        else:
            model.date=datetime.now() + timedelta(days=x)
        model.save()
    
    for mod in TestModel1.objects.all():
        all_ids.append(mod.id)
                         
    for i in range(n):
        x=rand.randint(0,30)
        model=TestModel2(model=TestModel1.objects.get( id=rand.choice(all_ids) ),
                         name=u"".join( [ rand.choice(access_chars) for i in range(rand.randint(6,24)) ] ),
                         about=u"".join( [ rand.choice(chars) for i in range(rand.randint(6,64)) ]) )
        if rand.randint(1,10)>5:
            model.date=datetime.now() - timedelta(days=x)
        else:
            model.date=datetime.now() + timedelta(days=x)
        model.save()
    
    for i in range(n):
        ids=[ rand.choice(all_ids) for i in range(rand.randint(4,12)) ]
        model=TestModel3(name=u"".join( [ rand.choice(access_chars) for i in range(rand.randint(6,24)) ] ),
                         about=u"".join( [ rand.choice(chars) for i in range(rand.randint(6,64)) ]) )
        model.save()
        model.model_list = TestModel1.objects.filter(id__in=ids)
        model.save()
    