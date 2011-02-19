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
    self.settings=settings
    return
  
  def readSettings(self):
    self.settings.readFromFile()
    self.options=["-t"]
    
    if None != self.settings:
      keyword="download.numberOfRetries"
      if keyword in self.settings.keys():
        self.options.append("-R")
        self.options.append(str(self.settings[keyword]))
    if self.settings["download.continue"] == "True":
      self.options.append("-c")
    if self.settings["download.overwrite"] == "False":
      self.options.append("-w")
      
    for i in self.options:
      logging.log(2,type(i).__name__+" "+i)
    return
  
  def run(self):
    while True:
      self.url = DownloadWorker.queue.get()
      DownloadWorker.addResult(self.url,"Downloading 0%")
      self.targetFile = None
      self.p = None
      self.tmpFile = tempfile.TemporaryFile()
      self.errFile = tempfile.TemporaryFile()
      self.readSettings()
      call=[]
      call.append(self.settings["download.downloader.path"])
      call+=self.options
      call.append(self.url)
      self.p=subprocess.Popen(call,
                          stdout=self.tmpFile,
                          stderr=self.errFile)
      while None != self.p and None == self.p.poll():
        time.sleep(0.2)
        self.updateResult(self.getState())
        
      self.updateTargetFile()
      self.updateResult("done")
      self.p=None
      #only for debugging
      self.tmpFile.seek(0)
      maybeErrors=self.tmpFile.read()
      logging.log(2,maybeErrors)
      if re.search(r"ERROR:",maybeErrors):
        logging.error(self.url+":"+maybeErrors)
      self.errFile.seek(0)
      errors=self.errFile.read()
      if errors != "":
        logging.error(self.url+": "+errors)
      logging.log(2,self.result[self.url])
    return

  def updateTargetFile(self):
    if None == self.targetFile:
      #First try to find it when downloaded the regular way
      patternDownloading = re.compile(r"\[download\] Destination: (.*)$")
      #2nd try: maybe it was already downloaded
      patternAlreadyDone = re.compile(r"\[download\] (.*?) has already.*$")
      self.tmpFile.seek(0)
      fileContent=self.tmpFile.read()
      for i in fileContent.split("\n"):
        if patternDownloading.search(i):
          self.targetFile = patternDownloading.findall(i)[0]
          logging.log(2,self.targetFile+" "+i)
          return
        if patternAlreadyDone.search(i):
          self.targetFile = patternAlreadyDone.findall(i)[0]
          logging.log(2,self.targetFile+" "+i)
          return
    return
    
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
          logging.log(2,toReturn[0])
          return toReturn[0]
    return "0%"
  
  def killSubprocess(self):
    if self.p != None:
      try:
        self.p.terminate()
      except AttributeError:
        #workaround for old python versions
        subprocess.call(["kill","-15",str(self.p.pid)])
      time.sleep(0.02)
      if None != self.p and None == self.p.poll():
        try:
          self.p.kill()
        except AttributeError:
          #workaround for old python versions
          subprocess.call(["kill","-9",str(self.p.pid)])
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
      if not (i["state"] != "done" or i["state"] == "error"):
        cnt+=1
  DownloadWorker.queue.join()
  sys.exit(0)
