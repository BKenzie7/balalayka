#!/usr/bin/python
# -*- coding: utf-8 -*-

from Xlib import X, Xatom, display
from task import Task
from helpers import get_property, get_property_by_atom_name
import time

LOOP_DELAY = 0.01


class Root(object):
    def __init__(self, event_queue):
        self.event_queue = event_queue
        self.display = display.Display()
        self.screen = self.display.screen()
        self.root_window = self.screen.root
        self.root_window.change_attributes(event_mask = (X.PropertyChangeMask))

    @property
    def tasks(self):
        current_tasks_ids = get_property_by_atom_name('_NET_CLIENT_LIST', self.root_window)
        banned_types = ['_NET_WM_WINDOW_TYPE_DESKTOP', '_NET_WM_WINDOW_TYPE_DOCK']
        banned_states = []
        # TODO: Check banned states like _NET_WM_STATE_SKIP_TASKBAR
        # TODO: Multiple types
        tasks = {}
        for id in current_tasks_ids:
            task = Task(id, self.display, self.event_queue)
            if task.type not in banned_types:
                tasks[id] = task
        return tasks

    @property
    def desktops(self):
        desktops_string = get_property_by_atom_name('_NET_DESKTOP_NAMES', self.root_window)
        # desktops_string is a string of desktop names separated by '\x00'
        desktops = filter(lambda s: len(s) != 0, desktops_string.split('\x00'))
        return desktops

    @property
    def current_desktop(self):
        return get_property_by_atom_name('_NET_CURRENT_DESKTOP', self.root_window)

    @property
    def active_window(self):
        return get_property_by_atom_name('_NET_ACTIVE_WINDOW', self.root_window)

    def loop(self):
        while 1:
            while self.display.pending_events():
                event = self.display.next_event()
                if hasattr(event, 'window'):
                    # Handle window event
                    if event.window.id in self.tasks:
                        self.tasks[event.window.id].event_dispatcher(event)
                    # Handle WM event
                    elif event.window.id == self.root_window.id:
                        self.event_dispatcher(event)
            # Slow the fuck down
            time.sleep(LOOP_DELAY)

    def send_event(self, type, data = None):
        event = ('ROOT', type, data)
        self.event_queue.put(event)

    def event_dispatcher(self, event):
        if event.type == X.PropertyNotify:
            atom = self.display.get_atom_name(event.atom)
            if atom == '_NET_CURRENT_DESKTOP':
                self.send_event('current_desktop', self.current_desktop)
            elif atom in ['_NET_NUMBER_OF_DESKTOPS', '_NET_DESKTOP_NAMES']:
                self.send_event('desktops', self.desktops)
            elif atom == '_NET_CLIENT_LIST':
                self.send_event('tasks', self.tasks)
            elif atom == '_NET_ACTIVE_WINDOW':
                self.send_event('active_window', self.active_window)
