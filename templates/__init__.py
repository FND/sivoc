import jinja2


ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('templates')) # XXX: use PackageLoader?
