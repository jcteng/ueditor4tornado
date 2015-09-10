#!/usr/bin/python
# -*- coding:utf-8 -*-
#

#
__author__ = 'nasiry.teng@gmail.com'
import os
from string import  join
def walkin(baseDir,cache):
     for root, dirs, files in os.walk(baseDir):
         for name  in files:
             cache.append((root+"/"+name).replace("\\","/"))
            #cache.append( {"file":join(root, name) })

packagedir = "ueditor4tornado/statics"
list=[]
walkin(packagedir,list)

print list