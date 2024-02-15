from gendiff.collect_diff import collect_diff


def test_differ():
    data1 = {
        'key1': 'value1',
        'key2': {
            'inner_key1': 'inner_value1',
            'inner_key2': 'inner_value2'
        },
        'key3': 'value3'
    }
    data2 = {
        'key1': 'true',
        'key2': {
            'inner_key1': 'some_value1',
            'inner_key3': 'inner_value2'
        },
        'key3': 'value3'
    }
    exp_res = {
        'key1': {'type': 'changed', 'value': 'value1', 'new_value': 'true'},
        'key2': {'type': 'unchanged', 'value': {
            'inner_key1': {
                'type': 'changed',
                'value': 'inner_value1',
                'new_value': 'some_value1'
            },
            'inner_key2': {'type': 'deleted', 'value': 'inner_value2'},
            'inner_key3': {'type': 'added', 'value': 'inner_value2'}
        }},
        'key3': {'type': 'unchanged', 'value': 'value3'}
    }
    assert collect_diff(data1, data2) == exp_res
