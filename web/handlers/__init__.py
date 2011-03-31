import sys
import itertools

import serialization.text

from bson.objectid import ObjectId # XXX: is this really required? (breaks encapsulation)

from web.http import HTTP, HTTP404
from config import CONFIG
from store import STORE


def list_concepts(environ, start_response):
    concepts = STORE.retrieve('concepts')

    content_type = environ['wsgi.accepted_type']

    response_headers = [('Content-Type', content_type)]
    start_response(HTTP['200'], response_headers)

    return _serializer(content_type).list_concepts(concepts)


def list_labels(environ, start_response):
    labels = [] # XXX: inefficient; laziness (i.e. a generator) would be preferable here
    for concept in STORE.retrieve('concepts', None, { 'labels': 1 }):
        labels.extend(concept.pref_labels + concept.alt_labels) # TODO: eliminate duplicates

    content_type = environ['wsgi.accepted_type']

    response_headers = [('Content-Type', content_type)]
    start_response(HTTP['200'], response_headers)

    return _serializer(content_type).list_labels(labels)


def get_concept(environ, start_response):
    _id = environ['wsgiorg.routing_args'][1]['id']

    concepts = STORE.retrieve('concepts', { '_id': ObjectId(_id) })
    concept = list(concepts)[0] # XXX: not particularly elegant

    if not concept:
        raise HTTP404('no such concept')

    content_type = environ['wsgi.accepted_type']

    response_headers = [('Content-Type', content_type)]
    start_response(HTTP['200'], response_headers)

    return _serializer(content_type).show_concept(concept)


def _serializer(content_type):
    serializer = CONFIG['serializations'][content_type]
    __import__(serializer)
    return sys.modules[serializer]
