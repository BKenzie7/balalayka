#!/usr/bin/python
# -*- coding: utf-8 -*-

from Xlib import X, Xatom, display
import Xlib.protocol.event

dsp = display.Display()
screen = dsp.screen()
root = screen.root


def simplify_property_values(values, transform_function=lambda x: x):
    if len(values) == 1:
        return transform_function(values[0])
    elif len(values) > 1:
        result = []
        for value in values:
            value = transform_function(value)
            result.append(value)
        return result
    else:
        return None


def get_property(atom, obj):
    result = None
    full_property = obj.get_full_property(atom, X.AnyPropertyType)

    if full_property:
        property_type = dsp.get_atom_name(full_property.property_type)
        raw_value = full_property.value

        if property_type == 'UTF8_STRING':
            result = raw_value
        elif property_type == 'WINDOW':
            result = simplify_property_values(raw_value)
        elif property_type == 'CARDINAL':
            result = simplify_property_values(raw_value, int)
        elif property_type == 'ATOM':
            result = simplify_property_values(raw_value, dsp.get_atom_name)
        else:
            result = 'RAWR'

    return result


def get_property_by_atom_name(atom_name, obj):
    atom = dsp.intern_atom(atom_name)
    return get_property(atom, obj)


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
    dsp.send_event(root, event, event_mask=mask, propagate=0)
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