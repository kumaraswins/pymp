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

try:
  from PySide import QtCore, QtGui
except:
  from PyQt4 import QtCore, QtGui
from maemoUtils import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
        self.actionOpenLog = QtGui.QAction(MainWindow)
        self.actionOpenLog.setObjectName(_fromUtf8("actionOpenLog"))
        self.actionAddFile = QtGui.QAction(MainWindow)
        self.actionAddFile.setObjectName(_fromUtf8("actionAddFile"))
        self.actionAddDirectory = QtGui.QAction(MainWindow)
        self.actionAddDirectory.setObjectName(_fromUtf8("actionAddDirectory"))
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
        self.menuHelp.addAction(self.actionOpenLog)
        self.menuFile.addAction(self.actionAddFile)
        self.menuFile.addAction(self.actionAddDirectory)
        self.menuFile.addAction(self.actionLoadList)
        self.menuFile.addAction(self.actionSaveList)
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
        self.downloadButton.setText(QtGui.QApplication.translate("MainWindow", "S&tart", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("MainWindow", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPreferences.setTitle(QtGui.QApplication.translate("MainWindow", "&Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenLog.setText(QtGui.QApplication.translate("MainWindow", "&Open Logfile", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddFile.setText(QtGui.QApplication.translate("MainWindow", "Add &file(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddDirectory.setText(QtGui.QApplication.translate("MainWindow", "Add &directory", None, QtGui.QApplication.UnicodeUTF8))
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
    self.setupUi()  
    return
  
  def setupUi(self):
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
    self.inputBrowser.moveCursor(QtGui.QTextCursor.End)
    return
  
  def retranslate(self):
    self.groupBoxInput.setTitle(QtGui.QApplication.translate("MainWindow","Download &list", None, QtGui.QApplication.UnicodeUTF8))
    self.inputBrowser.setText(QtGui.QApplication.translate(
                                                           "MainWindow",
                                                           "# Insert the URLs to download or files to convert here. Put each in a new line.\n", 
                                                           None, 
                                                           QtGui.QApplication.UnicodeUTF8))
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
