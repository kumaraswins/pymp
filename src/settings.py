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

import re,os,logging
from maemoUtils import *

class Settings(dict):
  def __init__(self,file,installationPath):
    dict.__init__({})
    self.settingsFile = file
    self.defaults = {
                     "workingDirectory":"~",
                     "numberOfSimultaniousDownloads":"1",
                     "numberOfSimultaniousConversions":"1",
                     "download.numberOfRetries":"0",
                     "download.downloader.path":installationPath+"/youtubeDownload.py",
                     "download.continue":"True",
                     "download.overwrite":"False",
                     "mplayer.path":"mplayer",
                     "ffmpeg.path":"ffmpeg",
                     "sox.path":"sox",
                     "lame.path":"lame",
                     "converter.kbps":"192",
                     "normalize.path":"normalize",
                     }
    return
  
  def readFromFile(self):
    self.clear()
    pattern=re.compile(r"(.*?)(#.*|$)")
    logging.log(1,"")
    try:
      fileObject=open(self.settingsFile,"r")
      logging.log(1,"")
      for line in fileObject:
        logging.log(1,line)
        if pattern.match(line):
          raw=pattern.findall(line)[0][0]
          logging.log(1,raw)
          columns=raw.split(" ")
          logging.log(1,columns)
          c0=columns[0]
          logging.log(1,c0)
          c1=raw.replace(c0+" ","").lstrip()
          logging.log(1,c1)
          self[c0]=c1
      fileObject.close()
    except:
      raise
    finally:
      self.checkSettings()
      return self
  
  def writeToFile(self):
    try:
      f=open(self.settingsFile,"w")
      print >> f, "#Warning, comments will be overwritten, when changes are made in the UI"
      for key,value in self.iteritems():
        if key in self.defaults.keys():
          print >> f, key, value
      f.close
    finally:
      return
    
  def checkSettings(self):
    for key,value in self.defaults.iteritems():
      if key not in self.keys():
        self[key] = value
    #exception from the rule -.-
    keyword="workingDirectory"
    if not os.path.isdir(self[keyword]):
      if isMaemo5() and os.path.isdir(os.path.expanduser("~/MyDocs")):
        self[keyword] = str(os.path.expanduser("~/MyDocs"))
      else:
        self[keyword]= str(os.path.expanduser("~"))
        
    return
  
if __name__ == "__main__":
  import sys
  logging.basicConfig(
                      filename=os.path.basename(__file__)+".log",
                      filemode="w",
                      level=logging.DEBUG,
                      format = "%(asctime)s %(levelname)s %(process)s %(module)s %(funcName)s %(lineno)s: %(message)s",
                      datefmt = "%F %H:%M:%S")
  if os.path.isfile("test"):
    os.remove("test")
  s=Settings("test")
  s.readFromFile()
  print s
  s["WorkingDirectory"] = "/tmp"
  s.writeToFile()
  f=open("test")
  for i in f:
    print i.rstrip()
  f.close
  sys.exit(0)
