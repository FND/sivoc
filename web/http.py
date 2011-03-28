import httplib


# dictionary of canonical HTTP responses (status code plus reason phrase)
HTTP = dict((str(code), '%s %s' % (code, httplib.responses[code]))
        for code in httplib.responses)


class HTTPException(Exception):
    """
    base class of an HTTP exception

    headers method's return value is a list of tuples, used for the
    corresponding WSGI start_response argument

    output method's return value is an iterator, used as WSGI application's
    return value
    """

    status = None

    def __init__(self, msg=None):
        self.msg = '\n\n%s' % msg if msg else ''

    def headers(self):
        return [('Content-Type', 'text/plain')]

    def output(self):
        return (HTTP[self.status], self.msg)


class HTTP404(HTTPException):
    status = '404'


class HTTP406(HTTPException):
    status = '406'


class HTTP415(HTTPException):
    status = '415'
