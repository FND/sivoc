"""
provides a WSGI application
"""

import os

from selector import Selector

from web.middleware import UTF8_Encoder
from web.handlers import get_root


mapfile = '%s/uris.map' % os.path.dirname(__file__) # XXX: use pkg_resources.resource_filename (cf. tiddlyweb.config:URLS_MAP)
app = Selector(mapfile=mapfile)
app = UTF8_Encoder(app)
