#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import threading
import Queue
import re,tempfile,subprocess,time,os
import inspect

def getName():
  "Returns the name of the calling function."
  frame = inspect.currentframe()
  return frame.f_back.f_code.co_name

class MyList(list):
  def last(self):
    return self[len(self)-1]

class ConvertWorker(threading.Thread):
  queue = Queue.Queue()
  result={}
  resultLock=threading.Lock()
  
  def __init__(self):
    threading.Thread.__init__(self)
    self.programList={
                      "ffmpeg":   {
                                   "exec":self.executeFfmpeg,
                                   "state":self.getStateFfmpeg,
                                   "path":"ffmpeg",
                                  },
                      "lame":     {"exec":self.executeLame,
                                   "state":self.getStateLame,
                                   "path":"lame",
                                  },
                      "mplayer":  {
                                   "exec":self.executeMplayer,
                                   "state":self.getStateMplayer,
                                   "path":"mplayer",
                                   },
                      "normalize":{
                                   "exec":self.executeNormalize,
                                   "state":self.getStateNormalize,
                                   "path":"normalize",
                                   },
                      "sox":      {
                                   "exec":self.executeSox,
                                   "state":self.getStateSox,
                                   "path":"sox",
                                   },
                      }
    self.readSettings()
    self.currentRunning=None
    self.fnullName="/dev/null"
    debugFlag = False
    if True == debugFlag:
      self.stdoutFake=sys.stdout
      self.stdinFake=open(self.fnullName,"r")
      self.stderrFake=sys.stderr
    else:
      self.stdoutFake=open(self.fnullName,"w")
      self.stdinFake=open(self.fnullName,"r")
      self.stderrFake=open(self.fnullName,"w")
    self.p = None
    self.filesToDelete = []
    return
  
  def isCommandAvailable(self,commandString):
    """
    Check for the binary that needs to be executed. Not OS independent :(
    """
    sts=subprocess.call("type %s 1>/dev/null 2>/dev/null"%commandString,shell=True)
    if sts == 0:
      return True
    else:
      return False
  
  def readSettings(self):
    pass
  
  def cleanUp(self):
    """
    Function to clean up everything which was created during the process. Such as
    temporary files for conversion etc.
    """
    self.p = None
    #uniqify the list
    self.filesToDelete = {}.fromkeys(self.filesToDelete).keys()
    for file in self.filesToDelete:
      if os.path.isfile(file):
        os.remove(file)
    return
  
  def addResult(convertingFile,state,putInQueue = False):
    rc = False
    ConvertWorker.resultLock.acquire()
    if convertingFile not in ConvertWorker.result.keys():
      ConvertWorker.result[convertingFile] = {"state": state,
                                              "step": "",
                                              "stepState": ""}
      if True == putInQueue:
        ConvertWorker.queue.put(convertingFile)
      rc = True
    ConvertWorker.resultLock.release()
    return rc
  addResult=staticmethod(addResult)
  
  def run(self):
    while True:
      self.convertingFile = ConvertWorker.queue.get()
      self.workingFile = MyList()
      self.workingFile.append(self.convertingFile)
      self.filesToDelete = []
      self.p = None
      ConvertWorker.addResult(self.convertingFile,"Converting 0%")
      self.totalProgress = 0
      if True == os.path.isfile(self.convertingFile):
        if False:
          self.totalSteps=2
          self.executeSubprocess("ffmpeg")
        else:
          self.totalSteps=4
          self.executeSubprocess("mplayer")
          self.executeSubprocess("sox")
          self.executeSubprocess("lame")
        self.executeSubprocess("normalize")
      self.updateResult("done")
      self.cleanUp()
    return

  def updateResult(self,state):
    try:
      ConvertWorker.resultLock.acquire()
      if "done" == state:
        ConvertWorker.queue.task_done()
        ConvertWorker.result[self.convertingFile] = {"state" : state, 
                                                     "step": self.currentRunning,
                                                     "stepState": state}
      else:
        total=(int(self.totalProgress) + float(state.strip("%"))/100)/float(self.totalSteps)*100
        ConvertWorker.result[self.convertingFile] = {"state": str(total)+"%",
                                                     "step": self.currentRunning,
                                                     "stepState": state}
      logging.debug(self.convertingFile)
      logging.debug(self.result[self.convertingFile])
      ConvertWorker.resultLock.release()
      return
    except ValueError:
      logging.exception(state)
      raise(ValueError)
    except:
      raise
  
  def getStateFfmpeg(self):
    totalTime=None
    pDuration=re.compile("totalTime.*:")
    pTime=re.compile("time=[0-9]+.[0-9]+")
    self.tmpFile.seek(0)
    fileContent=self.tmpFile.read()
    x=fileContent.split("\n")
    x.reverse()
    for line in x:
      convertedTime=None
      if None == totalTime and pDuration.search(line):
        totalTime = float(line.split(":")[1])
      elif None == convertedTime and pTime.search(line):
        strTime=pTime.findall(line)
        strTime.reverse()
        convertedTime=float(strTime[0].split("=")[1])

      if None != convertedTime and None != totalTime:
        toReturn="%i%%"%(convertedTime/totalTime*100.0)
        return toReturn
    return "0%"
  
  def getStateMplayer(self):
    pattern=re.compile(r"^A:")
    self.tmpFile.seek(0)
    fileContent=self.tmpFile.read()
    for line in fileContent.split("\n"):
      if pattern.search(line):
        allInfos=line.split("\r")
        allInfos.reverse()
        for i in allInfos:
          if pattern.search(i):
            infos=i.split()
            progress=infos[1]
            total=infos[4]
            percentage=float(progress)/float(total)*100
            toReturn="%i%%"%(percentage)
            return toReturn
    return "0%"
  
  def getStateLame(self):
    pattern=re.compile(r"\(([0-9]{1,3}%)\)")
    self.tmpFile.seek(0)
    fileContent=self.tmpFile.read()
    x=fileContent.split("\n")
    x.reverse()
    for line in x:
      if pattern.search(line):
        return pattern.findall(line)[0]
    return "0%"
  
  def getStateNormalize(self):
    pattern=re.compile(r"([0-9]{1,3}%)")
    pApplying=re.compile(r"^Applying")
    pComputing=re.compile(r"^Computing")
    fComputing=False
    fApplying=False
    
    self.tmpFile.seek(0)
    fileContent=self.tmpFile.read()
    for line in fileContent.split("\n"):
      if pattern.search(line):
        toReturn=pattern.findall(line)
        toReturn.reverse()
        return toReturn[0]
      elif False == fApplying and pApplying.search(line):
        fApplying=True
      elif False == fComputing and pComputing.search(line):
        fComputing=True
    return "0%"
  
  def getStateSox(self):
    pattern=re.compile(r"In:(.*?%) ")
    self.tmpFile.seek(0)
    fileContent=self.tmpFile.read()
    for line in fileContent.split("\n"):
      if pattern.search(line):
        result=pattern.findall(line)
        result.reverse()
        return result[0]
    return "0%"
  
  def getStateSubprocess(self):
    if self.currentRunning in self.programList:
      return self.programList[self.currentRunning]["state"]()
    else:
      return "0%"
    
  def executeFfmpeg(self):
    self.currentRunning="ffmpeg"
    self.workingFile.append(self.convertingFile+".mp3")
    self.tmpFile=tempfile.TemporaryFile()
    self.p = subprocess.Popen([
                               self.programList["ffmpeg"]["path"],
                               "-y",
                               "-ab",
                               "128k",
                               "-i",
                               self.convertingFile,
                               self.workingFile.last()
                               ],
                               stdin=self.stdinFake,
                               stdout=self.stdoutFake,
                               stderr=self.tmpFile
                               )
    while None != self.p and None == self.p.poll():
      time.sleep(0.1)
      self.updateResult(self.getStateSubprocess())
    self.tmpFile.close()
    return
  
  def executeLame(self):
    self.currentRunning="lame"
    toConvert=self.workingFile.last()
    self.workingFile.append(self.convertingFile+".mp3")
    self.tmpFile=tempfile.TemporaryFile()
    self.p=subprocess.Popen([
                             self.programList["lame"]["path"],
                             "-h",
                             toConvert,
                             self.workingFile.last()
                             ],
                             stdin=self.stdinFake,
                             stdout=self.stdoutFake,
                             stderr=self.tmpFile)
    while None != self.p and None == self.p.poll():
      time.sleep(0.1)
      self.updateResult(self.getStateSubprocess())
    self.tmpFile.close()
    return
  
  def executeMplayer(self):
    self.currentRunning="mplayer"
    self.workingFile.append(self.convertingFile+".dump.wav")
    self.filesToDelete.append(self.workingFile.last())
    self.tmpFile=tempfile.TemporaryFile()
    self.p=subprocess.Popen([
                             self.programList["mplayer"]["path"],
                             "-novideo",
                             "-ao",
                             "pcm:fast:file="+self.workingFile.last(),
                             self.convertingFile
                             ],
                             stdout=self.tmpFile,
                             stdin=self.stdinFake,
                             stderr=self.stderrFake
                             )
    while None != self.p and None == self.p.poll():
      self.updateResult(self.getStateSubprocess())
      time.sleep(0.1)
    self.tmpFile.close()
    return
  
  def executeNormalize(self):
    self.currentRunning="normalize"
    self.tmpFile=tempfile.TemporaryFile()
    self.p = subprocess.Popen([
                               self.programList["normalize"]["path"],
                               self.workingFile.last()
                               ],
                               stdin=self.stdinFake,
                               stdout=self.stdoutFake,
                               stderr=self.tmpFile
                               )
    while None != self.p and None == self.p.poll():
      time.sleep(0.1)
      self.updateResult(self.getStateSubprocess())
    self.tmpFile.close()
    return
  
  def executeSox(self):
    self.currentRunning="sox"
    toTrim=self.workingFile.last()
    self.workingFile.append(toTrim+".trim.wav")
    self.filesToDelete.append(self.workingFile.last())
    self.tmpFile=tempfile.TemporaryFile()
    # sox --show-progress fileToTrim outputFile reverse silence 1 1 2% reverse silence 1 1 2%
    self.p = subprocess.Popen([
                               self.programList["sox"]["path"],
                               "--show-progress",
                               toTrim,
                               self.workingFile.last(),
                               "reverse",
                               "silence",
                               "1",
                               "1",
                               "2%",
                               "reverse",
                               "silence",
                               "1",
                               "1",
                               "2%"
                               ],
                               stdin=self.stdinFake,
                               stdout=self.stdoutFake,
                               stderr=self.tmpFile
                               )
    while None != self.p and None == self.p.poll():
      time.sleep(0.1)
      self.updateResult(self.getStateSubprocess())
    self.tmpFile.close()
    return
  
  def executeSubprocess(self,commandString):
    logging.debug(commandString)
    if commandString in self.programList and self.isCommandAvailable(commandString):
      self.programList[commandString]["exec"]()
    else:
      logging.warning(commandString + " not available. Skipping that step.")
      self.currentRunning=None
    #no matter if something was done or not, we have progress - to reach the 100% someday
    self.p = None
    self.totalProgress+=1
    return
  
  def killSubprocess(self):
    if None != self.p:
      self.p.terminate()
      time.sleep(0.01)
      if None != self.p and None == self.p.poll():
        self.p.kill()
      self.p = None
    return

