#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'nasiry.teng@gmail.com'

__version__ = "0.1.1"

from tornado.web import StaticFileHandler
import os
import handler
notify='''
notes:
    copy statics to your real static serve directory
    from %s
'''
#just for simplely usage
def registerHandler(application,withStatics=False):


    if withStatics :
        print os.path.dirname(os.path.abspath(__file__))+"/statics/"
        application.add_handlers(".*$", [
            (r'/ueditor4tornado/controller',handler.ueditor4TornadoHandler),
            (r'^/statics/ueditor/(.*)',StaticFileHandler,{"path":os.path.dirname(os.path.abspath(__file__))+"/statics/ueditor/"}),
            (r'^/upload/(.*)',StaticFileHandler,{"path":"upload/"}),


            ])

    else:
        application.add_handlers(".*$", [
        (r'/ueditor4tornado/',handler.ueditor4TornadoHandler),
        ])


    print notify%(os.path.dirname(os.path.abspath(__file__))+"/statics/")

