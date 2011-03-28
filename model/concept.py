class Concept(object):

    def __init__(self, _id, pref_labels=None, alt_labels=None):
        self._id = _id
        self.pref_labels = pref_labels or []
        self.alt_labels = alt_labels or []

    def __repr__(self):
        return self.label() + object.__repr__(self)

    def label(self): # XXX: ambiguous; rename?
        """
        returns primary text representation (preferred label)
        """
        try:
            return self.pref_labels[0].name # TODO: use current locale
        except IndexError, exc:
            return self._id
