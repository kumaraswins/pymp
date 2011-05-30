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
  logging.log(4,"\n".join(filesInPath))
  filesNotInPath=[]
  for file in filesInPath:
    try:
      i=list.index(file)
    except:
      filesNotInPath.append(file)
  return filesNotInPath

if __name__ == "__main__":
  import sys
  filesInstalled=[]
  for i in open("../latestFiles","r").read().split("\n"):
    if len(i) >= 2:
      filesInstalled.append("./"+i.split(" ")[1])
  l=findFilesInPathButNotInList(".",filesInstalled)
  print "\n".join(l)
  sys.exit(0)
