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
import os,re,logging,types,tempfile,subprocess,sys,webbrowser
from PyQt4 import QtGui, QtCore
from qtUtils import *
from ui import *
from aboutdialog import Ui_AboutDialog
from maemoUtils import *
from downloadWorker import DownloadWorker
from convertWorker import ConvertWorker
from preferencesDialog import Ui_PreferencesDialog
from settings import Settings

class ProgressPage(QtGui.QWidget):
  def __init__(self,information,settings):
    global LOG_FILENAME
    QtGui.QWidget.__init__(self)
    self.settings = settings
    self.boxLayout = QtGui.QHBoxLayout(self)
    self.boxLayout.setObjectName("boxLayout")
    self.setLayout(self.boxLayout)
    self.groupBox = QtGui.QGroupBox(self)
    self.groupBox.setObjectName("groupBox")
    self.boxLayout.addWidget(self.groupBox)

    self.scrollArea = QtGui.QScrollArea(self)
    self.gridWidget= QtGui.QWidget(self.scrollArea)
    self.mainLayout = QtGui.QGridLayout()
    self.mainLayout.setObjectName("mainLayout")
    self.gridWidget.setLayout(self.mainLayout)
    self.scrollLayout = QtGui.QHBoxLayout()
    
    self.lines = len(information)
    self.widgets=[]
    rowCnt=0
    columnCnt=0
    headerCnt=0
    label=QtGui.QLabel(self)
    label.setText(translate("Url"))
    self.mainLayout.addWidget(label,rowCnt+headerCnt,columnCnt)
    columnCnt+=1
    label=QtGui.QLabel(self)
    label.setText(translate("Step"))
    self.mainLayout.addWidget(label,rowCnt+headerCnt,columnCnt)
    columnCnt+=1
    label=QtGui.QLabel(self)
    label.setText(translate("Filename"))
    self.mainLayout.addWidget(label,rowCnt+headerCnt,columnCnt)
    columnCnt+=1
    label=QtGui.QLabel(self)
    label.setText(translate("Progress"))
    self.mainLayout.addWidget(label,rowCnt+headerCnt,columnCnt)
    columnCnt+=1
    headerCnt+=1
    for key,val in information.iteritems():
      columnCnt=0
      self.widgets.append([])
      textEdit = QtGui.QTextBrowser(self)
      textEdit.setText(self.htmlLink(key,True))
      textEdit.setReadOnly(True)
      textEdit.setOpenExternalLinks(True)
      textEdit.setOpenLinks(False)
      self.connect(textEdit,
                   QtCore.SIGNAL("anchorClicked(QUrl)"),
                   self.redirect)
      self.widgets[rowCnt].append(textEdit)
      self.mainLayout.addWidget(self.widgets[rowCnt][len(self.widgets[rowCnt])-1],
                                rowCnt+headerCnt,
                                columnCnt)
      columnCnt+=1
      textEdit = QtGui.QTextBrowser(self)
      textEdit.setText(val["state"])
      textEdit.setReadOnly(True)
      textEdit.setOpenExternalLinks(True)
      textEdit.setOpenLinks(False)
      self.connect(textEdit,
                   QtCore.SIGNAL("anchorClicked(QUrl)"),
                   self.redirect)
      self.widgets[rowCnt].append(textEdit)
      self.mainLayout.addWidget(self.widgets[rowCnt][len(self.widgets[rowCnt])-1],
                                rowCnt+headerCnt,
                                columnCnt)
      columnCnt+=1
      textEdit = QtGui.QTextBrowser(self)
      textEdit.setOpenExternalLinks(True)
      textEdit.setOpenLinks(False)
      textEdit.setReadOnly(True)
      self.connect(textEdit,
                   QtCore.SIGNAL("anchorClicked(QUrl)"),
                   self.redirect)
      textEdit.setText(self.htmlLink(val["file"]))
      self.widgets[rowCnt].append(textEdit)
      self.mainLayout.addWidget(self.widgets[rowCnt][len(self.widgets[rowCnt])-1],
                                rowCnt+headerCnt,
                                columnCnt)
      columnCnt+=1
      bar = QtGui.QProgressBar(self)
      bar.setMinimum(0)
      bar.setMaximum(100)
      bar.setValue(0)
      self.widgets[rowCnt].append(bar)
      self.mainLayout.addWidget(self.widgets[rowCnt][len(self.widgets[rowCnt])-1],
                                rowCnt+headerCnt,
                                columnCnt)
      columnCnt+=1
      rowCnt+=1
    
    self.gridWidget.show()
    self.scrollArea.setWidget(self.gridWidget)
    self.scrollArea.setWidgetResizable(True)
    self.scrollLayout.addWidget(self.scrollArea)
    self.groupBox.setLayout(self.scrollLayout)
    self.retranslate()
    self.updateContent(information)
    return
  
  def retranslate(self):
    self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow","&Progress information", None, QtGui.QApplication.UnicodeUTF8))
    return
  
  def redirect(self,url):
    if type(url) == QtCore.QUrl:
      qurl=url
      url=str(url.toString())
    else:
      url = str(url)
      qurl=QtCore.QUrl(url)
      
    logging.debug(url)
    logging.debug(qurl)
    if isMaemo5():
      if  url.find("http") >= 0\
          or re.search(os.path.basename(LOG_FILENAME),url):
        QtGui.QDesktopServices.openUrl(qurl)
      else:
        subprocess.Popen(["osso-xterm -e \"%s %s\""%(self.settings["mplayer.path"],os.path.abspath(url))],shell=True)
    elif os.name == 'mac':
      subprocess.Popen(('open', url))
    elif os.name == 'nt':
      subprocess.Popen(('start', url))
    elif os.name == 'posix':
      QtGui.QDesktopServices.openUrl(qurl)
    elif type(qurl) == QtCore.QUrl:
      QtGui.QDesktopServices.openUrl(qurl)
  
  def htmlLink(self,link,force=False):
    toReturn=""
    try:
      words=link.split(" ")
      for i in words:
        toReturn+=self.singleLink(i, force)
        toReturn+=" "
      toReturn=toReturn.rstrip()
    finally:
      return toReturn
  
  def singleLink(self,link,force=False):
    if None == link:
      toReturn = ""
    elif  os.path.isfile(link):
      toReturn="<a href=\""+os.path.abspath(link)+"\">"+link+"</a>"
    elif link.find("http") or force == True:
      toReturn="<a href=\""+link+"\">"+link+"</a>"
    else:
      toReturn=link
    return toReturn
  
  def updateContent(self,information):
    rowCnt=0
    columnCnt=0
    for key,val in information.iteritems():
      columnCnt=0
      #url
      if self.htmlLink(key, True) != self.widgets[rowCnt][columnCnt].toPlainText():
        self.widgets[rowCnt][columnCnt].setText(self.htmlLink(key,True))
      columnCnt+=1
      #step information
      if val["state"] != self.widgets[rowCnt][columnCnt].toPlainText():
        self.widgets[rowCnt][columnCnt].setText(val["state"])
      columnCnt+=1
      #file information
      if val.has_key("converted"):
        strn=val["converted"]+" "+val["file"]
      else:
        strn=val["file"]
      if  val["file"] != None \
          and strn != self.widgets[rowCnt][columnCnt].toPlainText():
        self.widgets[rowCnt][columnCnt].setText(self.htmlLink(strn))
      columnCnt+=1
      #progress bar
      progress = val["totalProgress"]
      if type(val["totalProgress"]) is str:
        progress = progress.replace('%','')
      progress = float(progress)
      logging.debug("%i %s"%(progress,val["file"]))
      self.widgets[rowCnt][columnCnt].setValue(progress)
      columnCnt+=1
      rowCnt+=1
  
