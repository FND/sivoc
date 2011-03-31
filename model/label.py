class Label(object):

    def __init__(self, name, lang=None):
        self.name = name
        if lang:
            self.lang = lang

    def __repr__(self):
        return '%s[%s]' % (self.name, self.lang) + object.__repr__(self)

    def as_document(self):
        """
        returns a dictionary representing the instance's data
        """
        doc = { 'name': self.name }
        if getattr(self, 'lang', None):
            doc['lang'] = self.lang
        return doc

    def from_document(self, doc):
        """
        internalizes values from a dictionary (structure as per as_document)
        """
        self.name = doc['name']
        self.lang = doc.get('lang')
        return self
