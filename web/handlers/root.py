from web.http import HTTP, HTTP406
from templates import ENV


def get_root(environ, start_response):
    content_type = environ['wsgi.accepted_type']
    if content_type != 'text/html': # only works if HTML serializer is available
        raise HTTP406

    response_headers = [('Content-Type', content_type)]
    start_response(HTTP['200'], response_headers)

    template = ENV.get_template('index.html')
    return template.generate(title="Sivoc")
