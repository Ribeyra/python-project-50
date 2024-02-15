import pytest
from gendiff.command import create_node, set_added, set_deleted, \
    set_changed, get_value, get_new_value, get_status


@pytest.fixture
def data():
    return {'key': 'lock'}


def test_create_attribut(data):
    create_node(data, 'key', 'value')
    assert data == {'key': {'type': 'unchanged', 'value': 'value'}}

    create_node(data, 'key2', 'value2')
    assert data['key2'] == {'type': 'unchanged', 'value': 'value2'}


@pytest.fixture
def attributed_data():
    return {}


def test_set_added(attributed_data):
    create_node(attributed_data, 'key', 'value')
    set_added(attributed_data, 'key')
    assert attributed_data == {'key': {'type': 'added', 'value': 'value'}}


def test_set_deleted(attributed_data):
    create_node(attributed_data, 'key', 'value')
    set_deleted(attributed_data, 'key')
    assert attributed_data == {'key': {'type': 'deleted', 'value': 'value'}}


def test_set_changed(attributed_data):
    create_node(attributed_data, 'key', 'value')
    set_changed(attributed_data, 'key', 'value2')
    assert attributed_data == {'key': {
        'type': 'changed',
        'value': 'value',
        'new_value': 'value2'
    }}


@pytest.fixture
def changed_data():
    return {'key': {
        'type': 'changed',
        'value': 'value',
        'new_value': 'value2'
    }}


def test_show_status(changed_data):
    assert get_status('value') == 'unchanged'
    assert get_status(changed_data['key']) == 'changed'


def test_show_value(changed_data):
    assert get_value('value') == 'value'
    assert get_value(changed_data['key']) == 'value'


def test_show_new_value(changed_data):
    assert get_new_value('value') == 'value'
    assert get_new_value(changed_data['key']) == 'value2'
