#!/usr/bin/python
# -*- coding: utf-8 -*-

from Xlib import X
from helpers import *


class Task(object):
    '''Task class'''

    def __init__(self, id, display, event_queue):
        self.id = id
        self.display = display
        self.event_queue = event_queue
        self.window = self.display.create_resource_object('window', self.id)
        self.window.change_attributes(event_mask=(
                X.PropertyChangeMask | X.FocusChangeMask | X.StructureNotifyMask))

    def x_event_dispatcher(self, event):
        if event.type == X.PropertyNotify:
            atom = self.display.get_atom_name(event.atom)
            if atom in ['_NET_WM_STATE']:
                self.send_event('state', self.state)
            elif atom in ['_NET_WM_NAME']:
                self.send_event('name', self.name)
            elif atom in ['_NET_WM_ICON', '_NET_WM_ICON_GEOMETRY']:
                self.send_event('icon')
            elif atom in ['_NET_WM_DESKTOP']:
                self.send_event('desktop', self.desktop)

    def gui_event_dispatcher(self):
        pass

    def send_event(self, type, data=None):
        event = (self.id, type, data)
        self.event_queue.put(event)

    @property
    def name(self):
        return get_property_by_atom_name('_NET_WM_NAME', self.window)

    @property
    def state(self):
        return get_property_by_atom_name('_NET_WM_STATE', self.window)

    @property
    def desktop(self):
        return get_property_by_atom_name('_NET_WM_DESKTOP', self.window)

    @property
    def type(self):
        return get_property_by_atom_name('_NET_WM_WINDOW_TYPE', self.window)

    @property
    def icon(self):
        return get_property_by_atom_name('_NET_WM_ICON', self.window)

    @property
    def old_icon(self):
        hints = self.window.get_wm_hints()
        icon = {
            'pixmap': hints.icon_pixmap,
            'mask': hints.icon_mask,
            'width': hints.icon_x,
            'height': hints.icon_y,
            'window': hints.icon_window
        }
        return icon
