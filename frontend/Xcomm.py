#!/usr/bin/python
# -*- coding: utf-8 -*-

from Xlib import X, Xatom, display
import Xlib.protocol.event

dsp = display.Display()
screen = dsp.screen()
root = screen.root

def send_event(destination, property, type, data):
    if destination == 'ROOT':
        destination = root
    property = dsp.intern_atom(property)
    if type == 'atom':
        data = map(lambda x: dsp.intern_atom(x), data)
    data = (data + [0] * (5 - len(data)))[:5]
    event = Xlib.protocol.event.ClientMessage(
        window=destination, client_type=property, data=(32, data))
    mask = (X.SubstructureRedirectMask|X.SubstructureNotifyMask)
    dsp.send_event(root, event, event_mask=mask, propagate = 0)
    dsp.flush()


def set_window_property(window, property, type, value_list):
    if window == 'ROOT':
        window = root
    property = dsp.intern_atom(property)
    if type == 'atom':
        type = Xatom.ATOM
        value_list = map(lambda v: dsp.intern_atom(v), value_list)
    elif type == 'cardinal':
        type = Xatom.CARDINAL
    window.change_property(property, type, 32, value_list)