def list_concepts(concepts):
    for concept in concepts:
        yield '%s\n' % concept.label()


def show_concept(concept):
    yield '%s\n' % concept._id

    line = '    [%s] %s\n'

    yield '\nPREFERRED LABELS\n'
    for label in concept.pref_labels:
        yield line % (label.lang, label.name)

    yield '\nALTERNATIVE LABELS\n'
    for label in concept.alt_labels:
        yield line % (label.lang, label.name)
