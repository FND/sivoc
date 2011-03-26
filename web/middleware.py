class UTF8_Encoder(object):
    """
    ensure that outgoing content is UTF-8
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        def _start_response(status, headers, exc_info=None):
            """
            add charset to Content-Type header if necessary
            """
            for i, header in enumerate(headers):
                if header[0].lower() == "content-type" and ";" not in header[1]:
                    headers[i] = (header[0], "%s; charset=utf-8" % header[1])
            return start_response(status, headers, exc_info)

        for chunk in self.app(environ, _start_response):
            try:
                yield chunk.encode('utf-8')
            except UnicodeDecodeError:
                yield chunk
