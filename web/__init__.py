"""
provides a WSGI application
"""

import os

from selector import Selector

from web.middleware import Negotiate, HTTPExceptor, UTF8_Encoder
from web.handlers import get_root
from config import CONFIG


mapfile = '%s/uris.map' % os.path.dirname(__file__) # XXX: use pkg_resources.resource_filename (cf. tiddlyweb.config:URLS_MAP)
app = Selector(mapfile=mapfile)
app = Negotiate(app, CONFIG['serializations'].keys())
app = HTTPExceptor(app)
app = UTF8_Encoder(app)
