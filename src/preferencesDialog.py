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
    
    #
    #the grids
    #
    self.scrollAreaGeneral=QtGui.QScrollArea()
    self.gridWidgetGeneral=QtGui.QWidget(self.scrollAreaGeneral)
    self.gridLayoutGeneral=QtGui.QGridLayout(self.gridWidgetGeneral)
    self.gridWidgetGeneral.setLayout(self.gridLayoutGeneral)
    
    self.scrollAreaDownloader=QtGui.QScrollArea()
    self.gridWidgetDownloader=QtGui.QWidget(self.scrollAreaDownloader)
    self.gridLayoutDownloader=QtGui.QGridLayout(self.gridWidgetDownloader)
    self.gridWidgetDownloader.setLayout(self.gridLayoutDownloader)
    
    self.scrollAreaConverter=QtGui.QScrollArea()
    self.gridWidgetConverter=QtGui.QWidget(self.scrollAreaConverter)
    self.gridLayoutConverter=QtGui.QGridLayout(self.gridWidgetConverter)
    self.gridWidgetConverter.setLayout(self.gridLayoutConverter)
    
    #
    # the content of the several grids
    #
    
    #general tab content
    self.labelPath=QtGui.QLabel(self)
    self.labelPath.setText("Working directory")
    self.buttonPathOfUser=QtGui.QPushButton(self)
    self.buttonPathOfUser.setText("~")
    
    self.labelDownloads=QtGui.QLabel(self)
    self.labelDownloads.setText("Number of simultaneous downloads (needs transport bandwidth)")
    self.spinDownloads=QtGui.QSpinBox(self)
    self.spinDownloads.setMinimum(1)
    self.spinDownloads.setMaximum(999)
    
    self.labelConversions=QtGui.QLabel(self)
    self.labelConversions.setText("Number of simultaneous conversions (needs computing power)")
    self.spinConversions=QtGui.QSpinBox(self)
    self.spinConversions.setMinimum(1)
    self.spinConversions.setMaximum(999)
    
    #downloader tab content
    self.labelDownloaderVersion=QtGui.QLabel(self)
    self.labelDownloaderVersion.setText("Downloader Version (click to update)")
    self.buttonDownloaderVersion=QtGui.QPushButton(self)
    self.buttonDownloaderVersion.setText("...")
    
    self.labelRetry=QtGui.QLabel(self)
    self.labelRetry.setText("Number of download retries")
    self.spinRetry=QtGui.QSpinBox(self)
    self.spinRetry.setMinimum(0)
    self.spinRetry.setMaximum(99)
    
    self.labelDownloaderOverwrite=QtGui.QLabel(self)
    self.labelDownloaderOverwrite.setText("Downloader: Overwrite exisiting files")
    self.buttonDownloaderOverwrite=QtGui.QPushButton(self)
    self.buttonDownloaderOverwrite.setText("Overwrite")
    self.buttonDownloaderOverwrite.setCheckable(True)

    self.labelDownloaderContinue=QtGui.QLabel(self)
    self.labelDownloaderContinue.setText("Downloader: Continue partial downloaded files.")
    self.buttonDownloaderContinue=QtGui.QPushButton(self)
    self.buttonDownloaderContinue.setText("Continue")
    self.buttonDownloaderContinue.setCheckable(True)

    #converter tab contents
    self.labelConverterKbps=QtGui.QLabel(self)
    self.labelConverterKbps.setText("Converter: kbps")
    self.spinConverterKbps=QtGui.QSpinBox(self)
    self.spinConverterKbps.setMinimum(4)
    self.spinConverterKbps.setMaximum(512)
    
    #
    #ordering of layout content
    #
    
    #general tab
    rowCount=0
    columnCount=0
    self.gridLayoutGeneral.addWidget(self.labelPath,rowCount,columnCount)
    columnCount+=1
    self.gridLayoutGeneral.addWidget(self.buttonPathOfUser,rowCount,columnCount)

    rowCount+=1
    columnCount=0
    self.gridLayoutGeneral.addWidget(self.labelDownloads,rowCount,columnCount)
    columnCount+=1
    self.gridLayoutGeneral.addWidget(self.spinDownloads,rowCount,columnCount)

    rowCount+=1
    columnCount=0
    self.gridLayoutGeneral.addWidget(self.labelConversions,rowCount,columnCount)
    columnCount+=1
    self.gridLayoutGeneral.addWidget(self.spinConversions,rowCount,columnCount)
    
    #converter tab
    rowCount=0
    columnCount=0
    self.gridLayoutConverter.addWidget(self.labelConverterKbps,rowCount,columnCount)
    columnCount+=1
    self.gridLayoutConverter.addWidget(self.spinConverterKbps,rowCount,columnCount)
    
    #downloader tab
    rowCount=0
    columnCount=0
    self.gridLayoutDownloader.addWidget(self.labelDownloaderVersion,rowCount,columnCount)
    columnCount+=1
    self.gridLayoutDownloader.addWidget(self.buttonDownloaderVersion,rowCount,columnCount)
    rowCount+=1
    columnCount=0
    self.gridLayoutDownloader.addWidget(self.labelRetry,rowCount,columnCount)
    columnCount+=1
    self.gridLayoutDownloader.addWidget(self.spinRetry,rowCount,columnCount)
    rowCount+=1
    columnCount=0
    self.gridLayoutDownloader.addWidget(self.labelDownloaderOverwrite)
    columnCount+=1
    self.gridLayoutDownloader.addWidget(self.buttonDownloaderOverwrite)
    rowCount+=1
    columnCount=0
    self.gridLayoutDownloader.addWidget(self.labelDownloaderContinue)
    columnCount+=1
    self.gridLayoutDownloader.addWidget(self.buttonDownloaderContinue)
    
    #buttons
    self.buttonLayout=QtGui.QHBoxLayout()
    self.buttonLayout.addStretch()

    self.buttonOk=QtGui.QPushButton(self)
    self.buttonOk.setText("&Ok")
    self.buttonLayout.addWidget(self.buttonOk)
    self.buttonCancel=QtGui.QPushButton(self)
    self.buttonCancel.setText("&Cancel")
    self.buttonLayout.addWidget(self.buttonCancel)
    
    self.gridWidgetGeneral.show()
    self.gridWidgetConverter.show()
    self.gridWidgetDownloader.show()
    
    self.scrollAreaGeneral.setWidget(self.gridWidgetGeneral)
    self.scrollAreaGeneral.setWidgetResizable(True)
    self.scrollAreaConverter.setWidget(self.gridWidgetConverter)
    self.scrollAreaConverter.setWidgetResizable(True)
    self.scrollAreaDownloader.setWidget(self.gridWidgetDownloader)
    self.scrollAreaDownloader.setWidgetResizable(True)
    
    self.tabs=QtGui.QTabWidget(self)
    self.tabs.addTab(self.scrollAreaGeneral,translate("&General"))
    self.tabs.addTab(self.scrollAreaDownloader,translate("&Downloader"))
    self.tabs.addTab(self.scrollAreaConverter,translate("&Converter"))
    
    self.mainLayout.addWidget(self.tabs)
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
    self.labelDownloaderContinue.setText(translate("Continue partial downloaded files."))
    self.labelDownloaderOverwrite.setText(translate("Overwrite exisiting files"))
    self.labelConverterKbps.setText(translate("Data rate (kbps)"))
    self.buttonDownloaderContinue.setText(translate("Co&ntinue"))
    self.buttonDownloaderOverwrite.setText(translate("Over&write"))
    return
    
if __name__ == '__main__':
  import sys

  app = QtGui.QApplication(sys.argv) 
  dialog = Ui_PreferencesDialog()
  dialog.show()
  sys.exit(app.exec_())