if __name__== '__main__':
  logging.basicConfig(
                      filename=os.path.basename(__file__)+".log",
                      filemode="w",
                      level=logging.DEBUG,
                      format = "%(asctime)s %(levelname)s %(process)s %(thread)s %(module)s %(funcName)s %(lineno)s: %(message)s",
                      datefmt = "%F %H:%M:%S")
  
  threads = [ConvertWorker() for i in range(2)]
  for thread in threads:
    thread.setDaemon(True)
    thread.start()

  ConvertWorker.queue.put("../test/Aladdin_intro_German-bJAyLYR71NM.flv")
  ConvertWorker.queue.put("../test/Warum_bin_ich_so_fr_hlich-jrZHxIA0eVU.flvAaAStayInTehLight")
  ConvertWorker.queue.put("../test/Gummib_renbande_Titelsong_Lyrics-O5sd_CuZxNc.flv")
  ConvertWorker.queue.put("../test/Speedy_Gonzales_Die_schnellste_Maus_von_Mexiko_german_Intro-lfEDO1uZxVA.flv")
  ConvertWorker.queue.put("../test/Warum_bin_ich_so_fr_hlich-jrZHxIA0eVU.flv")
  time.sleep(0.1)
  cnt=1
  while cnt > 0:
    time.sleep(0.1)
    cnt=0
    for i,j in ConvertWorker.result.iteritems():
      print j,i
      if "done" != j["state"]:
        cnt+=1
  ConvertWorker.queue.join()
  sys.exit(0)
