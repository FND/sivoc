from web.util import HTTP


def get_root(environ, start_response):
    status = HTTP[200]
    response_headers = [('Content-Type', 'text/plain')]

    start_response(status, response_headers)

    return ('Welcome.',)
