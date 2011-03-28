#!/usr/bin/env python

"""
launch development server

Usage:
  $ launch.py [host [port]]
"""

import sys

from web import app
from web.util import serve


DEFAULT_HOST = ''
DEFAULT_PORT = 8080


def main(args):
    args = [unicode(arg, 'utf-8') for arg in args]

    host = _get_item(args, 1, DEFAULT_HOST)
    port = _get_item(args, 2, DEFAULT_PORT)

    serve(app, host, port)

    return True


def _get_item(indexable, index, default):
    try:
        return indexable[index]
    except IndexError, exc:
        return default


if __name__ == '__main__':
    status = not main(sys.argv)
    sys.exit(status)
