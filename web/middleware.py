import mimeparse

from http import HTTP, HTTPException


class Negotiator(object):
    """
    extend WSGI environment with information from simple content negotiation
    """

    def __init__(self, app, types_available):
        self.types_available = types_available # XXX: rename!?
        self.app = app

    def __call__(self, environ, start_response, exc_info=None):
        environ['wsgi.accepted_type'] = self._determine(environ) # XXX: bad key? (could also use incoming_type, for GET only)
        return self.app(environ, start_response)

    def _determine(self, environ): # XXX: rename? -- XXX: overly simplistic? (cf. tiddlyweb.web.negotiate)
        method = environ['REQUEST_METHOD'].upper()
        accept_header = environ.get('HTTP_ACCEPT')
        content_type = environ.get('CONTENT_TYPE')

        if method == 'GET':
            return mimeparse.best_match(self.types_available, accept_header)
        elif content_type:
            return content_type.split(';')[0]
        else:
            return None


class HTTPExceptor(object):
    """
    WSGI middleware handling HTTP errors
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response, exc_info=None):
        try:
            return self.app(environ, start_response)
        except HTTPException, exc:
            start_response(HTTP[exc.status], exc.headers(), exc_info)
            return exc.output()


class UTF8_Encoder(object):
    """
    ensure that outgoing content is UTF-8
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response, exc_info=None):

        def _start_response(status, headers, exc_info=None):
            """
            add charset to Content-Type header if necessary
            """
            for i, header in enumerate(headers):
                if header[0].lower() == 'content-type' and ';' not in header[1]:
                    headers[i] = (header[0], '%s; charset=utf-8' % header[1])
            return start_response(status, headers, exc_info)

        for chunk in self.app(environ, _start_response):
            try:
                yield chunk.encode('utf-8')
            except UnicodeDecodeError, exc:
                yield chunk
