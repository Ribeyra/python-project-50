from formater.stylish import replace_bool_or_None_to_str, assemble_string, \
    stylish
from gendiff.parser import get_raw_data, parser


def test_replace_bool_or_None_to_str():
    assert replace_bool_or_None_to_str(True) == 'true'
    assert replace_bool_or_None_to_str(False) == 'false'
    assert replace_bool_or_None_to_str(None) == 'null'
    assert replace_bool_or_None_to_str('some text') == 'some text'
    assert replace_bool_or_None_to_str(12) == 12


def test_assemble_string():
    deps = 1
    indentations = {
        'unchanged': (' ' * 4) * deps + '    ',
        'deleted': (' ' * 4) * deps + '  - ',
        'added': (' ' * 4) * deps + '  + '
    }
    key = 'key'

    node = {'type': 'unchanged', 'value': 'value'}
    res = "        key: value\n"
    assert assemble_string(indentations, key, node, deps) == res

    node = {'type': 'deleted', 'value': 'value'}
    res = "      - key: value\n"
    assert assemble_string(indentations, key, node, deps) == res

    node = {'type': 'added', 'value': 'value'}
    res = "      + key: value\n"
    assert assemble_string(indentations, key, node, deps) == res

    node = {'type': 'changed', 'value': 'old_value', 'new_value': 'new_value'}
    res = "      - key: old_value\n      + key: new_value\n"
    assert assemble_string(indentations, key, node, deps) == res


def test_stylish():
    raw_data = get_raw_data('tests/fixtures/raw_diff.json')
    raw_diff = parser(raw_data)

    with open('tests/fixtures/res_nested_json.txt') as file:
        exp_res = file.read()

    assert stylish(raw_diff) == exp_res
