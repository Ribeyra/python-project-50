from formater.plain import add_quotes, complex_value, assemble_string, plain
from gendiff.parser import parser


def test_add_quotes():
    assert add_quotes(True) == 'true'
    assert add_quotes(False) == 'false'
    assert add_quotes(None) == 'null'
    assert add_quotes('value') == "'value'"
    assert add_quotes(12) == 12


def test_complex_value():
    assert complex_value({}) == '[complex value]'
    assert complex_value(True) == 'true'
    assert complex_value('value') == "'value'"
    assert complex_value(12) == 12


def test_assemble_string():
    text1 = "Property 'path.to.value' was added with value: true"
    node1 = {'type': 'added', 'value': True}
    assert assemble_string('path.to.value.', node1) == text1
    text2 = "Property 'path.to.value' was removed"
    node2 = {'type': 'deleted', 'value': True}
    assert assemble_string('path.to.value.', node2) == text2
    text3 = "Property 'path.to.value' was updated. From '' to ' '"
    node3 = {'type': 'changed', 'value': '', 'new_value': ' '}
    assert assemble_string('path.to.value.', node3) == text3
    text4 = "Property 'path.to.value' was added with value: [complex value]"
    node4 = {'type': 'added', 'value': {}}
    assert assemble_string('path.to.value.', node4) == text4


def test_plain():
    raw_diff = parser('tests/fixtures/raw_diff.yaml')

    with open('tests/fixtures/res_plain_out.txt') as file:
        exp_res = file.read()

    assert plain(raw_diff) == exp_res
