#!/usr/bin/env python
###############################################################################

from api_cache.app import app_main
from werkzeug.debug import DebuggedApplication

import ARGs

###############################################################################
###############################################################################

application = app_main

###############################################################################

if ARGs.get ('debug'):
    application.catchall = False
    application = DebuggedApplication(
        application, evalex=True, pin_security=True)

###############################################################################
###############################################################################
