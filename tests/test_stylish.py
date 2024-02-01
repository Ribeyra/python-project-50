from formater.stylish import assemble_string, stylish
from gendiff.parser import parser


def test_assemble_string():
    deps = 1
    indentations = {
        ' ': (' ' * 4) * deps + '    ',
        '-': (' ' * 4) * deps + '  - ',
        '+': (' ' * 4) * deps + '  + '
    }
    key = 'key'

    attributs = [' ', 'value']
    res = "        key: value\n"
    assert assemble_string(indentations, key, attributs, deps) == res

    attributs = ['-', 'value']
    res = "      - key: value\n"
    assert assemble_string(indentations, key, attributs, deps) == res

    attributs = ['+', 'value']
    res = "      + key: value\n"
    assert assemble_string(indentations, key, attributs, deps) == res

    attributs = ['*', 'old_value', 'new_value']
    res = "      - key: old_value\n      + key: new_value\n"
    assert assemble_string(indentations, key, attributs, deps) == res


with open('tests/fixtures/res_nested_json.txt') as file:
    exp_res = file.read()


def test_stylish():
    raw_diff = parser('tests/fixtures/raw_diff.json')
    assert stylish(raw_diff) == exp_res
