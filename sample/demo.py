#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'nasiry.teng@gmail.com'

import tornado
import tornado.web,tornado.httpserver
import ueditor4tornado


class demoHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render("templates/ueditor.html")

if __name__ == '__main__':
    application = tornado.web.Application([(r'/', demoHandler), ])
    ueditor4tornado.registerHandler(application,withStatics=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(7777,address="0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()