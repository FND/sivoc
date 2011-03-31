class Concept(object):

    def __init__(self, _id=None, pref_labels=None, alt_labels=None):
        self._id = _id # None if not (yet) persisted
        self.pref_labels = pref_labels or []
        self.alt_labels = alt_labels or []

    def __repr__(self):
        try:
            return self.label() + object.__repr__(self)
        except TypeError, exc:
            return object.__repr__(self)

    def label(self): # XXX: ambiguous; rename?
        """
        returns primary text representation (preferred label)
        """
        try:
            return self.pref_labels[0].name # TODO: use current locale
        except IndexError, exc:
            return self._id

    def as_document(self):
        """
        returns a dictionary representing the instance's data
        """
        labels = {
            'pref': [label.as_document() for label in self.pref_labels],
            'alt': [label.as_document() for label in self.alt_labels]
        }
        return { 'labels': labels }

    def from_document(self, doc):
        """
        internalizes values from a dictionary (structure as per as_document)
        """
        from model.label import Label # XXX: coupling!

        self._id = doc.get('_id')
        for _type in ('pref', 'alt'):
            labels = doc.get('labels', {}).get(_type, [])
            setattr(self, "%s_labels" % _type, [Label('').from_document(label)
                    for label in labels])
        return self
