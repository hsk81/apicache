#!/usr/bin/env python
###############################################################################

from setuptools import setup

###############################################################################
###############################################################################

setup (
    name='apicache',
    version='0.0.2',
    description='API Cache Service(s)',
    author='Hasan Karahan',
    author_email='hasan.karahan@blackhan.com',
    url='https://github.com/hsk81/apicache',
    install_requires=[
        'bottle>=0.12.9',
        'python-binary-memcached>=0.24.6',
        'requests>=2.9.1',
        'redis>=2.10.5',
        'waitress>=0.9.0',
        'Werkzeug>=0.11.5'
    ],
)

###############################################################################
###############################################################################
