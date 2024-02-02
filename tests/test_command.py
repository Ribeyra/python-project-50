import pytest
from gendiff.command import create_attribut, set_added, set_deleted, \
    set_changed, get_value, get_new_value, get_status


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


def test_set_added(attributed_data):
    create_attribut(attributed_data, 'key', 'value')
    set_added(attributed_data, 'key')
    assert attributed_data == {'key': ['+', 'value']}


def test_set_deleted(attributed_data):
    create_attribut(attributed_data, 'key', 'value')
    set_deleted(attributed_data, 'key')
    assert attributed_data == {'key': ['-', 'value']}


def test_set_changed(attributed_data):
    create_attribut(attributed_data, 'key', 'value')
    set_changed(attributed_data, 'key', 'value2')
    assert attributed_data == {'key': ['*', 'value', 'value2']}


changed_data = {'key': ['*', 'value', 'value2']}


def test_show_status():
    assert get_status(changed_data['key']) == '*'


def test_show_value():
    assert get_value(changed_data['key']) == 'value'


def test_show_new_value():
    assert get_new_value(changed_data['key']) == 'value2'
