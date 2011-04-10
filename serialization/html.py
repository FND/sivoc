from templates import render


def list_concepts(concepts):

    def template_data(concept):
        return {
            'uri': 'concepts/%s' % concept._id, # XXX: URI hardcoded; breaks encapsulation
            'label': concept.label()
        }

    concepts_data = (template_data(concept) for concept in concepts) # XXX: unnecessarily complex?

    return render('list_concepts.html', title='Concepts',
            concepts=concepts_data, root_uri='/') # XXX: root_uri hardcoded; breaks encapsulation


def list_labels(labels):
    return render('list_labels.html', title='Labels', labels=labels,
            root_uri='/') # XXX: root_uri hardcoded; breaks encapsulation


def show_concept(concept): # TODO: i18n
    return render('show_concept.html', title=concept.label(), concept=concept,
            concepts_uri='/concepts') # XXX: concepts_uri hardcoded; breaks encapsulation
