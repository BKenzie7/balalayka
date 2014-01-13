#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from array import array
import struct

BEST_ICON_HEIGHT = 32

class TaskButton(QtGui.QFrame):
    """docstring for TaskButton"""

    activate_signal = QtCore.pyqtSignal(int)

    def __init__(self, task, panel):
        super(TaskButton, self).__init__()

        # Initial stuff
        self.task = task
        self.panel = panel
        self._active = False

        # Checkink' connektionz, comrade!
        panel.active_window_signal.connect(self.update_state)
        panel.task_name_signal.connect(self.update_name)
        self.activate_signal.connect(panel.set_active_window)

        # Layout
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.layout = QtGui.QHBoxLayout()
        self.setLayout(self.layout)

        # Task icon
        self.get_icons()
        if self.icons:
            pixmap = self.get_icon(BEST_ICON_HEIGHT)['pixmap']
            self.icon = QtGui.QLabel()
            self.icon.setPixmap(pixmap)
            self.icon.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            self.layout.addWidget(self.icon)

        # Task label
        self.label = QtGui.QLabel(task.name, self)
        self.label.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        self.layout.addWidget(self.label)

    def mousePressEvent(self, event):
        '''Reimplement Qt mouse click event handler'''
        super(TaskButton, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.on_left_button_click()

    def on_left_button_click(self):
        '''Handle LMB click'''
        self.activate_signal.emit(self.task.id)

    def on_right_button_click(self):
        '''Handle RMB click'''
        pass

    def update_state(self, active_window_id):
        '''Update widget to apply styles dependent on instance properties'''
        if active_window_id == self.task.id:
            self.active = True
        else:
            self.active = False

    def update_icon(self):
        pass

    def update_style(self):
        for widget in [self, self.label]:
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()

    def update_name(self, destination_id, name):
        '''Update task name'''
        if destination_id == self.task.id:
            self.label.setText(name)

    @QtCore.pyqtProperty(bool)
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active
        self.update_style()

    def get_icons(self):
        if self.task.icon:
            # Get all icons of multiple sizes from window's _NET_WM_ICON property,
            # which is a flat list of integers, representing icon's dimensions
            # and ARGB pixel colors
            pos = 0
            icons = []
            while pos < len(self.task.icon):
                icon_width = self.task.icon[pos]
                icon_height = self.task.icon[pos+1]
                data_length = icon_width * icon_height
                data_start = pos + 2    # skip width and height values
                data_finish = data_start + data_length
                data = self.task.icon[data_start:data_finish]
                icons.append({
                    'width': icon_width,
                    'height': icon_height,
                    'data': data
                })
                pos = data_finish

            for icon in icons:
                # Convert icon's pixel data to byte string as unsigned integers (4 bytes each)
                argb_data = array('I', icon['data']).tostring()

                # New QImage from icon's data,
                # third argument is number of bytes in argb_data per line of image
                image = QtGui.QImage(
                    argb_data, icon['width'], icon['height'],
                    4 * icon['width'], QtGui.QImage.Format_ARGB32)

                # New QPixmap to use as image in a QLabel widget
                pixmap = QtGui.QPixmap.fromImage(image)
                icon['pixmap'] = pixmap

            self.icons = icons

        elif self.task.old_icon:
            # Some applications don't set _NET_WM_ICON (namely SDL-based games:
            # Wesnoth, RenPy VNs, etc), so we've got to take icon from WM_HINTS

            # Create icon's image pixmap and mask pixmap from their X11 counterparts
            pixmap = QtGui.QPixmap.fromX11Pixmap(self.task.old_icon['pixmap'].id, 0)
            mask_pixmap = QtGui.QPixmap.fromX11Pixmap(self.task.old_icon['mask'].id, 0)

            # Create and apply bitmap mask from mask pixmap
            mask_bitmap = QtGui.QBitmap(mask_pixmap)
            # pixmap.setMask(mask_bitmap)

            # Scale down pixmap to best height if necessary
            # if pixmap.height() > BEST_ICON_HEIGHT:
            #     pixmap = pixmap.scaledToHeight(BEST_ICON_HEIGHT, QtCore.Qt.SmoothTransformation)

            self.icons = [{
                'width': pixmap.width(),
                'height': pixmap.height(),
                'pixmap': pixmap
            }]
        else:
            self.icons = []

    def get_icon(self, height):
        # Get the most appropriate icon by it's height
        icon = min(self.icons, key = lambda i: abs(height - i['height']))

        # Scale down pixmap to best height if necessary
        if icon['height'] > height:
            icon['pixmap'] = icon['pixmap'].scaledToHeight(height, QtCore.Qt.SmoothTransformation)

        return icon
