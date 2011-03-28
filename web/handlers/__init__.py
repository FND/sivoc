import sys
import itertools

import serialization.text

from web.http import HTTP, HTTP404
from config import CONFIG
from store import STORE


def get_root(environ, start_response):
    response_headers = [('Content-Type', 'text/plain')]
    start_response(HTTP['200'], response_headers)
    return ('Welcome.',)


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
