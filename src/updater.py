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
import logging,urllib,os,shutil,threading,time,inspect
from PyQt4 import QtGui, QtCore
from qtUtils import *
from utils import *

class Updater(QtGui.QDialog):
  def __init__(self,path,version,baseUrl,versionFile,filesFile,logFileName):
    QtGui.QDialog.__init__(self)
    self.updaterWorker = UpdaterWorker(path,version,baseUrl,versionFile,filesFile)
    self.version = version
    self.versionUrl = baseUrl+versionFile
    self.filesUrl = baseUrl+filesFile
    self.baseUrl = baseUrl
    self.installationPath = path+"/"
    self.logFileName = logFileName
    self.res = "failure"
    self.setupUi()
    return
  
  def setupUi(self):
    self.mainLayout=QtGui.QVBoxLayout(self)
    self.bar = QtGui.QProgressBar(self)
    self.bar.setMinimum(0)
    self.bar.setMaximum(999)
    self.cancelButton = QtGui.QPushButton(self)
    self.mainLayout.addWidget(self.bar)
    self.mainLayout.addWidget(self.cancelButton)
    self.setLayout(self.mainLayout)
    
    self.timer = QtCore.QTimer()
    
    self.connect(self.cancelButton,
                 QtCore.SIGNAL("clicked()"),
                 self.onCancel)
    self.connect(self.timer,
                 QtCore.SIGNAL("timeout()"),
                 self.updateActions)
    self.retranslate()
    return
  
  def retranslate(self):
    self.setWindowTitle(translate("Updating"))
    self.cancelButton.setText(translate("&Cancel"))
    return
  
  def updateActions(self):
    if 999 == self.bar.maximum() and self.updaterWorker.running == "yes":
      self.bar.setMaximum(self.updaterWorker.max)
      logging.log(4,self.updaterWorker.max)
    
    self.bar.setValue(self.updaterWorker.cnt)
    
    if self.updaterWorker.max == self.updaterWorker.cnt \
    and self.updaterWorker.running != "not started":
      self.updateDone()
      return False
    elif self.updaterWorker.running != "not started"\
    and self.updaterWorker.result != "not started":
      self.updateDone()
      self.res = "error " + str(inspect.currentframe().f_lineno)
      return False
    
    return True
  
  def updateDone(self):
    logging.log(4,"")
    self.bar.setValue(self.bar.maximum())
    self.timer.stop()
    self.hide()
    self.close()
    self.res="success"
    return
    
  def onCancel(self):
    logging.log(4,"")
    self.updaterWorker.stop()
    self.updateDone()
    self.bar.setValue(0)
    self.res="canceled"
    return
  
  def exec_(self):
    self.show()
    self.updaterWorker.trigger()
    self.updaterWorker.start()
    self.timer.start(100)
    QtGui.QDialog.exec_(self)
    self.updaterWorker.join()
    logging.log(4,self.res)
    if "canceled" == self.res:
      pass
    elif "success" == self.res:
      dialog=QtGui.QMessageBox(self)
      dialog.setWindowTitle("Finished")
      dialog.setText("Restarting the program is required to finish the update.")
      dialog.exec_()
    elif "failed" == self.res:
      dialog=QtGui.QMessageBox(self)
      dialog.setWindowTitle("Failed")
      dialog.setText("The update process failed. See " + self.logFileName + " for further information.")
      dialog.exec_()
    return self.res
  
class UpdaterWorker(threading.Thread):
  def __init__(self,path,version,baseUrl,versionFile,filesFile):
    self.abortFlag = False
    self.version = version
    self.versionUrl = baseUrl+versionFile
    self.filesUrl = baseUrl+filesFile
    self.baseUrl = baseUrl
    self.installationPath = path+"/"
    self.cnt = 0
    self.min = 0
    self.max = 0
    self.result = "not started"
    self.running = "not started"
    self.installedFiles=[]
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
    #be really sure that there are no empty lines
    self.files = os.linesep.join([s for s in self.files.splitlines() if s])
    self.files = os.linesep.join([s for s in self.files.splitlines() if 2 == len(s.split(" "))])
    logging.log(4,ver)
    return ver
  
  def isUpdateRequired(self):
    version = self.checkVersion()
    result = (self.version < version)
    logging.info(result)
    return result,version
  
  def run(self):
    rc = self.update()
    return rc
  
  def trigger(self):
    threading.Thread.__init__(self)
    self.cnt = 0
    self.min = 0
    self.max = 0
    self.result = "not started"
    self.running = "not started"
    self.installedFiles=[]
    return

  def update(self):
    logging.log(4,"")
    check,version = self.isUpdateRequired()
    if check:
      self.min = 0
      self.max = len(self.files.split("\n"))*3
      self.cnt=0
      self.running = "yes"
      updateContent={}
      for i in self.files.split("\n"):
        files=i.split(" ")
        file=self.installationPath+files[1]
        #store all currently installed files so they don't get deleted by removeNotInstalledFiles()
        self.installedFiles.append(file)
        if not os.access(file, os.W_OK):
          logging.error("No write permissions for "+file)
          raise OS.IOError
      #create backups
      for i in self.files.split("\n"):
        if not self.abortFlag:
          files=i.split(" ")
          shutil.copy2(self.installationPath+files[1],self.installationPath+files[1]+".backup")
          self.cnt+=1
      #get files from the internet
      try:
        for i in self.files.split("\n"):
          if not self.abortFlag:
            files=i.split(" ")
            newContent=self.getFile(version,files[0])
            updateContent[files[0]]=[files[1],newContent]
            self.cnt+=1
      except:
        logging.error("Unable to download")
        self.restore()
        self.result("failed")
        self.running("no")
        raise
      #write new files
      for val in updateContent.itervalues():
        if not self.abortFlag:
          try:
            targetFile = self.installationPath+val[0]
            stream = open(targetFile,"w")
            stream.write(val[1])
            stream.close()
            self.cnt+=1
          except:
            logging.error("Unable to write "+ targetFile)
            #restore backups
            self.restore()
            self.result = "failed"
            self.running = "no"
            return False
      #store all new installed files so they don't get deleted by removeNotInstalledFiles()
      if not self.abortFlag:
        for val in updateContent.itervalues():
          targetFile = self.installationPath+val[0]
          self.installedFiles.append(targetFile)
          
      if self.abortFlag:
        self.restore()
        
      self.removeNotInstalledFiles(self.installedFiles)
      self.result = "success"
      self.running = "no"
      return True
    logging.log(4,"")
    self.result = "success"
    self.running = "no"
    return False
  
  def restore(self):
    for i in self.files.split("\n"):
      files=i.split(" ")
      shutil.copy2(self.installationPath+files[1]+".backup",self.installationPath+files[1])
    self.removeNotInstalledFiles(self.installedFiles)
    return
  
  def removeNotInstalledFiles(self,installedFiles):
    logging.log(4,"")
    filesToDelete=findFilesInPathButNotInList(os.path.dirname(__file__),installedFiles)
    logging.log(4,"")
    for i in filesToDelete:
      logging.log(4,"Removing "+ i)
      os.remove(i)
    logging.log(4,"")
    return
  
  def getFile(self,version,fileSource):
    fileSource=self.baseUrl+fileSource+"?r="+version
    logging.log(4,fileSource)
    try:
      newContent = urllib.urlopen(fileSource).read()
      logging.log(4,"Got "+fileSource)
      return newContent
    except:
      logging.error("Unable to download "+fileSource)
      raise
    return None
  
  def getVersion(self):
    return self.version
  
  def stop(self):
    self.abortFlag = True
    return

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
  u.start()
  sys.exit(0)
