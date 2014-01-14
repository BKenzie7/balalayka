#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import threading
import Queue
from PyQt4 import QtGui, QtCore

from gui.task_button import TaskButton
from gui.desktop_button import DesktopButton
from gui.container import Container

from xcomm.helpers import *
from xcomm.root import Root


LOOP_DELAY = 0.01


class Panel(Container):

    current_desktop_signal = QtCore.pyqtSignal(int)
    active_window_signal = QtCore.pyqtSignal(int)
    task_name_signal = QtCore.pyqtSignal(int, str)

    def __init__(self):
        super(Panel, self).__init__('main',
                                    None,
                                    QtGui.QBoxLayout.LeftToRight,
                                    QtGui.QSizePolicy.Expanding,
                                    QtGui.QSizePolicy.Expanding)

        self.event_queue = Queue.Queue()
        self.root = Root(self.event_queue)

        self.screen_info = QtGui.QDesktopWidget().availableGeometry()
        self.desktop_buttons = {}
        self.task_buttons = {}

        self.setWindowTitle('APanel')
        self.load_stylesheet()
        self.resize(self.screen_info.width(), 0)
        self.move(0, 0)

        self.desktops_widget = Container('desktops',
                                         self,
                                         QtGui.QBoxLayout.LeftToRight,
                                         QtGui.QSizePolicy.Fixed,
                                         QtGui.QSizePolicy.Expanding)

        self.tasks_widget = Container('tasks',
                                      self,
                                      QtGui.QBoxLayout.LeftToRight,
                                      QtGui.QSizePolicy.Expanding,
                                      QtGui.QSizePolicy.Expanding)

        self.populate_desktop_buttons()
        self.populate_task_buttons()
        self.show()
        self.set_window_flags()

    def load_stylesheet(self, filename='default.qss'):
        style_file = open(filename, 'r').read()
        self.setStyleSheet(style_file)

    def populate_desktop_buttons(self):
        for num, name in enumerate(self.root.desktops):
            desktop_button = DesktopButton(name, num, self)
            self.desktop_buttons[num] = desktop_button
            self.desktops_widget.layout().addWidget(desktop_button)

    def populate_task_buttons(self):
        for tid, task in self.root.tasks.items():
            task_button = TaskButton(task, self)
            self.task_buttons[tid] = task_button
            self.tasks_widget.layout().addWidget(task_button)

    def loop(self):
        while 1:
            while not self.event_queue.empty():
                event = self.event_queue.get()
                self.event_dispatcher(event)
                self.event_queue.task_done()
            time.sleep(LOOP_DELAY)

    def event_dispatcher(self, event):
        destination, type, data = event
        if destination == 'ROOT':
            if type == 'current_desktop':
                self.current_desktop_signal.emit(data)
            elif type == 'active_window':
                self.active_window_signal.emit(data)
        else:
            if type == 'name':
                self.task_name_signal.emit(destination, data)

    # TODO: События отсылаются всем кнопкам - Кто из них перерисуется?
    def set_active_window(self, id):
        print id
        send_event('ROOT', '_NET_ACTIVE_WINDOW', 'cardinal', [id])

    def set_current_desktop(self, num):
        print num
        send_event('ROOT', '_NET_CURRENT_DESKTOP', 'cardinal', [num])

    def set_window_flags(self):
        window_id = self.winId()
        dsp = display.Display()
        window = dsp.create_resource_object("window", window_id)
        height = self.height()

        set_window_property(window, '_NET_WM_WINDOW_TYPE', 'atom', ['_NET_WM_WINDOW_TYPE_DOCK'])
        set_window_property(window, '_NET_WM_STRUT', 'cardinal', [0, 0, height, 0])
        set_window_property(window, '_NET_WM_DESKTOP', 'cardinal', [0xffffffff])

        dsp.flush()


def backend():
    panel.root.loop()


def frontend():
    panel.loop()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    panel = Panel()

    backendThread = threading.Thread(target=backend)
    backendThread.daemon = True
    backendThread.start()

    frontendThread = threading.Thread(target=frontend)
    frontendThread.daemon = True
    frontendThread.start()

    sys.exit(app.exec_())