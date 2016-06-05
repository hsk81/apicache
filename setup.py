#!/usr/bin/env python
###############################################################################

from setuptools import setup

###############################################################################
###############################################################################

setup (
    name='api-cache',
    version='0.0.1',
    description='API Cache Service(s)',
    author='Hasan Karahan',
    author_email='hasan.karahan@blackhan.com',
    url='git@bitbucket.org:hsk81/api-cache.git',
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
