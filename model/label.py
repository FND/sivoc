class Label(object):

    def __init__(self, name, lang=None):
        self.name = name
        if lang:
            self.lang = lang

    def __repr__(self):
        return '%s[%s]' % (self.name, self.lang) + object.__repr__(self)

    def data(self):
        """
        returns a dictionary representing the instance's data
        """
        data = { 'name': self.name }
        if getattr(self, 'lang', None):
            data['lang'] = self.lang
        return data
