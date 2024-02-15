from gendiff.command import get_node, get_status, get_value, get_new_value


def add_quotes(value):
    if value is True:
        value = 'true'
    elif value is False:
        value = 'false'
    elif value is None:
        value = 'null'
    elif isinstance(value, str):
        value = f"'{value}'"
    return value


def complex_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    return add_quotes(value)


def assemble_string(path, node):
    status = get_status(node)
    value = complex_value(get_value(node))
    if status == 'added':
        text = f'added with value: {value}'
    elif status == 'deleted':
        text = 'removed'
    elif status == 'changed':
        new_value = complex_value(get_new_value(node))
        text = f'updated. From {value} to {new_value}'
    result = f"Property '{path[:-1]}' was {text}"
    return result


def collect_strings_list(data, path=''):
    result = []
    for key in sorted(data.keys()):
        node = get_node(data, key)
        status = get_status(node)
        value = get_value(node)
        if isinstance(value, dict) and status == 'unchanged':
            result.extend(collect_strings_list(value, f'{path}{key}.'))
        elif status != 'unchanged':
            result.append(assemble_string(f'{path}{key}.', node))
    return result


def plain(data):
    result = collect_strings_list(data)
    return '\n'.join(result)
