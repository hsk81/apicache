# API Caching Service

Enables caching of responses for requests to up to 8 different back-end API services.

Any incoming request is forwarded one-to-one to a via an `api-index` addressed service, where if configured an API key is attached to the outgoing request.

The response is then cached using either `memcached` or `redis`, where the expiration time can be configured as well.

## Command line arguments
```
$ ./app.py --help
```

Typing the command above will produce a short description and a listing of the command line arguments, which have been grouped below. Almost each argument can also be set via an environment variable.

### Back-end API service

For each back-end API service up to four arguments can be set, where per service only the URL ()configurable via `api{n}-url`) would be required. If the services mandates an API key, then setting up `api{n}-key-name` and `api{n}-key-value` will do the job. Further, with `api{n}-expiry` the expiration time in in seconds can be controlled.

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

If no caching service is indicated at request time, then by default `memcached` will be attempted to be used: However if no such cache is present, then the response will directly be send to the originator without caching and without throwing errors:

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

These two parameters are strongly recommended to be left switch of during production, since they are meant to be used during development:
```
-d, --debug           Debug flag (default: False)
-r, --reload          Reload flag (default: False)
```

### WSGI server

The default WSGI server `waitress` is a relatively slow but purely in Python written and easy to install application container. However external ones can also be used by facilitating the argument below (if the external server has been correctly installed in the run-time environment and is a drop-in replacement for the default):

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

```bash
curl localhost:8080/my/query?my=parameters
```

Query the API caching service running on `localhost:8080`, where the `my/query?my=parameters` path is forwarded with the request to the back-end service `#1` (indicated by `api-index=1`). The response is explicitly cached using `memcached`:

```bash
curl localhost:8080/mdb/my/query?my=parameters&api-index=1
```

Query the API caching service running on `localhost:8080`, where the `my/query?my=parameters` path is forwarded with the request to the back-end service `#2` (indicated by `api-index=2`). The response is explicitly cached using `redis` (implicitly it's first database `#0`):

```bash
curl localhost:8080/rdb/my/query?my=parameters&api-index=2
```

Query the API caching service running on `localhost:8080`, where the `my/query?my=parameters` path is forwarded with the request to the back-end service `#3` (indicated by `api-index=3`). The response is explicitly cached using `redis` (but this time implicitly on it's second database `#1`):

```bash
curl localhost:8080/rdb/1/my/query?my=parameters&api-index=3;
```

Query the API caching service running on `localhost:8080`, where the `my/query?my=parameters` path is forwarded with the request to the default back-end service `#0`. But to set the API key the parameter `API_KEY=KEY_VALUE` is attached to the outgoing request URL:

```bash
curl localhost:8080/my/query?my=parameters&api-key-name=API_KEY&api-key-value=KEY_VALUE;
```
