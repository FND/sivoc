def serve(app, host, port):
    """
    serve WSGI application using a basic HTTP server

    NB: Not suitable for production use!
    """
    from wsgiref.simple_server import make_server

    httpd = make_server(host, port, app)
    print 'serving on http://%s:%s' % (host or 'localhost', port)
    httpd.serve_forever()