class AboutDialog(QtGui.QDialog, Ui_AboutDialog):
  def __init__(self,name,url,bugs):
    self.name=name
    self.url=url
    self.bugtracker=bugs
    QtGui.QDialog.__init__(self) 
    self.setupUi(self)
    
class PreferencesDialog(Ui_PreferencesDialog):
  def __init__(self,settings):
    Ui_PreferencesDialog.__init__(self)
    self.setWindowTitle(translate("Preferences"))
    self.settings=settings
    self.readSettings()
    self.connect(self.buttonCancel,
                 QtCore.SIGNAL("clicked()"),
                 QtCore.SLOT("close()"))
    self.connect(self.buttonOk,
                 QtCore.SIGNAL("clicked()"),
                 self.onOk)
    self.connect(self.buttonPathOfUser,
                 QtCore.SIGNAL("clicked()"),
                 self.changePath)
    self.connect(self.buttonDownloaderVersion,
                 QtCore.SIGNAL("clicked()"),
                 self.updateDownloader)
    self.updateContent()
    return
  
  def updateContent(self):
    self.updateDirectoryButton()
    self.updateVersionButton()
    self.spinDownloads.setValue(int(self.settings["numberOfSimultaniousDownloads"]))
    self.spinConversions.setValue(int(self.settings["numberOfSimultaniousConversions"]))
    self.spinRetry.setValue(int(self.settings["download.numberOfRetries"]))
    if self.settings["download.continue"] == "True":
      self.buttonDownloaderContinue.setChecked(True)
    if self.settings["download.overwrite"] == "True":
      self.buttonDownloaderOverwrite.setChecked(True)
    self.spinConverterKbps.setValue(int(self.settings["converter.kbps"]))
    return

  def readSettings(self):
    self.settings.readFromFile()

  def saveSettings(self):
    self.settings.writeToFile()

  def onOk(self):
    self.settings["download.numberOfRetries"]=str(self.spinRetry.value())
    self.settings["numberOfSimultaniousConversions"]=str(self.spinConversions.value())
    self.settings["numberOfSimultaniousDownloads"]=str(self.spinDownloads.value())
    if self.buttonDownloaderContinue.isChecked() == True:
      self.settings["download.continue"] = "True"
    else:
      self.settings["download.continue"] = "False"
    if self.buttonDownloaderOverwrite.isChecked() == True:
      self.settings["download.overwrite"] = "True"
    else:
      self.settings["download.overwrite"] = "False"
    self.settings["converter.kbps"]=str(self.spinConverterKbps.value())
    self.saveSettings()
    self.close()
    return

  def changePath(self):
    dir=QtGui.QFileDialog.getExistingDirectory(parent=self, 
                                               caption="Set working directory")
    if dir != "":
      self.settings["workingDirectory"]=str(dir)
    self.updateDirectoryButton()
    return
  
  def updateDirectoryButton(self):
    self.buttonPathOfUser.setText(os.path.basename(self.settings["workingDirectory"]))
    return

  def updateDownloader(self):
    self.tmpFile = tempfile.TemporaryFile()
    self.errFile = tempfile.TemporaryFile()
    sts=subprocess.call([self.settings["download.downloader.path"],"-U"],
                        stderr=self.errFile,
                        stdout=self.tmpFile)
    self.updateVersionButton()
    
  def updateVersionButton(self):
    self.tmpFile = tempfile.TemporaryFile()
    self.errFile = tempfile.TemporaryFile()
    sts=subprocess.call([self.settings["download.downloader.path"],"-v"],
                        stderr=self.errFile,
                        stdout=self.tmpFile)
    self.tmpFile.seek(0)
    version=self.tmpFile.read().rstrip()
    logging.debug(version)
    self.buttonDownloaderVersion.setText(version)

