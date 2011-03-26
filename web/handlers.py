import itertools

from web.util import HTTP
from store import STORE


def get_root(environ, start_response):
    status = HTTP['200']
    response_headers = [('Content-Type', 'text/plain')]

    start_response(status, response_headers)

    return ('Welcome.',)


def list_concepts(environ, start_response):
    concepts = STORE.concepts.items()

    status = '200' if len(concepts) > 0 else '404' # TODO: raise 404 as exception (cf. TiddlyWeb)
    response_headers = [('Content-Type', 'text/plain')]
    start_response(HTTP[status], response_headers)

    return ("%s\n" % concept.label().name for _id, concept in concepts)


def get_concept(environ, start_response):
    response_headers = [('Content-Type', 'text/plain')]

    _id = environ['wsgiorg.routing_args'][1]['id']
    try:
        concept = STORE.concepts[_id]
        status = '200'
    except IndexError:
        status = '404' # TODO: raise 404 as exception (cf. TiddlyWeb)

    start_response(HTTP[status], response_headers)

    labels = itertools.chain(concept.pref_labels, ["separator"], # XXX: use of separator hacky
            concept.alt_labels)

    return ("%s\n" % getattr(label, "name", "") for label in labels)
