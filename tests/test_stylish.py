from formater.stylish import replace_bool_or_None_to_str, assemble_string, \
    stylish
from gendiff.parser import parser


def test_replace_bool_or_None_to_str():
    assert replace_bool_or_None_to_str(True) == 'true'
    assert replace_bool_or_None_to_str(False) == 'false'
    assert replace_bool_or_None_to_str(None) == 'null'
    assert replace_bool_or_None_to_str('some text') == 'some text'
    assert replace_bool_or_None_to_str(12) == 12


def test_assemble_string():
    deps = 1
    indentations = {
        'unchg': (' ' * 4) * deps + '    ',
        'del': (' ' * 4) * deps + '  - ',
        'add': (' ' * 4) * deps + '  + '
    }
    key = 'key'

    node = {'type': 'unchg', 'value': 'value'}
    res = "        key: value\n"
    assert assemble_string(indentations, key, node, deps) == res

    node = {'type': 'del', 'value': 'value'}
    res = "      - key: value\n"
    assert assemble_string(indentations, key, node, deps) == res

    node = {'type': 'add', 'value': 'value'}
    res = "      + key: value\n"
    assert assemble_string(indentations, key, node, deps) == res

    node = {'type': 'mod', 'value': 'old_value', 'new_value': 'new_value'}
    res = "      - key: old_value\n      + key: new_value\n"
    assert assemble_string(indentations, key, node, deps) == res


def test_stylish():
    raw_diff = parser('tests/fixtures/raw_diff.json')

    with open('tests/fixtures/res_nested_json.txt') as file:
        exp_res = file.read()

    assert stylish(raw_diff) == exp_res
