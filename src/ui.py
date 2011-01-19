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

from PyQt4 import QtCore, QtGui
from maemoUtils import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

def translate(self,string):
  return QtGui.QApplication.translate("MainWindow", string, None, QtGui.QApplication.UnicodeUTF8)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #prepare the window
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 480)
        
        #set the central widget
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(MainWindow.geometry())
        self.widget.setObjectName(_fromUtf8("widget"))
        
        #central gridLayout
        self.horizontalLayout = QtGui.QVBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.centralwidget.setLayout(self.horizontalLayout)
        

        self.pages = QtGui.QStackedWidget(self.widget)
        self.horizontalLayout.addWidget(self.pages)
        self.inputPage = InputPage()
        self.pages.addWidget(self.inputPage)
        
        #gridLayout on the right
        self.verticalLayoutRight = QtGui.QHBoxLayout()
        self.verticalLayoutRight.setObjectName(_fromUtf8("verticalLayoutRight"))
        self.horizontalLayout.addLayout(self.verticalLayoutRight)
        self.verticalLayoutRight.addStretch()
        
        #check box flash
        self.checkBoxFlash = QtGui.QCheckBox(self.widget)
        self.checkBoxFlash.setObjectName(_fromUtf8("checkBoxFlash"))
        self.verticalLayoutRight.addWidget(self.checkBoxFlash)
        #check box mp3
        self.checkBoxMp3 = QtGui.QCheckBox(self.widget)
        self.checkBoxMp3.setObjectName(_fromUtf8("checkBoxMp3"))
        self.verticalLayoutRight.addWidget(self.checkBoxMp3)
        #download button
        self.downloadButton = QtGui.QPushButton(self.widget)
        self.downloadButton.setObjectName(_fromUtf8("downloadButton"))
        self.verticalLayoutRight.addWidget(self.downloadButton)
        self.cancelButton = QtGui.QPushButton(self.widget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.cancelButton.hide()
        self.verticalLayoutRight.addWidget(self.cancelButton)

        #menu actions
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.action_Set_working_directory = QtGui.QAction(MainWindow)
        self.action_Set_working_directory.setObjectName(_fromUtf8("action_Set_working_directory"))
        self.actionLoadList = QtGui.QAction(MainWindow)
        self.actionLoadList.setObjectName(_fromUtf8("actionLoadList"))
        self.actionSaveList = QtGui.QAction(MainWindow)
        self.actionSaveList.setObjectName(_fromUtf8("actionSaveList"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionPreferences"))

        #menu
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        #menu bar menus
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName(_fromUtf8("menuPreferences"))
        #menu add actions
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionLoadList)
        self.menuFile.addAction(self.actionSaveList)
        self.menuPreferences.addAction(self.action_Set_working_directory)
        self.menuPreferences.addAction(self.actionPreferences)
        if not isMaemo5():
          self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

#        #statusbar
#        self.statusbar = QtGui.QStatusBar(MainWindow)
#        self.statusbar.setObjectName(_fromUtf8("statusbar"))
#        MainWindow.setStatusBar(self.statusbar)
        
        #uff nearly done
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow","pymp", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxFlash.setText(QtGui.QApplication.translate("MainWindow", "Flash &video", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxMp3.setText(QtGui.QApplication.translate("MainWindow", "&Mp3", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadButton.setText(QtGui.QApplication.translate("MainWindow", "&Download", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("MainWindow", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPreferences.setTitle(QtGui.QApplication.translate("MainWindow", "&Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Set_working_directory.setText(QtGui.QApplication.translate("MainWindow", "Set working &directory", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoadList.setText(QtGui.QApplication.translate("MainWindow", "&Load download list", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveList.setText(QtGui.QApplication.translate("MainWindow", "&Save download list", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "&Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("MainWindow", "&Preferences", None, QtGui.QApplication.UnicodeUTF8))
    
    def changeDownloadButtonText(self,string):
      self.downloadButton.setText(QtGui.QApplication.translate("MainWindow", string, None, QtGui.QApplication.UnicodeUTF8))
      return self.downloadButton.text()

class InputPage(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)
    self.mainLayout = QtGui.QHBoxLayout(self)
    self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
    self.setLayout(self.mainLayout)
    
    self.groupBoxInput = QtGui.QGroupBox(self)
    self.mainLayout.addWidget(self.groupBoxInput)
    self.inputLayout=QtGui.QVBoxLayout()
    self.inputLayout.setObjectName(_fromUtf8("inputLayout"))
    self.inputBrowser = QtGui.QTextBrowser(self)
    #input box
    self.groupBoxInput.setObjectName(_fromUtf8("groupBoxInput"))
    self.groupBoxInput.setLayout(self.inputLayout)
    #input textbrowser
    self.inputBrowser.setObjectName(_fromUtf8("inputBrowser"))
    self.inputBrowser.setReadOnly(False)
    self.inputLayout.addWidget(self.inputBrowser)
    
    self.retranslate()
    return
  
  def retranslate(self):
    self.groupBoxInput.setTitle(QtGui.QApplication.translate("MainWindow","Download &list", None, QtGui.QApplication.UnicodeUTF8))
    self.inputBrowser.setText(QtGui.QApplication.translate("MainWindow","# Insert the URLs to download here. Put each in a new line.\n", None, QtGui.QApplication.UnicodeUTF8))
    return

class PreferencesDialog(QtGui.QDialog):
  def __init__(self):
    QtGui.QDialog.__init__(self)
    self.setupUi(self)
    return

  def setupUi(self, Dialog):
    #prepare the window
    Dialog.setObjectName(_fromUtf8("Dialog"))
    Dialog.resize(800, 480)
    self.mainLayout=QtGui.QVBoxLayout(Dialog)
    self.setLayout(self.mainLayout)
    #the gridLayout
    self.scrollArea=QtGui.QScrollArea()
    self.gridWidget=QtGui.QWidget(self.scrollArea)
    self.gridLayout=QtGui.QGridLayout(self.gridWidget)
    self.gridWidget.setLayout(self.gridLayout)
    
    rowCount=0
    columnCount=0
    self.labelPath=QtGui.QLabel(self)
    self.labelPath.setText("Working directory")
    self.gridLayout.addWidget(self.labelPath,rowCount,columnCount)
    columnCount+=1
    self.buttonPathOfUser=QtGui.QPushButton(self)
    self.buttonPathOfUser.setText("~")
    self.gridLayout.addWidget(self.buttonPathOfUser,rowCount,columnCount)
    rowCount+=1
    columnCount=0
    self.labelDownloads=QtGui.QLabel(self)
    self.labelDownloads.setText("Number of simultaneous downloads (needs transport bandwidth)")
    self.gridLayout.addWidget(self.labelDownloads,rowCount,columnCount)
    columnCount+=1
    self.spinDownloads=QtGui.QSpinBox(self)
    self.spinDownloads.setMinimum(1)
    self.spinDownloads.setMaximum(999)
    self.gridLayout.addWidget(self.spinDownloads,rowCount,columnCount)
    rowCount+=1
    columnCount=0
    self.labelConversions=QtGui.QLabel(self)
    self.labelConversions.setText("Number of simultaneous conversions (needs computing power)")
    self.gridLayout.addWidget(self.labelConversions,rowCount,columnCount)
    columnCount+=1
    self.spinConversions=QtGui.QSpinBox(self)
    self.spinConversions.setMinimum(1)
    self.spinConversions.setMaximum(999)
    self.gridLayout.addWidget(self.spinConversions,rowCount,columnCount)
    rowCount+=1
    columnCount=0
    self.labelDownloaderVersion=QtGui.QLabel(self)
    self.labelDownloaderVersion.setText("Downloader Version (click to update)")
    self.gridLayout.addWidget(self.labelDownloaderVersion,rowCount,columnCount)
    columnCount+=1
    self.buttonDownloaderVersion=QtGui.QPushButton(self)
    self.buttonDownloaderVersion.setText("...")
    self.gridLayout.addWidget(self.buttonDownloaderVersion,rowCount,columnCount)
    rowCount+=1
    columnCount=0
    self.labelRetry=QtGui.QLabel(self)
    self.labelRetry.setText("Number of download retries")
    self.gridLayout.addWidget(self.labelRetry,rowCount,columnCount)
    columnCount+=1
    self.spinRetry=QtGui.QSpinBox(self)
    self.spinRetry.setMinimum(0)
    self.spinRetry.setMaximum(99)
    self.gridLayout.addWidget(self.spinRetry,rowCount,columnCount)
    
    self.buttonLayout=QtGui.QHBoxLayout()
    self.buttonLayout.addStretch()

    self.buttonOk=QtGui.QPushButton(self)
    self.buttonOk.setText("&Ok")
    self.buttonLayout.addWidget(self.buttonOk)
    self.buttonCancel=QtGui.QPushButton(self)
    self.buttonCancel.setText("&Cancel")
    self.buttonLayout.addWidget(self.buttonCancel)
    
    self.gridWidget.show()
    self.scrollArea.setWidget(self.gridWidget)
    self.mainLayout.addWidget(self.scrollArea)
    self.mainLayout.addLayout(self.buttonLayout)
    return
    
  def retranslate(self):
    self.labelPath.setText("Working directory")
    self.buttonPathOfUser.setText("~")
    return
    

  
if __name__ == '__main__':
    import sys
    class MyWindow(QtGui.QMainWindow, Ui_MainWindow): 
        def __init__(self): 
            QtGui.QMainWindow.__init__(self) 
            self.setupUi(self)

    app = QtGui.QApplication(sys.argv) 
    dialog = MyWindow() 
    dialog.show() 
    sys.exit(app.exec_())