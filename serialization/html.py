from templates import ENV


def list_concepts(concepts):

    def template_data(concept):
        return {
            'uri': 'concepts/%s' % concept._id,
            'label': concept.label()
        }

    concepts_data = (template_data(concept) for concept in concepts) # XXX: unnecessarily complex?

    return _render('list_concepts.html', title='Concepts',
            concepts=concepts_data)


def show_concept(concept): # TODO: i18n
    return _render('show_concept.html', title=concept.label(), concept=concept)


def _render(template, **kwargs):
    template = ENV.get_template(template)
    return template.generate(**kwargs)
