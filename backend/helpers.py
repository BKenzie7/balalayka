#!/usr/bin/python
# -*- coding: utf-8 -*-

from Xlib import X, Xatom, display

dsp = display.Display()


def simplify_property_values(values, transform_function = lambda x: x):
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
        # print property_type, raw_value

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
