def create_attribut(target, key, value):
    """
    Creates an attribute for a dictionary element, changing the value
    to list [' ', value].
    The first element of the list is an attribute that describes the status
    of the value change.
    """
    target[key] = [' ', value]


def added(target, key, attributes):
    """
    Adds attributes by key to the target dictionary.
    Changes the attribute that describes the change status of the value.
    """
    create_attribut(target, key, show_value(attributes))
    target[key][0] = '+'


def deleted(target, key, attributes):
    """
    Adds attributes by key to the target dictionary.
    Changes the attribute that describes the change status of the value.
    """
    create_attribut(target, key, show_value(attributes))
    target[key][0] = '-'


def changed(target, key, old_attributes, new_attributes):
    """
    Adds attributes by key to the target dictionary.
    Adds a new value to the attributes.
    Changes the attribute that describes the change status of the value.
    """
    create_attribut(target, key, show_value(old_attributes))
    target[key].append(show_value(new_attributes))
    target[key][0] = '*'


def show_value(attributes):
    """
    Returns the value of a dictionary element from attributes
    """
    return attributes[1]


def show_new_value(attributes):
    """
    Returns the new value of a dictionary element from attributes
    """
    return attributes[2]


def show_status(attributes):
    """
    Returns the change status of a dictionary element from attributes
    """
    return attributes[0]
