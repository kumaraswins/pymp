#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,logging

def findFilesInPath(path):
  fileList=[]
  for root,dirs,files in os.walk(path):
    for f in files:
      ff=root+"/"+f
      fileList.append(ff)
  return fileList

def findFilesInPathButNotInList(path,list):
  filesInPath=findFilesInPath(path)
  filesNotInPath=[]
  for file in filesInPath:
    try:
      i=list.index(file)
    except:
      filesNotInPath.append(file)
  return filesNotInPath

if __name__ == "__main__":
  import sys
  logging.basicConfig(
                      filename=os.path.basename(__file__)+".log",
                      filemode="w",
                      level=4,
                      format = "%(asctime)s %(levelname)s %(process)s %(module)s %(funcName)s %(lineno)s: %(message)s",
                      datefmt = "%F %H:%M:%S")
  filesInstalled=[]
  for i in open("../latestFiles","r").read().split("\n"):
    if len(i) >= 2:
      filesInstalled.append("./"+i.split(" ")[1])
  l=findFilesInPathButNotInList(".",filesInstalled)
  print "\n".join(l)
  sys.exit(0)
