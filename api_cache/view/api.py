#!/usr/bin/env python
###############################################################################

from bottle import Bottle, request, response

import ARGs
import requests
import os.path
import api_cache.cache

###############################################################################
###############################################################################

app_api = Bottle()
app = app_api

###############################################################################
###############################################################################

@app.get('/rdb/<rdb_index:int>/<path:path>')
def api_rdb_n(rdb_index, path):

    rdb = getattr(api_cache.cache, 'redis_plugin_{0}'.format(rdb_index))
    @rdb.memoize(expiry=ARGs.get('api_expiry'), name='view.api',
                 unless=lambda: ARGs.debug())
    def memoized(*args, **kwargs):
        api_index = int(request.query.get('api-index', 0))
        key_name = \
            ARGs.get('api{0}_key_name'.format(api_index),
                     request.query.get('api{0}-key-name'.format(api_index)))
        key_value = \
            ARGs.get('api{0}_key_value'.format(api_index),
                     request.query.get('api{0}-key-value'.format(api_index)))
        api_url = \
            ARGs.get('api{0}_url'.format(api_index),
                     request.query.get('api{0}-url'.format(api_index)))

        if key_name and key_value: request.query[key_name] = key_value
        res = requests.get(os.path.join(api_url, path), params=request.query)
        res.raise_for_status()

        return res.text

    response.content_type = 'application/json; charset=utf-8'
    return memoized(path, request.query_string)

@app.get('/rdb/<path:path>')
def api_rdb_i(path):

    return api_rdb_n(0, path)

@app.get('/mdb/<path:path>')
def api_mdb_i(path):

    mdb = getattr(api_cache.cache, 'memcached_plugin',)
    @mdb.memoize(expiry=ARGs.get('api_expiry'), name='view.api',
                 unless=lambda: ARGs.debug())
    def memoized(*args, **kwargs):
        api_index = int(request.query.get('api-index', 0))
        key_name = \
            ARGs.get('api{0}_key_name'.format(api_index),
                     request.query.get('api{0}-key-name'.format(api_index)))
        key_value = \
            ARGs.get('api{0}_key_value'.format(api_index),
                     request.query.get('api{0}-key-value'.format(api_index)))
        api_url = \
            ARGs.get('api{0}_url'.format(api_index),
                     request.query.get('api{0}-url'.format(api_index)))

        if key_name and key_value: request.query[key_name] = key_value
        res = requests.get(os.path.join(api_url, path), params=request.query)
        res.raise_for_status()

        return res.text

    response.content_type = 'application/json; charset=utf-8'
    return memoized(path, request.query_string)

@app.get('/<path:path>')
def api_mdb(path):

    return api_mdb_i(path)

###############################################################################
###############################################################################
