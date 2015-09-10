#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'nasiry.teng@gmail.com'


import tornado
from tornado import  gen
import json




import os

import random,string
import codecs
import re
from os.path import join, getsize

#for simply intergation
#override template path here
#only impact this handler
def get_template_path():
    import os
    absdir= os.path.abspath(__file__)
    #print "[abs]"+absdir

    return os.path.dirname(absdir)+"/templates/"
#load config only once
class ueditor4TornadoEnv():

    walkImageCache=[]
    walkFileCache=[]
    def __init__(self,withListCache =False):
        #print get_template_path()
        fp  = codecs.open(get_template_path()+"/config.json","r",'utf-8')
        jsonstr = re.sub("\/\*[\s\S]+?\*\/" , '' ,fp.read()) #simple follow C# sample
        fp.close()
        self.config =  json.loads(jsonstr)

        #build file lists as cache
        if withListCache :
            self.walkin(self.config["imagePathFormat"],self.walkImageCache)
            self.walkin(self.config["filePathFormat"],self.walkFileCache)
        #print json.dumps(self.config, indent=1)

    #this only for single runtime instance
    # only if you use NAS as the file backend
    #for multi runtime instance please use database for indexing
    #also ,please add your file sync implement

    def walkin(self,baseDir,cache):
         for root, dirs, files in os.walk(baseDir):
             for name  in files:
                cache.append( {"file":join(root.replace(baseDir,''), name) })

         #print self.walkCache

    def getList(self,start=0,count=20,isImage=True):
        ret = []
        if isImage:
            cache = self.walkImageCache
        else:
            cache = self.walkFileCache

        #fill it as possible,if overthe range ,simplely go out
        try:
            for index in range(start,start+count):
                ret.append({"url":cache[index]["file"]})
        except:
            pass

        return ret

    def appendFile(self,fileName,isImage=True):
        if isImage:
            cache = self.walkImageCache
        else:
            cache = self.walkFileCache
        cache.append({"file": fileName })

u4Ts = ueditor4TornadoEnv(withListCache=True)

#print u4Ts.getList(count=2)
class ueditor4TornadoHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        try:
            user = super(ueditor4TornadoHandler, self).get_current_user()
        except:
            pass
        if user ==None:
            user = "anonymous"
        return user


    def saveFile(self,fileobj,baseDir,fname=None,usr=None,isImage=True):
        #print "on save"

        #print fileobj.body
        if usr ==None:
            usr = self.get_current_user()
         #gen path for usr

        import datetime

        uploadPath =usr+ '/'+ datetime.datetime.utcnow().strftime("%Y%m%d") +'/'

        if not os.path.exists(baseDir+uploadPath):
            print "make path"
            os.makedirs (baseDir+uploadPath)
        else:
            pass
        print uploadPath
        # gen fname
        if fname==None:
            fname =(''.join(random.choice(string.ascii_uppercase) for i in range(10)))

            fname += os.path.splitext(fileobj["filename"])[1]
            if not os.path.exists(baseDir+uploadPath+fname):
                fp = open(baseDir+uploadPath+fname,'wb')
                fp.write(fileobj["body"])
                fp.close()
                result = {
                      "state": "SUCCESS",
                      "url": uploadPath +fname,
                      "title": fname,
                      "original": fileobj["filename"] ,
                    }
                u4Ts.appendFile( uploadPath +fname,isImage=isImage)
                self.write(result)
                self.finish()
            else:
                 self.saveFile(usr=usr,baseDir=baseDir,fileobj=fileobj,isImage=isImage)







    @gen.coroutine
    def get(self):
        #print "do get"
        #for key in self.request.arguments:
        #    print key, self.get_arguments(key)

        action = self.get_argument("action")
        if  action == "config":
            self.render(get_template_path()+"config.json")
            return
        elif action==u4Ts.config["imageManagerActionName"]:
            start=int(self.get_argument('start'))
            size=int(self.get_argument('size'))
            urls = u4Ts.getList(start,size,isImage=True)
            result = {
                "state": "SUCCESS",
                "list": urls,
                "start": start ,
                "total": len(urls)
            }
            self.write(result)
            self.finish()
            return
        elif action==u4Ts.config["fileManagerActionName"]:
            start=int(self.get_argument('start'))
            size=int(self.get_argument('size'))
            urls = u4Ts.getList(start,size,isImage=False)
            result = {
                "state": "SUCCESS",
                "list": urls,
                "start": start ,
                "total": len(urls)
            }
            self.write(result)
            self.finish()
            return

        self.finish()


    @gen.coroutine
    def post(self):
        #print "do post"
        #for key in self.request.arguments:
        #    print key, self.get_arguments(key)

        if self.get_argument("action") == u4Ts.config["imageActionName"]:
            for keys in self.request.files:
                for fileobj in self.request.files[keys]:
                    self.saveFile(baseDir=u4Ts.config["imagePathFormat"] ,fileobj= fileobj)

        elif self.get_argument("action") == u4Ts.config["scrawlActionName"]:
            #print self.get_argument]
            import base64
            fileobj={"filename":"scrawl.png","body":base64.decodestring(self.get_argument(u4Ts.config["scrawlFieldName"]))}
            self.saveFile( baseDir=u4Ts.config["scrawlPathFormat"] ,fileobj= fileobj)

        elif self.get_argument("action") ==u4Ts.config["snapscreenActionName"]:
            for keys in self.request.files:
                for fileobj in self.request.files[keys]:
                 self.saveFile( baseDir=u4Ts.config["snapscreenPathFormat"] ,fileobj= fileobj)

        elif self.get_argument("action") ==u4Ts.config["videoActionName"]:
            for keys in self.request.files:
                for fileobj in self.request.files[keys]:
                    self.saveFile( baseDir=u4Ts.config["videoPathFormat"] ,fileobj= fileobj)

        elif self.get_argument("action") ==u4Ts.config["fileActionName"]:
            print ""
            for keys in self.request.files:
                for fileobj in self.request.files[keys]:
                    self.saveFile( baseDir=u4Ts.config["filePathFormat"] ,fileobj= fileobj,isImage=False)



