# HAX# 1!  app engine dev server ships with a crippled socket library.
# Requests needs this in order to run
import socket
if getattr(socket, 'setdefaulttimeout', None) is None:
    def setdefaulttimeout(timeout):
        socket.timeout = timeout
    socket.setdefaulttimeout = setdefaulttimeout


# HAX #2!  Production app engine ships with a broken urllib2.build_opener.
# Requests needs a less broken one in order to run.
import urllib2
import httplib
def build_opener(*handlers):
    """Create an opener object from a list of handlers.

    The opener will use several default handlers, including support
    for HTTP, FTP and when applicable, HTTPS.

    If any of the handlers passed as arguments are subclasses of the
    default handlers, the default handlers will not be used.
    """
    import types
    def isclass(obj):
        return isinstance(obj, types.ClassType) or hasattr(obj, "__bases__")

    opener = urllib2.OpenerDirector()
    default_classes = [urllib2.ProxyHandler, urllib2.UnknownHandler,
                       urllib2.HTTPHandler,
                       urllib2.HTTPDefaultErrorHandler,
                       urllib2.HTTPRedirectHandler,
                       urllib2.HTTPErrorProcessor]
    if hasattr(httplib, 'HTTPS'):
        default_classes.append(urllib2.HTTPSHandler)
    skip = set()
    for klass in default_classes:
        for check in handlers:
            if isclass(check):
                if issubclass(check, klass):
                    skip.add(klass)
            elif isinstance(check, klass):
                skip.add(klass)
    for klass in skip:
        default_classes.remove(klass)

    for klass in default_classes:
        opener.add_handler(klass())

    for h in handlers:
        if isclass(h):
            h = h()
        opener.add_handler(h)
    return opener
urllib2.build_opener = build_opener
