#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A simple hello world example.
"""

from weblayer import Bootstrapper, RequestHandler, WSGIApplication

class Hello(RequestHandler):
    def get(self, world):
        return u'hello {}'.format(world)
    


mapping = [(r'/(.*)', Hello)]

bootstrapper = Bootstrapper(url_mapping=mapping)
application = WSGIApplication(*bootstrapper())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('', 8080, application).serve_forever()
