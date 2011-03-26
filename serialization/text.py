def list_concepts(concepts):
    for concept in concepts:
        label = concept.label()
        try:
            yield "%s\n" % label.name
        except AttributeError: # ID
            yield "%s\n" % label


def show_concept(concept):
    line = "    [%s] %s\n"

    yield "%s\n\n" % concept._id

    yield "PREFERRED LABELS\n"
    for label in concept.pref_labels:
        yield line % (label.lang, label.name)

    yield "\n"

    yield "ALTERNATIVE LABELS\n"
    for label in concept.alt_labels:
        yield line % (label.lang, label.name)
