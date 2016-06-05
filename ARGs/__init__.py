__author__ = 'hsk81'

###############################################################################
###############################################################################

def put (namespace):
    global _ARGs; _ARGs = dict (namespace._get_kwargs ())

def get (key, default=None):
    global _ARGs

    if '_ARGs' not in globals ():
        _ARGs = {}

    return _ARGs.get (key, default)

###############################################################################

def debug (*args, **kwargs):
    return get ('debug')

###############################################################################
###############################################################################
