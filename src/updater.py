#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This file is part of pymp.

    pymp is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pymp is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pymp.  If not, see <http://www.gnu.org/licenses/>.
"""
import logging,urllib,os
from utils import *

class Updater():
  def __init__(self,path,version,baseUrl,versionFile,filesFile):
    self.version = version
    self.versionUrl = baseUrl+versionFile
    self.filesUrl = baseUrl+filesFile
    self.baseUrl = baseUrl
    self.installationPath = path+"/"
    
    logging.log(4,self.installationPath)
    logging.log(4,self.version)
    logging.log(4,self.baseUrl)
    logging.log(4,self.versionUrl)
    logging.log(4,self.filesUrl)
    return
  
  def checkVersion(self):
    ver = urllib.urlopen(self.versionUrl).read().strip().upper()
    if ver.find("404 NOT FOUND") >= 0:
      logging.error(self.versionUrl)
      logging.error(ver)
      raise(ValueError)
    self.files = urllib.urlopen(self.filesUrl).read().strip()
    if self.files.find("404 Not Found") >= 0:
      logging.error(self.filesUrl)
      logging.error(self.files)
      raise(ValueError)
    logging.log(4,ver)
    return ver
  
  def isUpdateRequired(self):
    result = (self.version != self.checkVersion())
    logging.log(4,result)
    return result
  
  def update(self):
    if self.isUpdateRequired():
      installedFiles=[]
      for i in self.files.strip().split("\n"):
        files=i.split(" ")
        if len(files) != 2:
          raise(ValueError)
        installedFiles.append(files[1])
        self.updateFile(files[0],files[1])
        self.removeNotInstalledFiles(installedFiles)
      return True
    return False
  
  def removeNotInstalledFiles(self,installedFiles):
    filesToDelete=findFilesInPathButNotInList(os.path.dirname(__file__))
    for i in filesToDelete:
      os.remove(i)
    return
  
  def updateFile(self,fileSource,fileTarget):
    fileSource=self.baseUrl+fileSource+"?r="+self.version
    fileTarget=self.installationPath+fileTarget
    logging.log(4,fileSource)
    logging.log(4,fileTarget)
    newcontent = urllib.urlopen(fileSource).read()
    stream = open(fileTarget,"w")
    stream.write(newcontent)
    stream.close()
    return
  
  def getVersion(self):
    return self.version
  
if __name__== '__main__':
  import sys
  logging.basicConfig(
                      filename=os.path.basename(__file__)+".log",
                      filemode="w",
                      level=4,
                      format = "%(asctime)s %(levelname)s %(process)s %(module)s %(funcName)s %(lineno)s: %(message)s",
                      datefmt = "%F %H:%M:%S")
  u = Updater(os.path.realpath(sys.argv[0]),
              "2011-05-28",
              "http://pymp.googlecode.com/hg/",
              "latestVersion",
              "latestFiles")
  u.update()
  sys.exit(0)
