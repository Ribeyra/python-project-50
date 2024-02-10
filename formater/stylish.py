from gendiff.command import get_status, get_value, get_new_value


def replace_bool_or_None_to_str(value):
    if value is True:
        value = 'true'
    elif value is False:
        value = 'false'
    elif value is None:
        value = 'null'
    return value


def assemble_string(indentations: dict, key: str, node: list, deps: int):
    """
    Assemble strings from key and value indentation.
    Is a child function of stylish
    """
    status = get_status(node)
    value = get_value(node)
    value = replace_bool_or_None_to_str(value)
    if isinstance(value, dict):
        value = stylish(value, deps + 1)
    if status == 'mod':
        new_value = get_new_value(node)
        new_value = replace_bool_or_None_to_str(new_value)
        if isinstance(new_value, dict):
            new_value = stylish(new_value, deps + 1)
        return (f'{indentations["del"]}{key}: {value}\n'
                f'{indentations["add"]}{key}: {new_value}\n')
    return f'{indentations[status]}{key}: {value}\n'


def stylish(data, deps=0) -> str:
    """
    Returns a string formatting the raw diff.
    Can be called recursively from a child function.
    """
    indentations = {
        'unchg': (' ' * 4) * deps + '    ',
        'del': (' ' * 4) * deps + '  - ',
        'add': (' ' * 4) * deps + '  + '
    }
    lines = []
    for key in sorted(data.keys()):
        value = data[key]
        lines.append(assemble_string(indentations, key, value, deps))
    result = ''.join(['{\n'] + lines + [f'{indentations["unchg"][:-4]}' + '}'])
    return result
