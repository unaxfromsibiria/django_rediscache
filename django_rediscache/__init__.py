# -*- coding: utf-8 -*-
VERSION = (1, 0, 5)

import os

if os.environ.get('DJANGO_SETTINGS_MODULE'):
    from .setup import install
    install()
