import sys
import itertools

import serialization.text

from web.util import HTTP
from config import CONFIG
from store import STORE


def get_root(environ, start_response):
    status = HTTP['200']
    response_headers = [('Content-Type', 'text/plain')]

    start_response(status, response_headers)

    return ('Welcome.',)


def list_concepts(environ, start_response):
    concepts = STORE.concepts.items()
    content_type = environ['wsgi.accepted_type']

    if len(concepts) > 0: # XXX: checking length kinda defeats the purpose of using generators
        status = '200'
        concepts = (concept for _id, concept in concepts)
    else:
        status = '404' # TODO: raise 404 as exception (cf. TiddlyWeb)

    response_headers = [('Content-Type', content_type)]
    start_response(HTTP[status], response_headers)

    return _serializer(content_type).list_concepts(concepts)


def get_concept(environ, start_response):
    content_type = environ['wsgi.accepted_type']

    _id = environ['wsgiorg.routing_args'][1]['id']
    try:
        concept = STORE.concepts[_id]
        status = '200'
    except IndexError:
        status = '404' # TODO: raise 404 as exception (cf. TiddlyWeb)

    response_headers = [('Content-Type', content_type)]
    start_response(HTTP[status], response_headers)

    return _serializer(content_type).show_concept(concept)


def _serializer(content_type):
    serializer = CONFIG['serializations'][content_type]
    __import__(serializer)
    return sys.modules[serializer]
