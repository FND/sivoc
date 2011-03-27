def list_concepts(concepts):
    for concept in concepts:
        yield '%s\n' % concept.label()


def show_concept(concept):
    line = '    [%s] %s\n'

    yield '%s\n\n' % concept._id

    yield 'PREFERRED LABELS\n'
    for label in concept.pref_labels:
        yield line % (label.lang, label.name)

    yield '\n'

    yield 'ALTERNATIVE LABELS\n'
    for label in concept.alt_labels:
        yield line % (label.lang, label.name)
