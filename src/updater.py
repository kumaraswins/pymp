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
    ver = urllib.urlopen(self.versionUrl).read().strip()
    if ver.find("404 Not Found") >= 0:
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
    version = self.checkVersion()
    result = (self.version < version)
    logging.log(4,result)
    return result,version
  
  def update(self):
    check,version = self.isUpdateRequired()
    if check:
      installedFiles=[]
      for i in self.files.strip().split("\n"):
        files=i.split(" ")
        if len(files) != 2:
          continue
        installedFiles.append(files[1])
        self.updateFile(version,files[0],files[1])
      self.removeNotInstalledFiles(installedFiles)
      return True
    return False
  
  def removeNotInstalledFiles(self,installedFiles):
    logging.log(4,"")
    filesToDelete=findFilesInPathButNotInList(os.path.dirname(__file__))
    logging.log(4,"")
    for i in filesToDelete:
      logging.log(4,"Removing "+ i)
      os.remove(i)
    logging.log(4,"")
    return
  
  def updateFile(self,version,fileSource,fileTarget):
    fileSource=self.baseUrl+fileSource+"?r="+version
    fileTarget=self.installationPath+fileTarget
    logging.log(4,fileSource)
    logging.log(4,fileTarget)
    try:
      newcontent = urllib.urlopen(fileSource).read()
    except:
      logging.error("Unable to download "+fileSource)
    try:
      stream = open(fileTarget,"w")
      stream.write(newcontent)
      stream.close()
    except:
      logging.error("Unable to write "+ fileTarget)
    logging.log(4,"Wrote "+fileTarget)
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
