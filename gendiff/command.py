"""This module describes the data abstraction used in the project"""


def create_node(target, key, value):
    """
    Creates an attribute for a dictionary element, changing the value
    to list [' ', value].
    The first element of the list is an attribute that describes the status
    of the value change.
    """
    target[key] = {'type': 'unchg', 'value': value}


def set_added(target, key):
    """
    Changes the attribute that describes the change status of the value.
    """
    target[key]['type'] = 'add'


def set_deleted(target, key):
    """
    Changes the attribute that describes the change status of the value.
    """
    target[key]['type'] = 'del'


def set_changed(target, key, new_value):
    """
    Adds a new_value to the attributes.
    Changes the attribute that describes the change status of the value.
    """
    target[key]['new_value'] = new_value
    target[key]['type'] = 'mod'


def get_node(data, key):
    return data[key]


def get_value(data):
    """
    Returns the value of a dictionary element from attributes
    """
    if isinstance(data, dict):
        return data.get('value', data)
    return data


def get_new_value(data):
    """
    Returns the new value of a dictionary element from attributes
    """
    if isinstance(data, dict):
        return data.get('new_value', data)
    return data


def get_status(data):
    """
    Returns the change status of a dictionary element from attributes
    """
    if isinstance(data, dict):
        return data.get('type', 'unchg')
    return 'unchg'
