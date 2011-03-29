class Concept(object):

    def __init__(self, _id=None, pref_labels=None, alt_labels=None):
        self._id = _id # None if not (yet) persisted
        self.pref_labels = pref_labels or []
        self.alt_labels = alt_labels or []

    def __repr__(self):
        return self.label() + object.__repr__(self)

    def data(self):
        """
        returns a dictionary representing the instance's data
        """
        return {
            'labels': {
                'pref': [label.data() for label in self.pref_labels],
                'alt': [label.data() for label in self.alt_labels]
            }
        }

    def label(self): # XXX: ambiguous; rename?
        """
        returns primary text representation (preferred label)
        """
        try:
            return self.pref_labels[0].name # TODO: use current locale
        except IndexError, exc:
            return self._id
