import pytest
from gendiff.command import create_attribut, added, deleted, changed, \
    show_value, show_new_value, show_status


@pytest.fixture
def data():
    return {'key': 'lock'}


def test_create_attribut(data):
    create_attribut(data, 'key', 'value')
    assert data == {'key': [' ', 'value']}

    create_attribut(data, 'key2', 'value2')
    assert data['key2'] == [' ', 'value2']


@pytest.fixture
def attributed_data():
    return {}


def test_added(attributed_data):
    added(attributed_data, 'key', [' ', 'value'])
    assert attributed_data == {'key': ['+', 'value']}


def test_deleted(attributed_data):
    deleted(attributed_data, 'key', [' ', 'value'])
    assert attributed_data == {'key': ['-', 'value']}


def test_changed(attributed_data):
    changed(attributed_data, 'key', [' ', 'value'], [' ', 'value2'])
    assert attributed_data == {'key': ['*', 'value', 'value2']}


changed_data = {'key': ['*', 'value', 'value2']}


def test_show_status():
    assert show_status(changed_data['key']) == '*'


def test_show_value():
    assert show_value(changed_data['key']) == 'value'


def test_show_new_value():
    assert show_new_value(changed_data['key']) == 'value2'
