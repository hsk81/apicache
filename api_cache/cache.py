__author__ = 'hsk81'

###############################################################################
###############################################################################

import ARGs
import abc
import bottle
import bmemcached
import functools
import hashlib
import inspect
import redis

###############################################################################
###############################################################################

class ApiCache (object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def NEVER (self): return
    @abc.abstractproperty
    def ASAP (self): return

    @abc.abstractmethod
    def get (self, key): return
    @abc.abstractmethod
    def set (self, key, value, expiry=None): pass
    @abc.abstractmethod
    def delete (self, key): pass
    @abc.abstractmethod
    def expire (self, key, expiry=None): pass
    @abc.abstractmethod
    def exists (self, key): return
    @abc.abstractmethod
    def flush_all (self): pass

    ###########################################################################

    @staticmethod
    def make_key (*args, **kwargs):

        kwargs.update (
            dict (map (lambda t: (str (t[0]), t[1]), enumerate (args))))
        string = repr (sorted (kwargs.items ())).encode('utf-8')
        hashed = hashlib.md5 (string)

        return hashed.hexdigest ()

    def prefixed (self, key):
        return self.KEY_PREFIX + key

    KEY_PREFIX = 'cache:'

    ###########################################################################

    def cached (self, expiry=None, name=None, keyfunc=None,
                unless=None, lest=None):

        if expiry is None:
            expiry = self.NEVER
        if not callable (keyfunc):
            keyfunc = lambda sid, fn, *args, **kwargs: \
                self.make_key (sid, name or fn.__name__) ## no (kw)args!

        return self.memoize (expiry, name, keyfunc, unless, lest)

    def memoize (self, expiry=None, name=None, keyfunc=None,
                 unless=None, lest=None):

        if expiry is None:
            expiry = self.NEVER
        if not callable (keyfunc):
            keyfunc = self.make_key

        def decorator (fn):
            @functools.wraps (fn)
            def decorated (*args, **kwargs):

                if callable (unless) and unless ():
                    return fn (*args, **kwargs)
                if callable (lest) and lest (*args, **kwargs):
                    return fn (*args, **kwargs)

                value_key = keyfunc (name or fn.__name__, *args, **kwargs)
                cached_value = self.get (value_key)

                if cached_value is None:
                    cached_value = fn (*args, **kwargs)
                    self.set (value_key, cached_value, expiry=expiry)

                return cached_value

            decorated.uncached = fn
            decorated.expiry = expiry

            return decorated
        return decorator

###############################################################################

class ApiMemcachedPlugin (ApiCache):

    @property
    def NEVER (self):
        return 0
    @property
    def ASAP (self):
        return None

    def __init__ (self, servers, username=None, password=None, keyword='mdb'):

        self.servers = servers
        self.username = username
        self.password = password
        self.keyword = keyword

    def setup (self, app):

        for plugin in app.plugins:
            if not isinstance (plugin, ApiMemcachedPlugin):
                continue
            if plugin.keyword == self.keyword:
                raise bottle.PluginError ('conflicting plugins')

    def apply (self, callback, route):

        config = route.config
        if 'memcached' in config:
            get_config = lambda k, d: config.get ('memcached', {}).get (k, d)
        else:
            get_config = lambda k, d: config.get ('memcached.' + k, d)

        keyword = get_config ('keyword', self.keyword)
        argspec = inspect.getargspec (route.callback)
        if keyword not in argspec.args: return callback

        def decorator (*args, **kwargs):
            kwargs[keyword] = self
            return callback (*args, **kwargs)

        return decorator

    def get (self, key):
        return self.connection.get (self.prefixed (key))

    def set (self, key, value, expiry=0): ## self.NEVER
        if expiry == self.ASAP:
            self.connection.delete (self.prefixed (key))
        else:
            self.connection.set (self.prefixed (key), value, time=expiry)

    def delete (self, key):
        self.connection.delete (self.prefixed (key))

    def expire (self, key, expiry=None): ## self.ASAP
        if expiry == self.ASAP:
            self.connection.delete (self.prefixed (key))
        else:
            self.connection.set (
                self.prefixed (key), self.connection.get(self.prefixed (key)),
                time=expiry)

    def exists (self, key):
        return self.connection.get (self.prefixed (key)) is not None

    def flush_all (self):
        self.connection.flush_all ()

    ###########################################################################

    @property
    def connection (self):
        if not hasattr (self, '_connection'):
            setattr (self, '_connection', self.connect ())
        return getattr (self, '_connection')

    def connect (self):
        return bmemcached.Client (
            self.servers, username=self.username, password=self.password)

    def close (self):
        if hasattr (self, '_connection'):
            self._connection.disconnect_all ()

###############################################################################

class ApiRedisPlugin (ApiCache):

    name = 'redis'
    api = 2

    @property
    def NEVER (self):
        return None
    @property
    def ASAP (self):
        return 0

    def __init__ (self, host, port=6379, password=None, db=0,
                  keyword='rdb'):

        self.host, self.port = host, port
        self.password, self.db = password, db
        self.keyword = keyword

    def setup (self, app):

        for plugin in app.plugins:
            if not isinstance (plugin, ApiRedisPlugin):
                continue
            if plugin.keyword == self.keyword:
                raise bottle.PluginError ('conflicting plugins')

    def apply (self, callback, route):

        config = route.config
        if 'redis' in config:
            get_config = lambda k, d: config.get ('redis', {}).get (k, d)
        else:
            get_config = lambda k, d: config.get ('redis.' + k, d)

        keyword = get_config ('keyword', self.keyword)
        argspec = inspect.getargspec (route.callback)
        if keyword not in argspec.args: return callback

        def decorator (*args, **kwargs):
            kwargs[keyword] = self
            return callback (*args, **kwargs)

        return decorator

    def get (self, key):
        return self.connection.get (self.prefixed (key))

    def set (self, key, value, expiry=None): ## self.NEVER
        if expiry == self.NEVER:
            self.connection.pipeline ().set (self.prefixed (key), value) \
                .persist (self.prefixed (key)).execute ()
        else:
            self.connection.pipeline ().set (self.prefixed (key), value) \
                .expire (self.prefixed (key), time=expiry).execute ()

    def delete (self, key):
        self.connection.delete (self.prefixed (key))

    def expire (self, key, expiry=0): ## self.ASAP
        if expiry == self.NEVER:
            self.connection.persist (self.prefixed (key))
        else:
            self.connection.expire (self.prefixed (key), time=expiry)

    def exists (self, key):
        return self.connection.exists (self.prefixed (key))

    def flush_all (self):
        self.connection.flushall ()

    ###########################################################################

    @property
    def connection (self):
        if not hasattr (self, '_connection'):
            setattr (self, '_connection', self.connect ())
        return getattr (self, '_connection')

    def connect (self):
        return redis.StrictRedis (
            host=self.host, port=self.port, password=self.password, db=self.db)

    def close (self):
        if hasattr (self, '_connection'):
            pass

###############################################################################

memcached_plugin = ApiMemcachedPlugin(
    servers=ARGs.get('memcached_servers', 'localhost:11211').split(','),
    username=ARGs.get('memcached_username', None),
    password=ARGs.get('memcached_password', None))

if ARGs.get('memcached_flush'):
    memcached_plugin.flush_all()

redis_plugin_0 = ApiRedisPlugin(db=0,
    host=ARGs.get('redis_host', 'localhost'),
    port=ARGs.get('redis_port', 6379),
    password=ARGs.get('redis_password', None))
redis_plugin_1 = ApiRedisPlugin(db=1,
    host=ARGs.get('redis_host', 'localhost'),
    port=ARGs.get('redis_port', 6379),
    password=ARGs.get('redis_password', None))
redis_plugin_2 = ApiRedisPlugin(db=2,
    host=ARGs.get('redis_host', 'localhost'),
    port=ARGs.get('redis_port', 6379),
    password=ARGs.get('redis_password', None))
redis_plugin_3 = ApiRedisPlugin(db=3,
    host=ARGs.get('redis_host', 'localhost'),
    port=ARGs.get('redis_port', 6379),
    password=ARGs.get('redis_password', None))
redis_plugin_4 = ApiRedisPlugin(db=4,
    host=ARGs.get('redis_host', 'localhost'),
    port=ARGs.get('redis_port', 6379),
    password=ARGs.get('redis_password', None))
redis_plugin_5 = ApiRedisPlugin(db=5,
    host=ARGs.get('redis_host', 'localhost'),
    port=ARGs.get('redis_port', 6379),
    password=ARGs.get('redis_password', None))
redis_plugin_6 = ApiRedisPlugin(db=6,
    host=ARGs.get('redis_host', 'localhost'),
    port=ARGs.get('redis_port', 6379),
    password=ARGs.get('redis_password', None))
redis_plugin_7 = ApiRedisPlugin(db=7,
    host=ARGs.get('redis_host', 'localhost'),
    port=ARGs.get('redis_port', 6379),
    password=ARGs.get('redis_password', None))

if ARGs.get('redis_flush_db') is not None:

    if '0' in ARGs.get('redis_flush_db'):
        redis_plugin_0.flush_all ()
    if '1' in ARGs.get('redis_flush_db'):
        redis_plugin_1.flush_all()
    if '2' in ARGs.get('redis_flush_db'):
        redis_plugin_2.flush_all()
    if '3' in ARGs.get('redis_flush_db'):
        redis_plugin_3.flush_all()
    if '4' in ARGs.get('redis_flush_db'):
        redis_plugin_4.flush_all()
    if '5' in ARGs.get('redis_flush_db'):
        redis_plugin_5.flush_all()
    if '6' in ARGs.get('redis_flush_db'):
        redis_plugin_6.flush_all()
    if '7' in ARGs.get('redis_flush_db'):
        redis_plugin_7.flush_all()

###############################################################################
###############################################################################
