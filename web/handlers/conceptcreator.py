try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

from model.concept import Concept
from model.label import Label
from web.http import HTTP, HTTP415
from templates import ENV
from store import STORE


def get_creator(environ, start_response):
    response_headers = [('Content-Type', 'text/html')]
    start_response(HTTP['200'], response_headers)
    template = ENV.get_template('edit_concept.html')
    return template.generate(title='Concept Creator', concept=Concept(),
            root_uri='/', # XXX: root_uri hardcoded; breaks encapsulation
            form_uri=environ['SCRIPT_NAME']) # XXX: SCRIPT_NAME correct?


def post_creator(environ, start_response):
    content_type = environ.get('CONTENT_TYPE', '')
    if not content_type == 'application/x-www-form-urlencoded': # XXX: TiddlyWeb uses startswith here!?
        raise HTTP415

    # TODO: this might be encapsulated in middleware (cf. tiddlyweb.web.query)
    content_length = int(environ['CONTENT_LENGTH'] or 0)
    content = environ['wsgi.input'].read(content_length)
    data = parse_qs(content, keep_blank_values=True)

    concept = Concept()
    # TODO: label language (input/selection currently missing from HTML template)
    for label_type in ['pref', 'alt']:
        key = '%s_labels' % label_type
        for name in data[key]:
            if name:
                label = Label(name, lang=None)
                getattr(concept, key).append(label)

    _id = STORE.add(concept)

    response_headers = [('Location', '/concepts/%s' % concept._id)]
    start_response(HTTP['302'], response_headers)
    return ['']
