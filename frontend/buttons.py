#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from array import array
import struct

BEST_ICON_HEIGHT = 32


class BaseButton(QtGui.QFrame):
    def __init__(self, panel=None):
        super(BaseButton, self).__init__()

        self._active = False

    def setup_layout(self, direction, size_policy_x, size_policy_y):
        layout = QtGui.QBoxLayout(direction)
        layout.setSpacing(0)
        layout.setMargin(0)
        self.setLayout(layout)
        self.setSizePolicy(size_policy_x, size_policy_y)

    def init_ui(self):
        pass

    def connect_event_handlers(self):
        pass

    def mousePressEvent(self, event):
        '''Reimplement Qt mouse click event handler'''
        super(BaseButton, self).mousePressEvent(event)

    def on_left_button_click(self):
        '''Handle LMB click'''
        pass

    def on_right_button_click(self):
        '''Handle RMB click'''
        pass

    def update_style(self):
        '''Update widget to apply styles dependent on instance properties'''
        self.style().unpolish(self);
        self.style().polish(self);
        self.update();

    @QtCore.pyqtProperty(bool)
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active
        self.update_style()

    @QtCore.pyqtProperty(bool)
    def name(self):
        return self.label.text()

    @name.setter
    def name(self, name):
        self.label.setText(name)







class DesktopButton(QtGui.QFrame):
    """docstring for TaskButton"""
    def __init__(self, name, num, panel):
        super(DesktopButton, self).__init__()
        self.name = name
        self.num = num
        self._current = False

        panel.current_desktop_signal.connect(self.update_state)

        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.layout = QtGui.QHBoxLayout()
        self.setLayout(self.layout)
        self.label = QtGui.QLabel(name)
        self.layout.addWidget(self.label)

    def update_state(self, current_desktop_num):
        if current_desktop_num == self.num:
            self.current = True
        else:
            self.current = False

    def update_style(self):
        self.style().unpolish(self);
        self.style().polish(self);
        self.update();

    @QtCore.pyqtProperty(bool)
    def current(self):
        return self._current

    @current.setter
    def current(self, current):
        self._current = current
        self.update_style()
