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
    ver = urllib.urlopen(self.versionUrl).read().strip()
    if ver.find("404"):
      logging.error(ver)
      raise(ValueError)
    self.files = urllib.urlopen(self.filesUrl).read().strip()
    if ver.find("404"):
      logging.error(self.files)
      raise(ValueError)
    return ver
  
  def isUpdateRequired(self):
    return (self.version != self.checkVersion())
  
  def update(self):
    if self.isUpdateRequired():
      logging.log(4,"")
    return
  
if __name__== '__main__':
  import sys
  logging.basicConfig(
                      filename=os.path.basename(__file__)+".log",
                      filemode="w",
                      level=4,
                      format = "%(asctime)s %(levelname)s %(process)s %(module)s %(funcName)s %(lineno)s: %(message)s",
                      datefmt = "%F %H:%M:%S")
  u = Updater("2011-05-29",
              "http://pymp.googlecode.com/hg/test/",
              "latestVersion",
              "latestFiles")
  u.update()
  sys.exit(0)
