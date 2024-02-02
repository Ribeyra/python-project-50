import argparse
from formater.json import json
from formater.plain import plain
from formater.stylish import stylish
from gendiff.parser import parser
from gendiff.command import create_attribut, set_added, set_deleted, \
    set_changed, get_value


def cli():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )

    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')

    args = parser.parse_args()

    print(generate_diff(args.first_file, args.second_file, args.format))


def replace_bool_or_None_to_str(value):
    if value is True:
        value = 'true'
    elif value is False:
        value = 'false'
    elif value is None:
        value = 'null'
    return value


def add_atribut(data):
    """
    Appends attribute to dictionary elements.
    If the value is a dictionary, execute recursively.
    """
    for key, value in data.items():
        if isinstance(value, dict):
            add_atribut(value)
            create_attribut(data, key, value)
        else:
            create_attribut(data, key, replace_bool_or_None_to_str(value))


def compar_values(data, key, value, new_value):
    """
    Changes an attribute depending on the result of the comparison
    """
    create_attribut(data, key, value)
    if new_value is None:
        set_deleted(data, key)
    elif value is None:
        create_attribut(data, key, new_value)
        set_added(data, key)
    elif value != new_value:
        set_changed(data, key, new_value)


def collect_diff(data1: dict, data2: dict) -> dict:
    """
    Returns a dictionary containing the result of comparing the values
    of two dictionaries. For each key, the value will be a list,
    the first element of which describes the change status (' ' - no change,
    '-' - key deleted, '+' - key added, '*' - key value changed).
    Can be run recursively.
    Example output:
       >>> pprint.pprint(vary(data1, data2))
       {'general': [' ',
               {'follow':   ['+', 'false'],
                'setting1': [' ', 'Value 1'],
                'setting2': ['-', 200],
                'setting3': ['*', 'true', 'null'],
                'setting4': ['+', 'blah blah'],
                'setting5': ['+', {'key5': [' ', 'value5']}],
                'setting6': [' ',
                             {'doge': [' ', {'wow': ['*', '', 'so much']}],
                              'key':  [' ', 'value'],
                              'oops': ['+', 'whoops']}]}],
        ...
    """
    no_attributes = [None, None]
    result = {}
    for key in sorted(set(data1) | set(data2)):
        attributes1 = data1.get(key, no_attributes)
        attributes2 = data2.get(key, no_attributes)
        value, new_value = get_value(attributes1), get_value(attributes2)
        if isinstance(value, dict) and isinstance(new_value, dict):
            create_attribut(result, key, collect_diff(value, new_value))
        else:
            compar_values(result, key, value, new_value)
    return result


def generate_diff(file1, file2, formater='stylish'):
    data1 = parser(file1)
    add_atribut(data1)

    data2 = parser(file2)
    add_atribut(data2)

    raw_diff = collect_diff(data1, data2)

    if formater == 'plain':
        result = plain(raw_diff)
    elif formater == 'json':
        result = json(raw_diff)
    else:
        result = stylish(raw_diff)
    return result
