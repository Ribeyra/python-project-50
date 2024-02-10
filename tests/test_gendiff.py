from gendiff.gendiff import collect_diff, generate_diff


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
        'key1': {'type': 'mod', 'value': 'value1', 'new_value': 'true'},
        'key2': {'type': 'unchg', 'value': {
            'inner_key1': {
                'type': 'mod',
                'value': 'inner_value1',
                'new_value': 'some_value1'
            },
            'inner_key2': {'type': 'del', 'value': 'inner_value2'},
            'inner_key3': {'type': 'add', 'value': 'inner_value2'}
        }},
        'key3': {'type': 'unchg', 'value': 'value3'}
    }
    assert collect_diff(data1, data2) == exp_res


def test_generate_diff_for_flat_structures():
    file1_json = 'tests/fixtures/file1.json'
    file2_json = 'tests/fixtures/file2.json'
    expected_result_to_flat_json = 'tests/fixtures/res_flat_json.txt'

    with open(expected_result_to_flat_json, 'r') as file:
        exp_flat = file.read()

    assert generate_diff(file1_json, file2_json) == exp_flat

    file1_yaml = 'tests/fixtures/file1.yaml'
    file2_yaml = 'tests/fixtures/file2.yml'
    expected_result_to_flat_yaml = 'tests/fixtures/res_flat_yaml.txt'

    with open(expected_result_to_flat_yaml, 'r') as file:
        exp_flat = file.read()

    assert generate_diff(file1_yaml, file2_yaml) == exp_flat


def test_generate_diff_for_nested_structures():

    file3_json = 'tests/fixtures/file3.json'
    file4_json = 'tests/fixtures/file4.json'
    expected_result_to_nested_json = 'tests/fixtures/res_nested_json.txt'

    with open(expected_result_to_nested_json, 'r') as file:
        exp_nested = file.read()

    assert generate_diff(file3_json, file4_json) == exp_nested

    file3_yaml = 'tests/fixtures/file3.yaml'
    file4_yaml = 'tests/fixtures/file4.yml'
    expected_result_to_nested_yaml = 'tests/fixtures/res_nested_yaml.txt'

    with open(expected_result_to_nested_yaml) as file:
        exp_nested = file.read()

    assert generate_diff(file3_yaml, file4_yaml) == exp_nested

    with open('tests/fixtures/res_plain_out.txt') as file:
        exp_nested = file.read()

    assert generate_diff(file3_json, file4_json, 'plain') == exp_nested

    with open('tests/fixtures/res_json_out.txt') as file:
        exp_nested = file.read()

    assert generate_diff(file3_json, file4_json, 'json') == exp_nested
