__author__ = 'hsk81'

###############################################################################
###############################################################################

from bottle import Bottle
from .view.debug import app_debug
from .view.api import app_api
from .view.now import app_now

import ARGs

###############################################################################
###############################################################################

app_main = Bottle()
app_main.merge(app_api)
app_main.merge(app_now)

if ARGs.get('debug'):
    app_main.merge(app_debug)

###############################################################################
###############################################################################
