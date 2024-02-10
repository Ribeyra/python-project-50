from formater.json import json
from formater.plain import plain
from formater.stylish import stylish
from gendiff.parser import parser
from gendiff.command import create_node, set_added, set_deleted, \
    set_changed


def collect_diff(data1: dict, data2: dict) -> dict:
    """
    Returns a dictionary containing the result of comparing the values
    of two dictionaries. For each key, the value will be a dictionary
    in which the element by the "type" key describes the change status
    ("unchg" - no changes, "del" - the key is deleted, "add" - the key
    is added, "mod" - the key value is changed).
    Can be done recursively.
    Example output:
       >>> pprint.pprint(vary(data1, data2))
       {'key1': {'type': 'mod', 'value': 'value1', 'new_value': 'true'},
        'key2': {'type': 'unchg',
                 'value': {'inner_key1': {'type': 'mod',
                                          'value': 'inner_value1',
                                          'new_value': 'some_value1'},
        ...
    """
    no_value = object()
    result = {}
    for key in sorted(set(data1) | set(data2)):
        old_value = data1.get(key, no_value)
        new_value = data2.get(key, no_value)
        create_node(result, key, old_value)
        if isinstance(old_value, dict) and isinstance(new_value, dict):
            create_node(result, key, collect_diff(old_value, new_value))
        elif new_value == no_value:
            set_deleted(result, key)
        elif old_value == no_value:
            create_node(result, key, new_value)
            set_added(result, key)
        elif old_value != new_value:
            set_changed(result, key, new_value)
    return result


def generate_diff(file1, file2, formater='stylish'):
    data1 = parser(file1)
    data2 = parser(file2)

    raw_diff = collect_diff(data1, data2)

    if formater == 'plain':
        return plain(raw_diff)
    elif formater == 'json':
        return json(raw_diff)
    return stylish(raw_diff)
