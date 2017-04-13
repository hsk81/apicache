#!/usr/bin/env python
###############################################################################

from setuptools import setup

###############################################################################
###############################################################################

setup (
    name='apicache',
    version='1.0.0',
    description='API Cache Service(s)',
    author='Hasan Karahan',
    author_email='hasan.karahan@blackhan.com',
    url='https://github.com/hsk81/apicache',
    install_requires=[
        'bottle>=0.12.13',
        'python-binary-memcached>=0.26.0',
        'requests>=2.13.0',
        'redis>=2.10.5',
        'waitress>=1.0.2',
        'Werkzeug>=0.12.1'
    ],
)

###############################################################################
###############################################################################
