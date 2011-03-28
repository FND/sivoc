import sys
import itertools

import serialization.text

try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

from web.http import HTTP, HTTP404, HTTP415
from config import CONFIG
from store import STORE


def get_root(environ, start_response):
    response_headers = [('Content-Type', 'text/plain')]
    start_response(HTTP['200'], response_headers)
    return ('Welcome.',)


def get_conceptcreator(environ, start_response):
    # XXX: nested imports evil!?
    from model.concept import Concept
    from templates import ENV

    response_headers = [('Content-Type', 'text/html')]
    start_response(HTTP['200'], response_headers)
    template = ENV.get_template('edit_concept.html')
    return template.generate(title='Concept Creator', concept=Concept(),
            form_uri=environ['SCRIPT_NAME']) # XXX: SCRIPT_NAME correct?


def post_conceptcreator(environ, start_response):
    # XXX: nested imports evil!?
    from model.concept import Concept
    from model.label import Label
    from store import STORE

    content_type = environ.get('CONTENT_TYPE', '')
    if not content_type == 'application/x-www-form-urlencoded': # XXX: TiddlyWeb uses startswith here!?
        raise HTTP415

    # TODO: this might be encapsulated in middleware (cf. tiddlyweb.web.query)
    content_length = int(environ['CONTENT_LENGTH'] or 0)
    content = environ['wsgi.input'].read(content_length)
    data = parse_qs(content, keep_blank_values=True)

    concept = Concept()
    # TODO: label language (input/selection currently missing from HTML template)
    for name in data['pref_labels']:
        label = Label(name, lang=None)
        concept.pref_labels.append(label)
    for name in data['alt_labels']:
        label = Label(name, lang=None)
        concept.alt_labels.append(label)

    _id = STORE.add(concept)

    response_headers = [('Location', '/concepts/%s' % concept._id)]
    start_response(HTTP['302'], response_headers)
    return ['']


def list_concepts(environ, start_response):
    concepts = STORE.concepts.items()

    if len(concepts) > 0: # XXX: checking length kinda defeats the purpose of using generators
        concepts = (concept for _id, concept in concepts)
    else:
        raise HTTP404('no concepts available')

    content_type = environ['wsgi.accepted_type']

    response_headers = [('Content-Type', content_type)]
    start_response(HTTP['200'], response_headers)

    return _serializer(content_type).list_concepts(concepts)


def get_concept(environ, start_response):
    _id = int(environ['wsgiorg.routing_args'][1]['id'])
    try:
        concept = STORE.concepts[_id]
    except KeyError, exc:
        raise HTTP404('no such concept')

    content_type = environ['wsgi.accepted_type']

    response_headers = [('Content-Type', content_type)]
    start_response(HTTP['200'], response_headers)

    return _serializer(content_type).show_concept(concept)


def _serializer(content_type):
    serializer = CONFIG['serializations'][content_type]
    __import__(serializer)
    return sys.modules[serializer]
