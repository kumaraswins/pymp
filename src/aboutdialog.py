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
from qtUtils import *
from maemoUtils import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AboutDialog(object):
  def __init__(self,name,version,url,bugs):
    self.name=name
    self.version=version
    self.url=url
    self.bugtracker=bugs
  
  def setupUi(self, Dialog):
    #prepare the window
    Dialog.setObjectName(_fromUtf8("Dialog"))
    if isMaemo5():
      Dialog.resize(800, 480)
    else:
      Dialog.resize(600, 400)
      
    #the layout
    self.layout=QtGui.QVBoxLayout(Dialog)
    self.setLayout(self.layout)
    #some tabs
    self.tabs=QtGui.QTabWidget(Dialog)
    self.layout.addWidget(self.tabs)
    #some browsers
    self.browserDonate=QtGui.QTextBrowser(self.tabs)
    self.browserDonate.setOpenExternalLinks(True)
    self.browserDonate.setOpenLinks(False)
    self.browserGeneral=QtGui.QTextBrowser(self.tabs)
    self.browserGeneral.setOpenExternalLinks(True)
    self.browserGeneral.setOpenLinks(False)
    self.browserWebsite=QtGui.QTextBrowser(self.tabs)
    self.browserWebsite.setOpenExternalLinks(True)
    self.browserWebsite.setOpenLinks(False)
    self.browserFeedback=QtGui.QTextBrowser(self.tabs)
    self.browserFeedback.setOpenExternalLinks(True)
    self.browserFeedback.setOpenLinks(False)
    #insert the tabs
    tabCnt=1
    self.tabs.insertTab(tabCnt, self.browserGeneral,
                        QtGui.QApplication.translate(
                                                     "Dialog", "&General", None, 
                                                     QtGui.QApplication.UnicodeUTF8))
    tabCnt+=1
    self.tabs.insertTab(tabCnt, self.browserFeedback,
                        QtGui.QApplication.translate(
                                                     "Dialog", "&Feedback", None, 
                                                     QtGui.QApplication.UnicodeUTF8))
    tabCnt+=1
    self.tabs.insertTab(tabCnt, self.browserWebsite,
                        QtGui.QApplication.translate(
                                                     "Dialog", "&Website", None, 
                                                     QtGui.QApplication.UnicodeUTF8))
    tabCnt+=1
    self.tabs.insertTab(tabCnt, self.browserDonate,
                        QtGui.QApplication.translate(
                                                     "Dialog", "&Donate", None, 
                                                     QtGui.QApplication.UnicodeUTF8))

    
    #uff nearly done
    self.connect(self.browserGeneral,
                 QtCore.SIGNAL("anchorClicked(QUrl)"),
                 self.redirect)
    self.connect(self.browserWebsite,
                 QtCore.SIGNAL("anchorClicked(QUrl)"),
                 self.redirect)
    self.connect(self.browserDonate,
                 QtCore.SIGNAL("anchorClicked(QUrl)"),
                 self.redirect)
    self.connect(self.browserFeedback,
                 QtCore.SIGNAL("anchorClicked(QUrl)"),
                 self.redirect)
    self.retranslateUi(Dialog)
    QtCore.QMetaObject.connectSlotsByName(Dialog)

  def redirect(self,url):
    QtGui.QDesktopServices.openUrl(url)
    return

  def retranslateUi(self, Dialog):
    x=str("About "+self.name)
    Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", x, None, QtGui.QApplication.UnicodeUTF8))
    self.browserDonate.setText(translate(
        "You like what you have in your hands? You use it on regular basis? "\
        "Support the development by making a donation."\
        "<p>Donate through "\
        "<a href=\"https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=TPX9PV29D4L9Y\">paypal</a></p>"\
        "<p>Visit the projects <a href=\"http://sites.google.com/site/markusscharnowski/donate\">donation website</a></p>"
        ))
    self.browserWebsite.setText(translate(
        "<p>Visit</p>"\
        "<p>"\
        "<a href=\""+ self.url + "\">" + self.url + "</a>"\
        "</p>"\
        "<p>"\
        "<a href=\"http://sites.google.com/site/markusscharnowski\">http://sites.google.com/site/markusscharnowski</a>"\
        "</p>"
        ))
    self.browserFeedback.setText(translate(
        "<p>Do you have ideas for improving the program? You want a specific functionality? "
        "You have found a bug?</p>"
        "<p><a href=\""+self.bugtracker+"\">Bugtracker</a></p>"
        "<p>Email <a href=\"mailto:markus.scharnowski@gmail.com?subject=SW Feedback " + self.windowTitle() +
        " &body=Hello Markus,\">Feedback</a></p>"
        ))
    self.browserGeneral.setText(translate(
        "<p>" + str(self.name) + " " + self.version + "</p>"\
#        "<p>Test <a href=\"file:////home/markus/workspace/eclipse/python/pymp/test/Aladdin_intro_German-bJAyLYR71NM.flv\">test.flv</a></p>"\
#        "<p>Test <a href=\"file:////home/markus/workspace/eclipse/python/pymp/test/Aladdin_intro_German-bJAyLYR71NM.flv.mp3\">test.flv.mp3</a></p>"\
#        "<p>Test <a href=\"x\">test</a></p>"\
        "<p>Concept and programming: <a href=\"mailto:markus.scharnowski@gmail.com?subject=Thank you for " + self.name +
        "&body=Hello Markus,\">Markus Scharnowski</a></p>"\
        """
<p><h1>License</h1></p>
<p>
""" + str(self.name) + """ is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or any later version.
</p><p>
""" + str(self.name) + """ is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
</p><p>
You should have received a copy of the GNU General Public License
along with """ + str(self.name) + """.  If not, see <a href="http://www.gnu.org/licenses/">gnu.org</a>.
</p>
        """
        ))

if __name__ == '__main__':
  import sys,os
  class MyWindow(QtGui.QDialog, Ui_AboutDialog): 
    def __init__(self,name,version,url,bugs):
      self.name=str(name)
      self.version=version
      self.url=url
      self.bugtracker=bugs
      QtGui.QDialog.__init__(self) 
      self.setupUi(self)

  app = QtGui.QApplication(sys.argv) 
  dialog = MyWindow(os.path.basename(__file__),"0.0test","http://sites.google.com/site/markusscharnowski/123","http://code.google.com/p/push-it/issues/list")
  dialog.show() 
  sys.exit(app.exec_())
