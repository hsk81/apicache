#!/usr/bin/env python
###############################################################################

from bottle import Bottle, request, response

import ARGs
import requests
import os.path
import apicache.cache as cache

###############################################################################
###############################################################################

app_api = Bottle()
app = app_api

###############################################################################
###############################################################################

@app.get('/rdb/<rdb_index:int>/<path:path>')
def api_rdb_n(rdb_index, path):

    rdb = getattr(cache, 'redis_plugin_{0}'.format(rdb_index))
    idx = int(request.query.get('api-index', 0))
    exp = request.query.get(
        'api{0}-expiry'.format(idx), ARGs.get('api{0}_expiry'.format(idx)))

    @rdb.memoize(expiry=exp, name='view.rdb', unless=lambda: ARGs.debug())
    def memoized(*args, **kwargs):

        if request.auth:
            auth = request.auth
        else:
            auth_user = ARGs.get('api{0}_user'.format(idx))
            auth_pass = ARGs.get('api{0}_pass'.format(idx))
            auth = (auth_user, auth_pass) if auth_user else None

        key_name = request.query.get(
            'api{0}-key-name'.format(idx),
            ARGs.get('api{0}_key_name'.format(idx)))
        key_value = request.query.get(
            'api{0}-key-value'.format(idx),
            ARGs.get('api{0}_key_value'.format(idx)))
        api_url = request.query.get(
            'api{0}-url'.format(idx),
            ARGs.get('api{0}_url'.format(idx)))

        if key_name and key_value:
            request.query[key_name] = key_value

        res = requests.get(
            os.path.join(api_url, path), auth=auth, params=request.query)
        res.raise_for_status()

        return res.text

    response.content_type = 'application/json; charset=utf-8'
    return memoized(path, request.query_string)

@app.get('/rdb/<path:path>')
def api_rdb_i(path):

    return api_rdb_n(0, path)

@app.get('/mdb/<path:path>')
def api_mdb_i(path):

    mdb = getattr(cache, 'memcached_plugin')
    idx = int(request.query.get('api-index', 0))
    exp = request.query.get(
        'api{0}-expiry'.format(idx), ARGs.get('api{0}_expiry'.format(idx)))

    @mdb.memoize(expiry=exp, name='view.mdb', unless=lambda: ARGs.debug())
    def memoized(*args, **kwargs):

        if request.auth:
            auth = request.auth
        else:
            auth_user = ARGs.get('api{0}_user'.format(idx))
            auth_pass = ARGs.get('api{0}_pass'.format(idx))
            auth = (auth_user, auth_pass) if auth_user else None

        key_name = request.query.get(
            'api{0}-key-name'.format(idx),
            ARGs.get('api{0}_key_name'.format(idx)))
        key_value = request.query.get(
            'api{0}-key-value'.format(idx),
            ARGs.get('api{0}_key_value'.format(idx)))
        api_url = request.query.get(
            'api{0}-url'.format(idx),
            ARGs.get('api{0}_url'.format(idx)))

        if key_name and key_value:
            request.query[key_name] = key_value

        res = requests.get(
            os.path.join(api_url, path), auth=auth, params=request.query)
        res.raise_for_status()

        return res.text

    response.content_type = 'application/json; charset=utf-8'
    return memoized(path, request.query_string)

@app.get('/<path:path>')
def api_mdb(path):

    return api_mdb_i(path)

###############################################################################
###############################################################################
