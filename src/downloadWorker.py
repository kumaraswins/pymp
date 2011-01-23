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
import logging
import threading
import Queue
import re,tempfile,subprocess,time,os

class DownloadWorker(threading.Thread):
  queue = Queue.Queue()
  result={}
  resultLock=threading.Lock()
  
  def addResult(url,state,putInQueue = False):
    rc = False
    DownloadWorker.resultLock.acquire()
    if url not in DownloadWorker.result.keys():
      DownloadWorker.result[url] = {"state": state,
                                    "file": ""}
      if True == putInQueue:
        DownloadWorker.queue.put(url)
      rc = True
    DownloadWorker.resultLock.release()
    return rc
  addResult=staticmethod(addResult)
  
  def __init__(self,settings):
    threading.Thread.__init__(self)
    self.p = None
    self.options=["-t"]
    self.readSettings(settings)
    self.settings=settings
    return
  
  def readSettings(self,settings=None):
    if None != settings:
      keyword="download.numberOfRetries"
      if keyword in settings.keys():
        self.options.append("-R")
        self.options.append(str(settings[keyword]))
    for i in self.options:
      logging.debug(type(i).__name__+" "+i)
    return
  
  def run(self):
    while True:
      self.url = DownloadWorker.queue.get()
      DownloadWorker.addResult(self.url,"Downloading 0%")
      self.targetFile = None
      self.p = None
      self.tmpFile = tempfile.TemporaryFile()
      self.errFile = tempfile.TemporaryFile()
      call=[]
      call.append(self.settings["download.downloader.path"])
      call+=self.options
      call.append(self.url)
      self.p=subprocess.Popen(call,
                          stdout=self.tmpFile,
                          stderr=self.errFile)
      while None != self.p and None == self.p.poll():
        time.sleep(0.2)
        self.updateTargetFile()
        self.updateResult(self.getState())
      self.updateResult("done")
      self.p=None
      self.errFile.seek(0)
      errors=self.errFile.read()
      if errors != "":
        logging.error(errors)
    return

  def updateTargetFile(self):
    if None == self.targetFile:
      pattern = re.compile(r"\[download\] Destination: (.*)$")
      self.tmpFile.seek(0)
      fileContent=self.tmpFile.read()
      for i in fileContent.split("\n"):
        if pattern.search(i):
          logging.debug(i)
          self.targetFile = pattern.findall(i)[0]
    
  def updateResult(self,state):
    DownloadWorker.resultLock.acquire()
    DownloadWorker.result[self.url] = {"state": state, 
                                       "file": self.targetFile}
    DownloadWorker.resultLock.release()
    if "done" == state:
      DownloadWorker.queue.task_done()
    return
  
  def getState(self):
    if None != self.p and None == self.p.poll():
      pattern=re.compile(r" ([0-9\.]*%) ")
      self.tmpFile.seek(0)
      fileContent=self.tmpFile.read()
      fileContent=fileContent.split("\n")
      fileContent.reverse()
      for i in fileContent:
        if pattern.search(i):
          toReturn=pattern.findall(i)
          toReturn.reverse()
          logging.debug(toReturn[0])
          return toReturn[0]
    return "0%"
  
  def killSubprocess(self):
    if self.p != None:
      self.p.terminate()
      time.sleep(0.01)
      if None != self.p and None == self.p.poll():
        self.p.kill()
      self.p = None
    return


if __name__== '__main__':
  import sys
  logging.basicConfig(
                  filename=os.path.basename(__file__)+".log",
                  filemode="w",
                  level=logging.DEBUG,
                  format = "%(asctime)s %(levelname)s %(process)s %(thread)s %(module)s %(funcName)s %(lineno)s: %(message)s",
                  datefmt = "%F %H:%M:%S")
  settings={
            "download.downloader.path":"youtubeDownload.py"
            }
  threads = [DownloadWorker(settings) for i in range(2)]
  for thread in threads:
    thread.setDaemon(True)
    thread.start()
  
  DownloadWorker.queue.put("http://www.youtube.com/watch?v=O5sd_CuZxNc")
  DownloadWorker.queue.put("http://www.youtube.com/watch?v=O5sd_CuZxNcaa") #not working
  DownloadWorker.queue.put("http://www.youtube.com/watch?v=jrZHxIA0eVU&feature=related")
  DownloadWorker.queue.put("http://www.youtube.com/watch?v=bJAyLYR71NM&NR=1")
  DownloadWorker.queue.put("http://www.youtube.com/watch?v=lfEDO1uZxVA")
  time.sleep(1)
  cnt=1
  while cnt > 0:
    cnt=0
    time.sleep(1)
    for i,j in DownloadWorker.result.iteritems():
      print j,i
    for i in DownloadWorker.result.itervalues():
      if i["state"] != "done":
        cnt+=1
  DownloadWorker.queue.join()
  sys.exit(0)
