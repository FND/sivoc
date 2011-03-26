"""
provides a WSGI application
"""

from selector import Selector

from web.middleware import UTF8_Encoder
from web.handlers import get_root


app = Selector()
app.add('/', GET=get_root)

app = UTF8_Encoder(app)
