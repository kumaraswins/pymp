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

class Updater():
  def __init__(self,version,baseUrl,versionFile,filesFile):
    self.version = version
    self.versionUrl = baseUrl+versionFile
    self.filesUrl = baseUrl+filesFile
    self.baseUrl = baseUrl
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
    self.files = urllib.urlopen(self.filesUrl).read().strip().upper()
    if self.files.find("404 NOT FOUND") >= 0:
      logging.error(self.filesUrl)
      logging.error(self.files)
      raise(ValueError)
    logging.log(4,ver)
    logging.log(4,self.files)
    return ver
  
  def isUpdateRequired(self):
    result = (self.version != self.checkVersion())
    logging.log(4,result)
    return result
  
  def update(self):
    if self.isUpdateRequired():
      for i in self.files.strip().split("\n"):
        files=i.split(" ")
        if len(files) != 2:
          raise(ValueError)
        self.updateFile(files[0],files[1])
    return
  
  def updateFile(self,fileSource,fileTarget):
    logging.log(4,fileSource,fileTarget)
    return
  
if __name__== '__main__':
  import sys
  logging.basicConfig(
                      filename=os.path.basename(__file__)+".log",
                      filemode="w",
                      level=4,
                      format = "%(asctime)s %(levelname)s %(process)s %(module)s %(funcName)s %(lineno)s: %(message)s",
                      datefmt = "%F %H:%M:%S")
  u = Updater("2011-05-28",
              "http://pymp.googlecode.com/hg/test/",
              "latestVersion",
              "latestFiles")
  u.update()
  sys.exit(0)
