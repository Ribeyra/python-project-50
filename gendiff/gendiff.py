import argparse
from gendiff.parser import parser
from gendiff.command import create_attribut, added, deleted, changed, show_value
from formater.stylish import stylish
from formater.plain import plain
from formater.json import json


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )

    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')

    args = parser.parse_args()

    print(generate_diff(args.first_file, args.second_file, args.format))


def replace_bool_or_None_to_str(value) -> str:
    if value is True:
        value = 'true'
    elif value is False:
        value = 'false'
    elif value is None:
        value = 'null'
    return value


def add_atribut(data):
    """
    Appends dictionary elements with an attribute.
    If the value is a dictionary, execute recursively.
    """
    for key, value in data.items():
        if isinstance(value, dict):
            add_atribut(value)
            create_attribut(data, key, value)
        else:
            create_attribut(data, key, replace_bool_or_None_to_str(value))


def compar_values(key, data, attributes1, attributes2):
    """
    Changes an attribute depending on the result of the comparison
    """
    old_value, new_value = show_value(attributes1), show_value(attributes2)
    if new_value is None:
        deleted(data, key, attributes1)
    elif old_value is None:
        added(data, key, attributes2)
    elif isinstance(old_value, dict) and isinstance(new_value, dict):
        create_attribut(data, key, differ(old_value, new_value))
    elif attributes1 != attributes2:
        changed(data, key, attributes1, attributes2)
    else:
        create_attribut(data, key, old_value)


def differ(data1: dict, data2: dict) -> dict:
    """
    Returns a dictionary containing the result of comparing the values
    of two dictionaries. For each key, the value will be a list,
    the first element of which describes the change status (' ' - no change,
    '-' - key deleted, '+' - key added, '*' - key value changed).
    Can be run recursively from a child function.
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
        compar_values(key, result, attributes1, attributes2)
    return result


def generate_diff(file1, file2, formater='stylish'):
    data1 = parser(file1)
    add_atribut(data1)

    data2 = parser(file2)
    add_atribut(data2)

    result = differ(data1, data2)
    if formater == 'stylish':
        result = stylish(result)
    elif formater == 'plain':
        result = plain(result)
    elif formater == 'json':
        result = json(result)
    return result


if __name__ == '__main__':
    main()
