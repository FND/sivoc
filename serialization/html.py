import jinja2


ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('templates')) # XXX: use PackageLoader?


def list_concepts(concepts):

    def template_data(concept):
        return {
            'uri': 'concepts/' + concept._id,
            'label': concept.label()
        }

    concepts_data = (template_data(concept) for concept in concepts) # XXX: unnecessarily complex?

    template = ENV.get_template('list_concepts.html')
    return template.generate(concepts=concepts_data)


def show_concept(concept): # TODO: i18n
    template = ENV.get_template('show_concept.html')
    return template.generate(concept=concept)
