import argparse
from gendiff.parser import parser


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')

    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))


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


def assemble_string(indentations: dict, key: str, attributs: list, deps: int):
    """
    Assemble strings from key and value indentation.
    Is a child function of stylish
    """
    status = show_status(attributs)
    value = show_value(attributs)
    if isinstance(value, dict):
        value = stylish(value, deps + 1)
    if status == '*':
        new_value = show_new_value(attributs)
        return (f'{indentations["-"]}{key}: {value}\n'
                f'{indentations["+"]}{key}: {new_value}\n')
    elif status == '-':
        return f'{indentations["-"]}{key}: {value}\n'
    elif status == '+':
        return f'{indentations["+"]}{key}: {value}\n'
    return f'{indentations[" "]}{key}: {value}\n'


def stylish(data, deps=0) -> str:
    """
    Returns a string formatting the raw diff.
    Can be called recursively from a child function.
    """
    indentations = {
        ' ': (' ' * 4) * deps + '    ',
        '-': (' ' * 4) * deps + '  - ',
        '+': (' ' * 4) * deps + '  + '
    }
    lines = []
    for key, value in data.items():
        lines.append(assemble_string(indentations, key, value, deps))
    result = ''.join(['{\n'] + lines + [f'{indentations[" "][:-4]}' + '}'])
    return result


def generate_diff(file1, file2, formater=stylish):
    data1 = parser(file1)
    add_atribut(data1)

    data2 = parser(file2)
    add_atribut(data2)

    result = differ(data1, data2)
    return formater(result)


if __name__ == '__main__':
    main()
