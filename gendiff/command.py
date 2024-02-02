"""This module describes the data abstraction used in the project"""


def create_attribut(target, key, value):
    """
    Creates an attribute for a dictionary element, changing the value
    to list [' ', value].
    The first element of the list is an attribute that describes the status
    of the value change.
    """
    target[key] = [' ', value]


def set_added(target, key):
    """
    Changes the attribute that describes the change status of the value.
    """
    target[key][0] = '+'


def set_deleted(target, key):
    """
    Changes the attribute that describes the change status of the value.
    """
    target[key][0] = '-'


def set_changed(target, key, new_value):
    """
    Adds a new_value to the attributes.
    Changes the attribute that describes the change status of the value.
    """
    target[key].append(new_value)
    target[key][0] = '*'


def get_value(attributes):
    """
    Returns the value of a dictionary element from attributes
    """
    return attributes[1]


def get_new_value(attributes):
    """
    Returns the new value of a dictionary element from attributes
    """
    return attributes[2]


def get_status(attributes):
    """
    Returns the change status of a dictionary element from attributes
    """
    return attributes[0]
