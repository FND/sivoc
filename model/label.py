class Label(object):

    def __init__(self, name, lang=None):
        self.name = name
        if lang:
            self.lang = lang

    def __repr__(self):
        return self.name + object.__repr__(self)
