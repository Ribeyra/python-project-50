from gendiff.command import show_status, show_value, show_new_value


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
        if isinstance(new_value, dict):
            new_value = stylish(new_value, deps + 1)
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
