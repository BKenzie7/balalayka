#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class DesktopButton(QtGui.QFrame):

    current_signal = QtCore.pyqtSignal(int)

    def __init__(self, name, num, panel):
        super(DesktopButton, self).__init__()
        self.name = name
        self.num = num
        self._current = False

        panel.current_desktop_signal.connect(self.update_state)
        self.current_signal.connect(panel.set_current_desktop)

        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.layout = QtGui.QHBoxLayout()
        self.setLayout(self.layout)
        # self.label = QtGui.QLabel(self.name)
        self.label = QtGui.QLabel(str(self.num))
        self.layout.addWidget(self.label)

    def mousePressEvent(self, event):
        '''Reimplement Qt mouse click event handler'''
        super(DesktopButton, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.on_left_button_click()

    def on_left_button_click(self):
        '''Handle LMB click'''
        self.current_signal.emit(self.num)

    def on_right_button_click(self):
        '''Handle RMB click'''
        pass

    def update_state(self, current_desktop_num):
        if current_desktop_num == self.num:
            self.current = True
        else:
            self.current = False

    def update_style(self):
        for widget in [self, self.label]:
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()

    @QtCore.pyqtProperty(bool)
    def current(self):
        return self._current

    @current.setter
    def current(self, current):
        self._current = current
        self.update_style()
