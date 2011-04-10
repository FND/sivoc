import jinja2


ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('templates')) # XXX: use PackageLoader?


def render(template, **kwargs):
    template = ENV.get_template(template)
    return template.generate(**kwargs)
