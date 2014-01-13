#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
from PyQt4 import QtGui, QtCore
from Xlib import Xatom, display
from task_button import TaskButton
from desktop_button import DesktopButton
from xcomm.helpers import *


class Panel(QtGui.QWidget):

    # backend_signal = QtCore.pyqtSignal(tuple)
    current_desktop_signal = QtCore.pyqtSignal(int)
    active_window_signal = QtCore.pyqtSignal(int)
    task_name_signal = QtCore.pyqtSignal(int, str)

    def __init__(self, root, event_queue):
        super(Panel, self).__init__()

        self.root = root
        self.event_queue = event_queue
        self.ui_init()
        self.load_stylesheet()
        # self.connect_signals()
        self.main_window.show()
        self.set_window_flags()

    def load_stylesheet(self, file = 'default.qss'):
        style_file = open(file, 'r').read()
        self.main_window.setStyleSheet(style_file)

    def ui_init(self):

        self.main_window, self.main_layout = self.create_container(
                'main', QtGui.QBoxLayout.LeftToRight,
                QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.main_window.setWindowTitle('APanel')
        self.screen_info = QtGui.QDesktopWidget().availableGeometry()
        self.main_window.resize(self.screen_info.width(), 10)
        self.main_window.move(0, 0)

        self.desktops_widget, self.desktops_layout = self.create_container(
                'desktops', QtGui.QBoxLayout.LeftToRight,
                QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.main_layout.addWidget(self.desktops_widget)

        self.tasks_widget, self.tasks_layout = self.create_container(
                'tasks', QtGui.QBoxLayout.LeftToRight,
                QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.main_layout.addWidget(self.tasks_widget)



        self.desktop_buttons = {}
        for num, name in enumerate(self.root.desktops):
            desktop_button = DesktopButton(name, num, self)
            self.desktop_buttons[num] = desktop_button
            self.desktops_layout.addWidget(desktop_button)

        self.task_buttons = {}
        for id, task in self.root.tasks.items():
            task_button = TaskButton(task, self)
            self.task_buttons[id] = task_button
            self.tasks_layout.addWidget(task_button)


    def window_setup(self):
        pass

    def loop(self):
        while 1:
            while not self.event_queue.empty():
                event = self.event_queue.get()
                self.event_dispatcher(event)
                self.event_queue.task_done()
            time.sleep(0.01)

    # def connect_signals(self):
    #     self.backend_signal.connect(self.event_dispatcher)

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

    def create_container(self, name, direction, size_policy_x, size_policy_y):
        widget = QtGui.QFrame()
        widget.setObjectName(name)
        layout = QtGui.QBoxLayout(direction)
        layout.setSpacing(0)
        layout.setMargin(0)
        widget.setLayout(layout)
        widget.setSizePolicy(size_policy_x, size_policy_y)
        return widget, layout

    def set_active_window(self, id):
        print id
        send_event('ROOT', '_NET_ACTIVE_WINDOW', 'cardinal', [id])


    def set_current_desktop(self, num):
        print num
        send_event('ROOT', '_NET_CURRENT_DESKTOP', 'cardinal', [num])


    def set_window_flags(self):
        window_id = self.main_window.winId()
        dsp = display.Display()
        window = dsp.create_resource_object("window", window_id)
        height = self.main_window.height()

        set_window_property(window, '_NET_WM_WINDOW_TYPE', 'atom', ['_NET_WM_WINDOW_TYPE_DOCK'])
        set_window_property(window, '_NET_WM_STRUT', 'cardinal', [0, 0, height, 0])
        set_window_property(window, '_NET_WM_DESKTOP', 'cardinal', [0xffffffff])

        dsp.flush()