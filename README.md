# API Caching Service

Enables response caching of requests for up to eight different back-end API services.

Any incoming request is forwarded one-to-one to a via an `api-index` addressed service, where if configured an API key is attached to the outgoing request. The response is then cached using either `memcached` or `redis`, where the expiration time can be configured as well.

## Installation
Setup `virtualenv` environment: requires `virtualenv2` with `python2`!
```
./scripts/setup.sh
```
Switch to `virtualenv` environment:
```
source bin/activate
```
Install `python` dependencies:
```
./setup.py
```

## Running
```
./app.py --api0-url=$API0_URL \
         --api0-key-name=$API0_KEY_NAME \
         --api0-key-value=$API0_KEY_VALUE \
         --api0-expiry=$API0_EXPIRY
```

* Where `$API0_URL` is the URL of the back-end service you want to cache for,

* `$API0_KEY_NAME` is the query parameter name for the API key (depends on the service),

* `$API0_KEY_VALUE` is the parameter value for the API key (depends on your account credentials) and

* `$API0_EXPIRY` is the default expiration time in seconds for the returned responses (depends on your judgment).

## Command line arguments
```
./app.py --help
```

Typing the command above will produce a short description and a listing of the command line arguments, which have been grouped below. Almost each argument can also be set via an environment variable.

### Back-end API service

For each back-end API service up to four arguments can be set, where per service only the URL (configurable via `api{n}-url`) is required. If the services mandates an API key, then setting up `api{n}-key-name` and `api{n}-key-value` will be sufficient. Further, with `api{n}-expiry` the expiration time in in seconds can be controlled.

```
--api0-url API0_URL   API#0 URL (default: http://localhost)
--api0-key-name API0_KEY_NAME
                    API#0 key name (default: None)
--api0-key-value API0_KEY_VALUE
                    API#0 key value (default: None)
--api0-expiry API0_EXPIRY
                    API#0 expiry of cache in seconds (default: 900)

[..]

--api7-url API0_URL   API#0 URL (default: http://localhost)
--api7-key-name API0_KEY_NAME
                    API#0 key name (default: None)
--api7-key-value API0_KEY_VALUE
                    API#0 key value (default: None)
--api7-expiry API0_EXPIRY
                    API#0 expiry of cache in seconds (default: 900)
```

Each of the above arguments can also be set at request time by appending `api{n}-url=$API_URL`, `api{n}-key-name=$API_KEY_NAME`, , `api{n}-key-value=$API_KEY_VALUE`, and `api7-expiry=$API0_EXPIRY` query parameters.

### Memcached

If no caching service is indicated at request time, then by default `memcached` will be used: However if no such cache is present, then the response will directly be sent to the originator without caching and without throwing errors:

```
--memcached-servers MEMCACHED_SERVERS
                    Memcached server(s) (default: localhost:11211)
--memcached-username MEMCACHED_USERNAME
                    Memcached username (default: None)
--memcached-password MEMCACHED_PASSWORD
                    Memcached password (default: None)
--memcached-flush     Memcached flush flag (default: False)
```

### Redis

If the `redis` caching service is indicated at request time, but if no such service has been setup, then the application will throw an exception for the given request:

```
--redis-host REDIS_HOSTNAME
                    Redis host (default: localhost)
--redis-port REDIS_PORT
                    Redis port (default: 6379)
--redis-password REDIS_PASSWORD
                    Redis password (default: None)
--redis-flush-db [REDIS_FLUSH_DB]
                    Redis DB(s) to flush (default: None)
```

### Development

The following two parameters are strongly recommended to be switched off in production, since they are meant to be used only in development:
```
-d, --debug           Debug flag (default: False)
-r, --reload          Reload flag (default: False)
```

### WSGI server

The default WSGI server `waitress` is a relatively slow application container, but written purely in Python and easy to install. It is also possible to use WSGI by passing the argument below (if the external server has been correctly installed in the run-time environment and is a drop-in replacement for the default):

```
-w WSGI, --wsgi WSGI  WSGI server to use (default: waitress)
```

### Host address and port number
```
--host HOST           Host to listen on (default: localhost)
--port PORT           Port to listen on (default: 8080)
```

## Query Examples

Query the API caching service running on `localhost:8080`, where the `my/query?my=parameters` path is forwarded with the request to the default back-end service `#0`. The response is by default cached using `memcached`, with a default `expiration` time:

```
curl localhost:8080/my/query?my=parameters
```

Query the API caching service running on `localhost:8080`, where the `my/query?my=parameters` path is forwarded with the request to the back-end service `#1` (indicated by `api-index=1`). The response is explicitly cached using `memcached`:

```
curl localhost:8080/mdb/my/query?my=parameters&api-index=1
```

Query the API caching service running on `localhost:8080`, where the `my/query?my=parameters` path is forwarded with the request to the back-end service `#2` (indicated by `api-index=2`). The response is explicitly cached using `redis` (implicitly it's the first database `#0`):

```
curl localhost:8080/rdb/my/query?my=parameters&api-index=2
```

Query the API caching service running on `localhost:8080`, where the `my/query?my=parameters` path is forwarded with the request to the back-end service `#3` (indicated by `api-index=3`). The response is explicitly cached using `redis` (with the second database `#1`):

```
curl localhost:8080/rdb/1/my/query?my=parameters&api-index=3
```

Query the API caching service running on `localhost:8080`, where the `my/query?my=parameters` path is forwarded with the request to the default back-end service `#0`. But to set the API key, the parameter `API_KEY=KEY_VALUE` is attached to the outgoing request URL:

```
curl localhost:8080/my/query?my=parameters&api-key-name=API_KEY&api-key-value=KEY_VALUE
```