class Ui(QtGui.QMainWindow, Ui_MainWindow):
  def __init__(self):
    global LOG_FILENAME
    QtGui.QMainWindow.__init__(self)
    #directory setup
    global LOG_PATH
    global PATH
    self.settingsPath=LOG_PATH
    self.installationPath=PATH
    self.settings=Settings(self.settingsPath+"/pymprc",PATH)
    self.readSettings()
    self.timer = QtCore.QTimer()
    self.setupUi(self)
    
    #signals and slot stuff
    self.connect(self.timer,
                 QtCore.SIGNAL("timeout()"),
                 self.updateActions)
    #actions
    self.connect(self.actionAbout, 
                 QtCore.SIGNAL("triggered()"),
                 self.onAbout)
    self.connect(self.actionAddFile,
                 QtCore.SIGNAL("triggered()"),
                 self.onAddFile)
    self.connect(self.actionAddDirectory,
                 QtCore.SIGNAL("triggered()"),
                 self.onAddDirectory)
    self.connect(self.actionLoadList,
                 QtCore.SIGNAL("triggered()"),
                 self.onLoadList)
    self.connect(self.actionSaveList,
                 QtCore.SIGNAL("triggered()"),
                 self.onSaveList)
    self.connect(self.actionExit,
                 QtCore.SIGNAL("triggered()"),
                 QtCore.SLOT("close()"))
    self.connect(self.actionPreferences,
                 QtCore.SIGNAL("triggered()"),
                 self.onPreferences)
    #buttons
    self.connect(self.downloadButton,
                 QtCore.SIGNAL("clicked()"),
                 self.onDownload)
    self.connect(self.cancelButton, 
                 QtCore.SIGNAL("clicked()"),
                 self.onCancel)
    self.connect(self.actionOpenLog,
                 QtCore.SIGNAL("triggered()"),
                 self.onOpenLog)
    
    self.pNumbers=re.compile(r"([0-9]*)")
    self.progressPage = None
    self.downloaders = None
    self.converters = None
    self.closeWhenFinished = False
    return
  
  def __del__(self):
    self.settings.writeToFile()
    return
  
  def readSettings(self):
    self.settings.readFromFile()
    try:
      os.chdir(self.settings["workingDirectory"])
    except:
      pass #dont change the directory
    return
  
  def performActions(self):
    """
    Concept:
    1. Determine all files to download
    2. Assign worker to each of the items. Workers are threads. How many workers are allowed is defined
    via preferences.
    3. The worker creates:
    4. Create a itemized list which looks like this:
    urlname (from the "from" list) - status (downloading/converting) - progress-bar
    5. Worker starts downloading
    6. Worker updates its progress
    """
    #init downloaders
    if None == self.downloaders:
      self.downloaders= [DownloadWorker(self.settings) for i in range(int(self.settings["numberOfSimultaniousDownloads"]))]
      for i in self.downloaders:
        i.setDaemon(True)
        i.start()
    else:
      for i in self.downloaders:
        i.prepare()
      DownloadWorker.resultLock.acquire()
      DownloadWorker.result = {}
      DownloadWorker.resultLock.release()
    #init converters
    if None == self.converters:
      self.converters = [ConvertWorker(self.settings) for i in range(int(self.settings["numberOfSimultaniousConversions"]))]
      for i in self.converters:
        i.setDaemon(True)
        i.start()
    else:
      for i in self.converters:
        i.prepare()
      ConvertWorker.resultLock.acquire()
      ConvertWorker.result = {}
      ConvertWorker.resultLock.release()
    
    self.results = {}
    for url in self.downloadList:
      if  os.path.isfile(os.path.abspath(url))\
          and url not in ConvertWorker.result.keys():
        ConvertWorker.addResult(url,"queued 0%",True)
        self.results[url] = {"state": "Queued for converting",
                             "file": url,
                             "totalProgress": 50,
                             "stepProgress": 0}
      elif os.path.isdir(os.path.abspath(url)):
        list = os.listdir(url)
        for f in list:
          if  os.path.isfile(f)\
              and f not in ConvertWorker.result.keys():
            logging.debug(f)
            ConvertWorker.addResult(f,"queued 0%",True)
            self.results[f] = {"state": "Queued for converting",
                               "file": f,
                               "totalProgress": 50,
                               "stepProgress": 0}
      elif url not in DownloadWorker.result.keys():
        if True == DownloadWorker.addResult(url,"queued 0%",True):
          self.results[url] = {"state": "Queued for downloading",
                               "file": "",
                               "totalProgress": 0,
                               "stepProgress": 0}
    logging.debug(self.results)
    self.timer.start(300)
    self.updateActions()
    return
  
  def updateDownloaderStatus(self):
    pQueued=re.compile(r"queued",re.IGNORECASE)
    downloadCnt=0
    downloadDoneCnt=0
    downloadErrorCnt=0
    DownloadWorker.resultLock.acquire()
    for url,state in DownloadWorker.result.iteritems():
      downloadCnt+=1
      if  state["state"].find("done") >= 0\
          or state["state"].find("error") >= 0:
        downloadDoneCnt+=1
        if  type(state["file"]) == types.NoneType\
            or not os.path.isfile(state["file"]):
          self.results[url]["file"] = state["file"]
          self.results[url]["state"] = "Download error. See <a href=\"" +LOG_FILENAME+ "\">"+LOG_FILENAME+"</a> for more information."
          self.results[url]["stepProgress"] = "100%"
          self.results[url]["totalProgress"] = "100%"
          downloadErrorCnt+=1
        elif state["file"] not in ConvertWorker.result.keys()  and self.checkBoxMp3.isChecked():
          self.results[url]["file"] = state["file"]
          self.results[url]["state"] = "Queued for converting"
          self.results[url]["stepProgress"] = "100%"
          self.results[url]["totalProgress"] = "50%"
          ConvertWorker.addResult(state["file"],"queued 0%",True)
        elif not self.checkBoxMp3.isChecked():
          self.results[url]["file"] = state["file"]
          self.results[url]["state"] = "done"
          self.results[url]["stepProgress"] = "100%"
          self.results[url]["totalProgress"] = "100%"
      else:
        if  self.results[url]["state"] != "Downloading" \
            and not pQueued.search(state["state"]):
          self.results[url]["state"] = "Downloading"
        self.results[url]["stepProgress"] = state["state"]
        self.results[url]["file"] = state["file"]
        steps=1
        if self.checkBoxMp3.isChecked():
          steps+=1
        total=float(filter(None,self.pNumbers.findall(state["state"]))[0])/steps
        self.results[url]["totalProgress"] = "%.1lf%%" %(total)
    DownloadWorker.resultLock.release()
    return downloadCnt,downloadDoneCnt,downloadErrorCnt
  
  def updateConverterStatus(self):
    pQueued=re.compile(r"queued",re.IGNORECASE)
    converterDoneCnt = 0
    converterCnt = 0
    converterErrorCnt = 0
    if self.checkBoxMp3.isChecked():
      ConvertWorker.resultLock.acquire()
      for cfile,state in ConvertWorker.result.iteritems():
        converterCnt+=1
        for key,value in self.results.iteritems():
          try:
            if re.match(cfile,value["file"]):
              #Does the state need to be updated?
              if  (value["state"] != "Converting" \
                  or not value["state"].find("done")\
                  or not value["state"].find("error"))\
                  and not pQueued.search(state["state"]):
                value["state"] = "Converting"
              
              value["stepProgress"] = state["state"]
              if state["state"].find("done") >= 0:
                value["state"] = state["state"]
                converterDoneCnt+=1
                total=100
                value["converted"] = state["workingFile"]
              elif  state["state"].find("error") >= 0:
                value["state"] = "Conversion error. See <a href=\"" +LOG_FILENAME+ "\">"+LOG_FILENAME+"</a> for more information."
                converterDoneCnt+=1
                converterErrorCnt+=1
                total=100
                value["converted"] = ""
              else:
                steps=1
                offset=0
                if  self.checkBoxFlash.isChecked() \
                    or not os.path.isfile(os.path.abspath(key)):
                  steps+=1
                  offset=50
                total=float(filter(None,self.pNumbers.findall(state["state"]))[0])/steps+offset
              value["totalProgress"] = "%.1lf%%" %(total)
          except TypeError:
            pass
      ConvertWorker.resultLock.release()
    return converterCnt,converterDoneCnt,converterErrorCnt

  
  def updateActions(self):
    downloadDoneCnt=0
    downloadCnt=0
    downloadErrorCnt=0
    converterDoneCnt=0
    converterCnt=0
    converterErrorCnt=0
    downloadCnt,downloadDoneCnt,downloadErrorCnt = self.updateDownloaderStatus()
    converterCnt,converterDoneCnt,converterErrorCnt = self.updateConverterStatus()
    
    logging.debug(self.results)
    logging.debug("%i %i %i %i %i %i %i %i"
                  %(len(DownloadWorker.result),
                    downloadCnt,
                    downloadDoneCnt,
                    downloadErrorCnt,
                    len(ConvertWorker.result),
                    converterCnt,
                    converterDoneCnt,
                    converterErrorCnt))
    
    if None == self.progressPage:
      self.progressPage = ProgressPage(self.results,self.settings)
      self.pages.addWidget(self.progressPage)
      self.pages.setCurrentWidget(self.progressPage)
      self.pages.setCurrentIndex(self.pages.count()-1)
      self.progressPage.show()
      self.downloadButton.hide()
      self.cancelButton.show()
      self.checkBoxFlash.setDisabled(True)
      self.checkBoxMp3.setDisabled(True)
    else:
      self.progressPage.updateContent(self.results)
    
    if downloadCnt == downloadDoneCnt and downloadCnt > 0:
      if self.checkBoxMp3.isChecked() and downloadDoneCnt > downloadErrorCnt:
        if converterCnt == converterDoneCnt and converterCnt > 0:
          self.uiAfterActions()
      else:
        self.uiAfterActions()
    elif  self.checkBoxMp3.isChecked() \
          and downloadCnt == 0: #file actions
      if converterCnt == converterDoneCnt and converterCnt > 0:
        self.uiAfterActions()

    return
  
  def uiAfterActions(self):
    self.timer.stop()
    self.progressPage.updateContent(self.results)
    self.cancelButton.setText("&Done")
    if True == self.closeWhenFinished:
      self.close()
    return
  
  def onCancel(self):
    return self.cleanAfterDownload()
    
  def cleanAfterDownload(self):
    logging.debug(" ")
    for i in self.converters:
      i.killSubprocess()
    for i in self.downloaders:
      i.killSubprocess()
    DownloadWorker.queue.join()
    ConvertWorker.queue.join()
    self.timer.stop()
    if not self.checkBoxFlash.isChecked():
      DownloadWorker.resultLock.acquire()
      for val in DownloadWorker.result.itervalues():
        if val["file"] and os.path.isfile(val["file"]):
          os.remove(val["file"])
      DownloadWorker.resultLock.release()
    
    self.pages.removeWidget(self.progressPage)
    self.checkBoxFlash.setDisabled(False)
    self.checkBoxMp3.setDisabled(False)
    self.cancelButton.hide()
    self.cancelButton.setText("&Cancel")
    self.downloadButton.show()
    del(self.progressPage)
    self.progressPage = None
    return
  
  def onDownload(self):
    logging.debug(" ")
    toDl=str(self.inputPage.inputBrowser.toPlainText())
    lines=toDl.split("\n")
    self.downloadList=[]
    cnt=0
    for line in lines:
      newLine=re.sub(r"#.*",r"",line)
      if newLine != "" and (self.checkBoxMp3.isChecked() or self.checkBoxFlash.isChecked()):
        self.downloadList.append(newLine)
        cnt+=1
    if 0 == cnt:
      dialog=QtGui.QMessageBox(self)
      infoStr="Nothing found to be done."
      dialog.setWindowTitle(infoStr)
      if (self.checkBoxMp3.isChecked() or self.checkBoxFlash.isChecked()):
        dialog.setText(infoStr+"\n\nYou may forgot to enter a URL.")
      else:
        dialog.setText(infoStr+"\n\nYou forgot to check on of the check boxes right next to the download button.")
      if True == self.closeWhenFinished:
        print(dialog.text())
        sys.exit(0)
      dialog.exec_()
    else:
      self.performActions()
    return
  
  def onAddFile(self):
    toAdd=QtGui.QFileDialog.getOpenFileNames(parent=self,
                                             caption=translate("Select file(s)"))
    self.inputPage.inputBrowser.setText(self.inputPage.inputBrowser.toPlainText()+"\n"+toAdd.join("\n"))
    self.checkBoxMp3.setChecked(True)
    return

  def onAddDirectory(self):
    toAdd=QtGui.QFileDialog.getExistingDirectory(parent=self,
                                                 caption=translate("Select directory"))
    self.inputPage.inputBrowser.setText(self.inputPage.inputBrowser.toPlainText()+"\n"+toAdd)
    self.checkBoxMp3.setChecked(True)
    return

  def onLoadList(self):
    listFile=QtGui.QFileDialog.getOpenFileName(parent=self,
                                               caption=translate("Select download list"))
    return self.loadFile(listFile)

  def loadFile(self,file):
    if os.path.isfile(file):
      f=open(file,"r")
      self.inputPage.inputBrowser.setText(f.read())
      f.close()

  def onSaveList(self):
    file=QtGui.QFileDialog.getSaveFileName(parent=self, 
                                           caption=translate("Save to convertingFile"))
    content=self.inputPage.inputBrowser.toPlainText()
    f=open(file,"w")
    f.write(content)
    f.close()
  
  def onAbout(self):
    dlg=AboutDialog(self.windowTitle(),
               "https://sites.google.com/site/markusscharnowski/pc-software/pymp-youtube-downloader-and-mp3-converter",
               "https://code.google.com/p/pymp/issues/list")
    dlg.exec_()
    return
  
  def onOpenLog(self):
    dlg=QtGui.QDialog(self)
    layout=QtGui.QHBoxLayout(dlg)
    dlg.setLayout(layout)
    textb=QtGui.QTextBrowser(dlg)
    layout.addWidget(textb)
    f=open(LOG_FILENAME,"r")
    textb.setText(LOG_FILENAME+"\n"+f.read())
    f.close
    textb.show()
    dlg.resize(800, 480)
    dlg.exec_()
    return
    
  def onPreferences(self):
    dlg=PreferencesDialog(self.settings)
    dlg.exec_()
    self.readSettings()
    return


