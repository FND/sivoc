# TODO: embed in common layout


def list_concepts(concepts):
    yield '<ul>'
    for concept in concepts:
        label = concept.label()
        uri = 'concepts/' + concept._id
        yield '<li><a href="%s">%s</a></li>' % (uri, label)
    yield '</ul>'


def show_concept(concept): # TODO: i18n
    yield '<dl>'

    yield '<dt>ID</dt><dd>%s</dd>' % concept._id

    line = '<dd>%s <span class="language">[%s]</span></dd>' # XXX: embedded SPAN less than ideal

    yield '<dt>Preferred Labels</dt>'
    for label in concept.pref_labels:
        yield  line % (label.name, label.lang)

    yield '<dt>Alternative Labels</dt>'
    for label in concept.alt_labels:
        yield line % (label.name, label.lang)

    yield '</dl>'
