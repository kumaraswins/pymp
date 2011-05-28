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
from qtUtils import translate

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PreferencesDialog(QtGui.QDialog):
  def __init__(self):
    QtGui.QDialog.__init__(self)
    self.setupUi()
    return

  def setupUi(self):
    #prepare the window
    self.setObjectName(_fromUtf8("PreferencesDialog"))
#    self.resize(800, 480)
    self.mainLayout=QtGui.QVBoxLayout()
    self.setLayout(self.mainLayout)
    #the gridLayout
    self.scrollArea=QtGui.QScrollArea(self)
    self.gridWidget=QtGui.QWidget(self.scrollArea)
    self.gridLayout=QtGui.QGridLayout(self.gridWidget)
    self.gridWidget.setLayout(self.gridLayout)
    
    rowCount=0
    columnCount=0
    self.labelPath=QtGui.QLabel(self)
    self.labelPath.setText("Working directory")
    columnCount+=1
    self.buttonPathOfUser=QtGui.QPushButton(self)
    self.buttonPathOfUser.setText("~")
    
    rowCount+=1
    columnCount=0
    self.labelDownloads=QtGui.QLabel(self)
    self.labelDownloads.setText("Number of simultaneous downloads (needs transport bandwidth)")
    columnCount+=1
    self.spinDownloads=QtGui.QSpinBox(self)
    self.spinDownloads.setMinimum(1)
    self.spinDownloads.setMaximum(999)
    
    rowCount+=1
    columnCount=0
    self.labelConversions=QtGui.QLabel(self)
    self.labelConversions.setText("Number of simultaneous conversions (needs computing power)")
    columnCount+=1
    self.spinConversions=QtGui.QSpinBox(self)
    self.spinConversions.setMinimum(1)
    self.spinConversions.setMaximum(999)
    
    rowCount+=1
    columnCount=0
    self.labelDownloaderVersion=QtGui.QLabel(self)
    self.labelDownloaderVersion.setText("Downloader Version (click to update)")
    columnCount+=1
    self.buttonDownloaderVersion=QtGui.QPushButton(self)
    self.buttonDownloaderVersion.setText("...")
    
    rowCount+=1
    columnCount=0
    self.labelRetry=QtGui.QLabel(self)
    self.labelRetry.setText("Number of download retries")
    columnCount+=1
    self.spinRetry=QtGui.QSpinBox(self)
    self.spinRetry.setMinimum(0)
    self.spinRetry.setMaximum(99)
    
    rowCount+=1
    columnCount=0
    self.labelDownloaderOverwrite=QtGui.QLabel(self)
    self.labelDownloaderOverwrite.setText("Downloader: Overwrite exisiting files")
    columnCount+=1
    self.buttonDownloaderOverwrite=QtGui.QPushButton(self)
    self.buttonDownloaderOverwrite.setText("Overwrite")
    self.buttonDownloaderOverwrite.setCheckable(True)

    rowCount+=1
    columnCount=0
    self.labelDownloaderContinue=QtGui.QLabel(self)
    self.labelDownloaderContinue.setText("Downloader: Continue partial downloaded files.")
    columnCount+=1
    self.buttonDownloaderContinue=QtGui.QPushButton(self)
    self.buttonDownloaderContinue.setText("Continue")
    self.buttonDownloaderContinue.setCheckable(True)

    rowCount+=1
    columnCount=0
    self.labelConverterKbps=QtGui.QLabel(self)
    self.labelConverterKbps.setText("Converter: kbps")
    columnCount+=1
    self.spinConverterKbps=QtGui.QSpinBox(self)
    self.spinConverterKbps.setMinimum(4)
    self.spinConverterKbps.setMaximum(512)

    #ordering of layout content
    rowCount=0
    columnCount=0
    self.gridLayout.addWidget(self.labelPath,rowCount,columnCount)
    columnCount+=1
    self.gridLayout.addWidget(self.buttonPathOfUser,rowCount,columnCount)

    rowCount+=1
    columnCount=0
    self.gridLayout.addWidget(self.labelConversions,rowCount,columnCount)
    columnCount+=1
    self.gridLayout.addWidget(self.spinConversions,rowCount,columnCount)
    rowCount+=1
    columnCount=0
    self.gridLayout.addWidget(self.labelConverterKbps)
    columnCount+=1
    self.gridLayout.addWidget(self.spinConverterKbps)
    
    rowCount+=1
    columnCount=0
    self.gridLayout.addWidget(self.labelDownloaderVersion,rowCount,columnCount)
    columnCount+=1
    self.gridLayout.addWidget(self.buttonDownloaderVersion,rowCount,columnCount)
    rowCount+=1
    columnCount=0
    self.gridLayout.addWidget(self.labelDownloads,rowCount,columnCount)
    columnCount+=1
    self.gridLayout.addWidget(self.spinDownloads,rowCount,columnCount)
    rowCount+=1
    columnCount=0
    self.gridLayout.addWidget(self.labelRetry,rowCount,columnCount)
    columnCount+=1
    self.gridLayout.addWidget(self.spinRetry,rowCount,columnCount)
    rowCount+=1
    columnCount=0
    self.gridLayout.addWidget(self.labelDownloaderOverwrite)
    columnCount+=1
    self.gridLayout.addWidget(self.buttonDownloaderOverwrite)
    rowCount+=1
    columnCount=0
    self.gridLayout.addWidget(self.labelDownloaderContinue)
    columnCount+=1
    self.gridLayout.addWidget(self.buttonDownloaderContinue)
    
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
    self.scrollArea.setWidgetResizable(True)
    self.mainLayout.addWidget(self.scrollArea)
    self.mainLayout.addLayout(self.buttonLayout)
    self.retranslate()
    return
    
  def retranslate(self):
    self.labelPath.setText(translate("Working directory"))
    self.buttonPathOfUser.setText(translate("~"))
    self.labelDownloads.setText(translate("Number of simultaneous downloads (needs transport bandwidth)"))
    self.labelConversions.setText(translate("Number of simultaneous conversions (needs computing power)"))
    self.labelDownloaderVersion.setText(translate("Downloader Version (click to update)"))
    self.labelRetry.setText(translate("Number of download retries"))
    self.buttonOk.setText(translate("&Ok"))
    self.buttonCancel.setText(translate("&Cancel"))
    self.labelDownloaderContinue.setText(translate("Downloader: Continue partial downloaded files."))
    self.labelDownloaderOverwrite.setText(translate("Downloader: Overwrite exisiting files"))
    self.labelConverterKbps.setText(translate("Converter: kbps"))
    self.buttonDownloaderContinue.setText(translate("Co&ntinue"))
    self.buttonDownloaderOverwrite.setText(translate("Over&write"))
    return
    
if __name__ == '__main__':
  import sys

  app = QtGui.QApplication(sys.argv) 
  dialog = Ui_PreferencesDialog()
  dialog.show()
  sys.exit(app.exec_())
