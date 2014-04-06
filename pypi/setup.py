# -*- coding: utf-8 -*-
import codecs
import django_rediscache
import os.path

version = ".".join((
    str(v) for v in django_rediscache.VERSION))

about = codecs.open(
    os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            'README.txt'))).read()

setup_options = dict(
    name='django_rediscache',
    version=version,
    description=about.split('\n')[0],
    author_email='linkofwise@gmail.com',
    author='Michael Vorotyntsev',
    maintainer_email='linkofwise@gmail.com',
    packages=['django_rediscache'],
    long_description=about,
    include_package_data=True,
)

requires = (
    str('redis>=2.4.13'),
)
try:
    from setuptools import setup
    setup_options.update({
        str('install_requires'): requires})
except ImportError:
    from distutils.core import setup
    setup_options.update({
        str('requires'): requires})

setup(**setup_options)