if __name__ == '__main__':
  import optparse
  parser=optparse.OptionParser(usage="usage: %prog [options] url1 url2")
  parser.add_option("-D", 
                    "--debug",
                    dest="debugLevel",
                    action="store",
                    type="int",
                    default=20,
                    help="""Set the debug output level (default %default). The lower the number, the more gets logged. Example levels are:
CRITICAL 50\n
ERROR 40\n
WARNING 30\n
INFO 20\n
DEBUG 10""")
  parser.add_option("-l", 
                    "--list",
                    dest="listFile",
                    action="store",
                    type="str",
                    help="""Load a file containing a download list""")
  parser.add_option("-c", 
                    "--close",
                    dest="close",
                    action="store_true",
                    default="store_false",
                    help="""Close and exit when finished.""")
  parser.add_option("-d", 
                    "--download",
                    dest="download",
                    action="store_true",
                    default="store_false",
                    help="""Start downloading immediatly. Needs either --video or --mp3.""")
  parser.add_option("-m", 
                    "--mp3",
                    dest="downloadMp3",
                    action="store_true",
                    default="store_false",
                    help="""Check the mp3 button.""")
  parser.add_option("-v", 
                    "--video",
                    dest="downloadVideo",
                    action="store_true",
                    default="store_false",
                    help="""Check the video button.""")
  (options, args) = parser.parse_args()
  """
#For Testing:
http://www.youtube.com/watch?v=lfEDO1uZxVA
http://www.youtube.com/watch?v=bJAyLYR71NM&NR=1
http://www.youtube.com/watch?v=jrZHxIA0eVU&feature=related
http://www.youtube.com/watch?v=O5sd_CuZxNc
http://www.youtube.com/watch?v=O5sd_CuZxNcaa
  """
  #logger
  LOG_PATH=os.path.expanduser("~/."+os.path.basename(__file__))
  PATH=os.path.dirname(os.path.realpath(__file__))
  if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
  LOG_FILENAME=LOG_PATH+"/"+os.path.basename(__file__)+".log"
  logging.basicConfig(
                      filename=LOG_FILENAME,
                      filemode="w",
                      level=options.debugLevel,
                      format = "%(asctime)s %(levelname)s %(process)s %(thread)s %(module)s %(funcName)s %(lineno)s: %(message)s",
                      datefmt = "%F %H:%M:%S")
  logging.info(options.debugLevel)
  logging.debug(PATH)
  logging.debug(LOG_PATH)
  app = QtGui.QApplication(sys.argv)
  ui = Ui() 
  ui.show()
  #option processing
  if options.close:
    if True == options.close:
      ui.closeWhenFinished = True
  if options.listFile:
    ui.loadFile(options.listFile)
  if options.downloadMp3:
    if True == options.downloadMp3:
      ui.checkBoxMp3.setChecked(True)
  if options.downloadVideo:
    if True == options.downloadVideo:
      ui.checkBoxFlash.setChecked(True)
  #add command line arguments to the input browser
  for i in args:
    text=str(ui.inputPage.inputBrowser.toPlainText())
    text+="\n"+i
    ui.inputPage.inputBrowser.setText(text)
  if options.download:
    if True == options.download:
      ui.onDownload()
  sys.exit(app.exec_())
