from gendiff.command import show_status, show_value, show_new_value


def add_quotes(text):
    if text in ('true', 'false', 'null'):
        return text
    return f"'{text}'"


def complex_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    return add_quotes(value)


def assemble_string(path, attributes):
    status = show_status(attributes)
    value = complex_value(show_value(attributes))
    if status == '+':
        text = f'added with value: {value}'
    elif status == '-':
        text = 'removed'
    elif status == '*':
        new_value = complex_value(show_new_value(attributes))
        text = f'updated. From {value} to {new_value}'
    result = f"Property '{path[:-1]}' was {text}"
    return result


def plained(data, path=''):
    result = []
    for key, attributes in data.items():
        status = show_status(attributes)
        value = show_value(attributes)
        if isinstance(value, dict) and status == ' ':
            result.extend(plained(value, f'{path}{key}.'))
        elif status != ' ':
            result.append(assemble_string(f'{path}{key}.', attributes))
    return result


def plain(data):
    result = plained(data)
    return '\n'.join(result)
