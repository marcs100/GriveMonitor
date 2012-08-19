#!/usr/bin/python2.6

from systemtray import SystemTray
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sys

app = QApplication(sys.argv)
app.processEvents()
widget = QWidget()
trayIcon = SystemTray(QIcon("/usr/share/icons/GriveMonitor/google.png"), widget)
#trayIcon.setQApp(app) # pass reference to the QApplication so we can update events
trayIcon.show()
sys.exit(app.exec_())
