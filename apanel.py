#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import Queue
import sys
from PyQt4 import QtGui
from xcomm.root import Root
from gui.panel import Panel
# from dummy import printer

app = QtGui.QApplication(sys.argv)
event_queue = Queue.Queue()
root = Root(event_queue)
panel = Panel(root, event_queue)


def backend():
    root.loop()


def frontend():
    panel.loop()
    # printer(event_queue)

if __name__ == "__main__":
    backendThread = threading.Thread(target=backend)
    backendThread.daemon = True
    backendThread.start()

    frontendThread = threading.Thread(target=frontend)
    frontendThread.daemon = True
    frontendThread.start()

    sys.exit(app.exec_())
