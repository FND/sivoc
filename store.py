from pymongo import Connection

from model.concept import Concept
from model.label import Label


STORE = None # populated below


class Store(object):
    """
    MongoDB persistence wrapper
    """

    collections = {
        'Concept': 'concepts'
    }

    def __init__(self, host, port, database):
        self.db = getattr(Connection(host, port), database)

    def retrieve(self, collection, query=None):
        if collection not in self.collections.values():
            raise ValueError('invalid collection')

        results = []
        # XXX: hard-coding concepts (with nested labels) for now
        for concept in getattr(self.db, collection).find(query):
            pref_labels = [Label(label['name'], label.get('lang'))
                    for label in concept['labels']['pref']]
            alt_labels = [Label(label['name'], label.get('lang'))
                    for label in concept['labels']['alt']]
            yield Concept(str(concept['_id']), pref_labels, alt_labels)

    def add(self, entity):
        """
        add entity to the corresponding collection
        """
        collection = self.collections[entity.__class__.__name__]
        _id = getattr(self.db, collection, None).insert(entity.data())
        entity._id = _id
        return _id


def _seed():
    import json

    print 'INFO: seeding database' # TODO: use logger
    with open('data.json') as fp:
        for concept in json.load(fp):
            pref_label = Label(concept['pref']['name'], concept['pref']['lang'])
            alt_labels = [Label(label['name'], label['lang'])
                    for label in concept['alt']]
            concept = Concept(pref_labels=[pref_label], alt_labels=alt_labels)
            STORE.add(concept)


# XXX: does not belong into this module
STORE = Store('localhost', 27017, 'sivoc') # TODO: read from config
