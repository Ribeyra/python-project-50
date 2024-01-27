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


def replace_bool_or_None_to_str(value) -> str:
    if value is True:
        return 'true'
    elif value is False:
        return 'false'
    return 'null'


def add_parameter(data):
    """
    Changes the value to a tuple (' ' , value).
    For dictionaries it runs recursively.
    The first value of the tuple is a parameter describing the status
    of the value change
    """
    if isinstance(data, bool) or data is None:
        return (' ', replace_bool_or_None_to_str(data))
    if isinstance(data, dict):
        res = {}
        for key, value in data.items():
            if isinstance(value, dict):
                res[key] = add_parameter(value)
            else:
                res[key] = (' ', value)
        return (' ', res)
    return (' ', data)


def compar_values(value1, value2, obj):
    """
    Changes the value of a parameter depending on the result
    of comparing two values
    """
    if isinstance(value1, dict) and isinstance(value2, dict):
        result = (' ', differ(value1, value2))
    elif value1 == value2:
        result = (' ', add_parameter(value1)[1])
    elif value2 == obj:
        result = ('-', add_parameter(value1)[1])
    elif value1 == obj:
        result = ('+', add_parameter(value2)[1])
    elif not (isinstance(value1, dict) and isinstance(value2, dict)):
        result = ('*', add_parameter(value1)[1], add_parameter(value2)[1])
    return result


def differ(data1: dict, data2: dict) -> dict:
    """
    Returns a dictionary containing the result of comparing the values
    of two files. For each key, the value will be a tuple, the first
    element of which describes the change status (' ' - unchanged,
    '-' - key deleted, '+' - key added, '*' - key value changed).
    Can be run recursively from a child function.
    Example output:
    >>> pprint.pprint(differ(data1, data2))
    {'common': (' ',
            {'follow': ('+', 'false'),
             'setting1': (' ', 'Value 1'),
             'setting2': ('-', 200),
             'setting3': ('*', 'true', 'null'),
             'setting4': ('+', 'blah blah'),
             'setting5': ('+', {'key5': (' ', 'value5')}),
             'setting6': (' ',
                          {'doge': (' ', {'wow': ('*', '', 'so much')}),
                           'key': (' ', 'value'),
                           'ops': ('+', 'vops')})}),
    ...
    """
    obj = object()
    res = {}
    for el in sorted(set(data1) | set(data2)):
        value1, value2 = data1.get(el, obj), data2.get(el, obj)
        res[el] = compar_values(value1, value2, obj)
    return res


def assemble_string(indentations: dict, key: str, value: tuple, deps) -> str:
    """
    Assemble strings from key and value indentation.
    Is a child function of stylish
    """
    changed, value1, *_ = value
    if isinstance(value1, dict):
        value1 = stylish(value1, deps + 1)
    if changed == '*':
        value2 = value[2]
        return (f'{indentations["-"]}{key}: {value1}\n'
                f'{indentations["+"]}{key}: {value2}\n')
    elif changed == '-':
        return f'{indentations["-"]}{key}: {value1}\n'
    elif changed == '+':
        return f'{indentations["+"]}{key}: {value1}\n'
    return f'{indentations[" "]}{key}: {value1}\n'


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
    data2 = parser(file2)

    result = differ(data1, data2)
    return formater(result)


if __name__ == '__main__':
    main()
