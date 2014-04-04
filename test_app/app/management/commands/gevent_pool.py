# -*- coding: utf-8 -*-
'''
Created on 03 апр. 2014 г.

@author:  Michael Vorotyntsev
@email: linkofwise@gmail.com
'''
try:
    import gevent
    from gevent import monkey
except ImportError:
    monkey = None
if monkey:
    monkey.patch_all()

import sys
from django.core.management.base import BaseCommand

from .test import rand, stdout, random_date, random_hex
from app.models import Model1


def create_data(count):
    stdout("Creating {} models...".format(count))
    for _ in xrange(count):
        Model1.objects.get_or_create(
            name=random_hex(),
            created=random_date(),
            number=rand.randint(0, count))
    stdout('done.')


def find_object(index, count, statistic):
    stdout('Thread {} started.'.format(index))
    for _ in xrange(count):
        _filter = {
            'created__lte': random_date(),
            'name__contains': random_hex(size=2),
        }

        models = Model1.objects.filter(**_filter)
        result_count = models.count()
        if result_count:
            statistic['hits'] += result_count
            for model in models.cache:
                obj = Model1.objects.get(id=model.id)
                statistic['sum'] += sys.getsizeof(obj)
        else:
            statistic['misses'] += 1

        gevent.sleep(0)

    stdout('Thread {} completed.'.format(index))


class Command(BaseCommand):
    help = '''Test connection pool. Run:
        $watch -n 1 "redis-cli info | grep connected_clients:"'''

    def handle(self, *args, **options):
        # thread count
        thread = options.get('thread', 50)
        count = options.get('count', 10)
        create_data(count)
        statistic = {'hits': 0, 'misses': 0, 'sum': 1}
        greenlets = [
            gevent.spawn(find_object, i + 1, count, statistic)
                for i in xrange(thread)]
        gevent.joinall(greenlets)

        stdout("""
            Hits: {hits} Misses: {misses}
            Result: {sum}
            """.format(**statistic))
