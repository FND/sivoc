from pymongo import Connection

from model.concept import Concept
from model.label import Label


STORE = None # populated below


class Store(object): # XXX: use MongoKit or MongoEngine instead?
    """
    MongoDB persistence wrapper

    document-object mapping is delegated to individual entities
    """

    collections = {
        'Concept': 'concepts'
    }

    def __init__(self, host, port, database):
        self.db = getattr(Connection(host, port), database)

    def retrieve(self, collection, *args, **kwargs):
        """
        collection argument is a string, remaining arguments are passed through
        to PyMongo's `find` method
        """
        if collection not in self.collections.values():
            raise ValueError('invalid collection')

        # XXX: hard-coding concepts for now
        # XXX: association with models is dangerous also because we might query only for a limited selection of fields
        return (Concept().from_document(doc)
                for doc in getattr(self.db, collection).find(*args, **kwargs))

    def add(self, entity):
        """
        add entity to the corresponding collection
        """
        collection = self.collections[entity.__class__.__name__]
        _id = getattr(self.db, collection, None).insert(entity.as_document())
        entity._id = _id
        return _id


def _seed():
    import json

    print 'INFO: seeding database' # TODO: use logger
    with open('data.json') as fp:
        for doc in json.load(fp):
            concept = Concept().from_document(doc)
            STORE.add(concept)
            print concept._id, concept


# XXX: does not belong into this module
STORE = Store('localhost', 27017, 'sivoc') # TODO: read from config
