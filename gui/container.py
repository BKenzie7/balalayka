#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui


class Container(QtGui.QFrame):
    """Basic stylable container widget"""
    # TODO: Named arguments with defaults
    def __init__(self, name, parent, layout_direction, size_policy_x, size_policy_y):
        # super(Container, self).__init__(parent)
        super(Container, self).__init__()
        if parent:
            parent.layout().addWidget(self)
        self.setObjectName(name)
        layout = QtGui.QBoxLayout(layout_direction)
        layout.setSpacing(0)
        layout.setMargin(0)
        self.setLayout(layout)
        self.setSizePolicy(size_policy_x, size_policy_y)

    def reapply_stylesheet(self):
        for widget in [self]:
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()
