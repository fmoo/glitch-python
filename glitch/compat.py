try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import logging
        logging.error("json or simplejson are required to run this")
        raise
