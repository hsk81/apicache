#!/usr/bin/env python
###############################################################################

import ARGs
import argparse
import bottle
import importlib
import os
import sys

###############################################################################
###############################################################################

PYCART_DIR = "".join (['python-', '.'.join (map (str, sys.version_info[:2]))])

###############################################################################
###############################################################################

try:
    zvirtenv = os.path.join (os.environ.get ('OPENSHIFT_HOMEDIR', '.'),
        PYCART_DIR, 'virtenv', 'bin', 'activate_this.py')
    exec (compile (open (zvirtenv).read (), zvirtenv, 'exec'), dict(
        __file__=zvirtenv))
except IOError:
   pass

###############################################################################
###############################################################################

## IMPORTANT: Put any additional includes below this line!

###############################################################################
###############################################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser (
        description="""API Cache Service""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--api0-url', metavar='API0_URL',
        default=os.environ.get('API0_URL', 'http://localhost'),
        help='API#0 URL')
    parser.add_argument('--api0-key-name', metavar='API0_KEY_NAME',
        default=os.environ.get('API0_KEY_NAME'),
        help='API#0 key name')
    parser.add_argument('--api0-key-value', metavar='API0_KEY_VALUE',
        default=os.environ.get('API0_KEY_VALUE'),
        help='API#0 key value')
    parser.add_argument('--api0-expiry', metavar='API0_EXPIRY',
        default=os.environ.get('API0_EXPIRY', 900), ## 15 minutes
        help='API#0 expiry of cache in seconds', type=int)

    parser.add_argument('--api1-url', metavar='API1_URL',
        default=os.environ.get('API1_URL', 'http://localhost'),
        help='API#1 URL')
    parser.add_argument('--api1-key-name', metavar='API1_KEY_NAME',
        default=os.environ.get('API1_KEY_NAME'),
        help='API#1 key name')
    parser.add_argument('--api1-key-value', metavar='API1_KEY_VALUE',
        default=os.environ.get('API1_KEY_VALUE'),
        help='API#1 key value')
    parser.add_argument('--api1-expiry', metavar='API1_EXPIRY',
        default=os.environ.get('API1_EXPIRY', 900), ## 15 minutes
        help='API#1 expiry of cache in seconds', type=int)

    parser.add_argument('--api2-url', metavar='API2_URL',
        default=os.environ.get('API2_URL', 'http://localhost'),
        help='API#2 URL')
    parser.add_argument('--api2-key-name', metavar='API2_KEY_NAME',
        default=os.environ.get('API2_KEY_NAME'),
        help='API#2 key name')
    parser.add_argument('--api2-key-value', metavar='API2_KEY_VALUE',
        default=os.environ.get('API2_KEY_VALUE'),
        help='API#2 key value')
    parser.add_argument('--api2-expiry', metavar='API2_EXPIRY',
        default=os.environ.get('API2_EXPIRY', 900), ## 15 minutes
        help='API#2 expiry of cache in seconds', type=int)

    parser.add_argument('--api3-url', metavar='API3_URL',
        default=os.environ.get('API3_URL', 'http://localhost'),
        help='API#3 URL')
    parser.add_argument('--api3-key-name', metavar='API3_KEY_NAME',
        default=os.environ.get('API3_KEY_NAME'),
        help='API#3 key name')
    parser.add_argument('--api3-key-value', metavar='API3_KEY_VALUE',
        default=os.environ.get('API3_KEY_VALUE'),
        help='API#3 key value')
    parser.add_argument('--api3-expiry', metavar='API3_EXPIRY',
        default=os.environ.get('API3_EXPIRY', 900), ## 15 minutes
        help='API#3 expiry of cache in seconds', type=int)

    parser.add_argument('--api4-url', metavar='API4_URL',
        default=os.environ.get('API4_URL', 'http://localhost'),
        help='API#4 URL')
    parser.add_argument('--api4-key-name', metavar='API4_KEY_NAME',
        default=os.environ.get('API4_KEY_NAME'),
        help='API#4 key name')
    parser.add_argument('--api4-key-value', metavar='API4_KEY_VALUE',
        default=os.environ.get('API4_KEY_VALUE'),
        help='API#4 key value')
    parser.add_argument('--api4-expiry', metavar='API4_EXPIRY',
        default=os.environ.get('API4_EXPIRY', 900), ## 15 minutes
        help='API#4 expiry of cache in seconds', type=int)

    parser.add_argument('--api5-url', metavar='API5_URL',
        default=os.environ.get('API5_URL', 'http://localhost'),
        help='API#5 URL')
    parser.add_argument('--api5-key-name', metavar='API5_KEY_NAME',
        default=os.environ.get('API5_KEY_NAME'),
        help='API#5 key name')
    parser.add_argument('--api5-key-value', metavar='API5_KEY_VALUE',
        default=os.environ.get('API5_KEY_VALUE'),
        help='API#5 key value')
    parser.add_argument('--api5-expiry', metavar='API5_EXPIRY',
        default=os.environ.get('API5_EXPIRY', 900), ## 15 minutes
        help='API#5 expiry of cache in seconds', type=int)

    parser.add_argument('--api6-url', metavar='API6_URL',
        default=os.environ.get('API6_URL', 'http://localhost'),
        help='API#6 URL')
    parser.add_argument('--api6-key-name', metavar='API6_KEY_NAME',
        default=os.environ.get('API6_KEY_NAME'),
        help='API#6 key name')
    parser.add_argument('--api6-key-value', metavar='API6_KEY_VALUE',
        default=os.environ.get('API6_KEY_VALUE'),
        help='API#6 key value')
    parser.add_argument('--api6-expiry', metavar='API6_EXPIRY',
        default=os.environ.get('API6_EXPIRY', 900), ## 15 minutes
        help='API#6 expiry of cache in seconds', type=int)

    parser.add_argument('--api7-url', metavar='API7_URL',
        default=os.environ.get('API7_URL', 'http://localhost'),
        help='API#7 URL')
    parser.add_argument('--api7-key-name', metavar='API7_KEY_NAME',
        default=os.environ.get('API7_KEY_NAME'),
        help='API#7 key name')
    parser.add_argument('--api7-key-value', metavar='API7_KEY_VALUE',
        default=os.environ.get('API7_KEY_VALUE'),
        help='API#7 key value')
    parser.add_argument('--api7-expiry', metavar='API7_EXPIRY',
        default=os.environ.get('API7_EXPIRY', 900), ## 15 minutes
        help='API#7 expiry of cache in seconds', type=int)

    parser.add_argument ('--host', metavar='HOST',
        default=os.environ.get ('OPENSHIFT_PYTHON_IP', 'localhost'),
        help='Host to listen on')
    parser.add_argument ('--port', metavar='PORT', type=int,
        default=os.environ.get ('OPENSHIFT_PYTHON_PORT', 8080),
        help='Port to listen on')

    parser.add_argument ('--memcached-servers', metavar='MEMCACHED_SERVERS',
        default=os.environ.get ('MEMCACHED_SERVERS', 'localhost:11211'),
        help='Memcached server(s)')
    parser.add_argument ('--memcached-username', metavar='MEMCACHED_USERNAME',
        default=os.environ.get ('MEMCACHED_USERNAME', None),
        help='Memcached username')
    parser.add_argument ('--memcached-password', metavar='MEMCACHED_PASSWORD',
        default=os.environ.get ('MEMCACHED_PASSWORD', None),
        help='Memcached password')
    parser.add_argument ('--memcached-flush', action='store_true',
        default=os.environ.get ('MEMCACHED_FLUSH', False),
        help='Memcached flush flag')

    parser.add_argument ('--redis-host', metavar='REDIS_HOSTNAME',
        default=os.environ.get ('REDIS_HOSTNAME', 'localhost'),
        help='Redis host')
    parser.add_argument ('--redis-port', metavar='REDIS_PORT',
        default=os.environ.get ('REDIS_PORT', 6379),
        help='Redis port', type=int)
    parser.add_argument ('--redis-password', metavar='REDIS_PASSWORD',
        default=os.environ.get ('REDIS_PASSWORD', None),
        help='Redis password')
    parser.add_argument ('--redis-flush-db', metavar='REDIS_FLUSH_DB',
        default=os.environ.get ('REDIS_FLUSH_DB', None), type=list,
        help='Redis DB(s) to flush', const=map (str, range (1)), nargs='?')

    parser.add_argument ('-d', '--debug',
        default=os.environ.get ('DEBUG', False),
        help='Debug flag', action='store_true')
    parser.add_argument ('-r', '--reload',
        default=os.environ.get ('RELOAD', False),
        help='Reload flag', action='store_true')
    parser.add_argument ('-w', '--wsgi',
        default=os.environ.get ('WSGI', 'waitress'),
        help='WSGI server to use', metavar='WSGI')

    ARGs.put (parser.parse_args ())

    wsgi = importlib.import_module ('wsgi')
    bottle.run (app=wsgi.application, server=ARGs.get ('wsgi'),
        host=ARGs.get ('host'), port=ARGs.get ('port'),
        debug=ARGs.get ('debug'), reloader=ARGs.get ('reload'))

###############################################################################
###############################################################################
