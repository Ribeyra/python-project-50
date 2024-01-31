from formater.plain import add_quotes, complex_value, assemble_string, plain
from gendiff.parser import parser


def test_add_quotes():
    assert add_quotes('true') == 'true'
    assert add_quotes('false') == 'false'
    assert add_quotes('null') == 'null'
    assert add_quotes('value') == "'value'"
    assert add_quotes(12) == 12


def test_complex_value():
    assert complex_value({}) == '[complex value]'
    assert complex_value('true') == 'true'
    assert complex_value('value') == "'value'"
    assert complex_value(12) == 12


def test_assemble_string():
    text1 = "Property 'path.to.value' was added with value: true"
    assert assemble_string('path.to.value.', ['+', 'true']) == text1
    text2 = "Property 'path.to.value' was removed"
    assert assemble_string('path.to.value.', ['-', 'true']) == text2
    text3 = "Property 'path.to.value' was updated. From '' to ' '"
    assert assemble_string('path.to.value.', ['*', '', ' ']) == text3
    text4 = "Property 'path.to.value' was added with value: [complex value]"
    assert assemble_string('path.to.value.', ['+', {}]) == text4


with open('tests/fixtures/res_plain_out.txt') as file:
    exp_res = file.read()


def test_plain():
    raw_diff = parser('tests/fixtures/raw_diff.yaml')
    assert plain(raw_diff) == exp_res
