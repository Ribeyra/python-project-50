from gendiff.gendiff import replace_bool_or_None_to_str, add_atribut, \
    compar_values, differ, generate_diff


def test_replace_bool_or_None_to_str():
    assert replace_bool_or_None_to_str(True) == 'true'
    assert replace_bool_or_None_to_str(False) == 'false'
    assert replace_bool_or_None_to_str(None) == 'null'
    assert replace_bool_or_None_to_str('some text') == 'some text'
    assert replace_bool_or_None_to_str(12) == 12


def test_add_atribut():
    data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    exp_res = {
        'key1': [' ', 'value1'],
        'key2': [' ', 'value2'],
        'key3': [' ', 'value3']
    }
    add_atribut(data)
    assert data == exp_res

    data2 = {
        'key1': 'value1',
        'key2': {
            'inner_key1': 'inner_value1',
            'inner_key2': 'inner_value2'
        },
        'key3': 'value3'
    }
    exp_res2 = {
        'key1': [' ', 'value1'],
        'key2': [' ', {
            'inner_key1': [' ', 'inner_value1'],
            'inner_key2': [' ', 'inner_value2']
        }],
        'key3': [' ', 'value3']
    }
    add_atribut(data2)
    assert data2 == exp_res2


def test_differ():
    data1 = {
        'key1': [' ', 'value1'],
        'key2': [' ', {
            'inner_key1': [' ', 'inner_value1'],
            'inner_key2': [' ', 'inner_value2']
        }],
        'key3': [' ', 'value3']
    }
    data2 = {
        'key1': [' ', 'true'],
        'key2': [' ', {
            'inner_key1': [' ', 'some_value1'],
            'inner_key3': [' ', 'inner_value2']
        }],
        'key3': [' ', 'value3']
    }
    exp_res = {
        'key1': ['*', 'value1', 'true'],
        'key2': [' ', {
            'inner_key1': ['*', 'inner_value1', 'some_value1'],
            'inner_key2': ['-', 'inner_value2'],
            'inner_key3': ['+', 'inner_value2']
        }],
        'key3': [' ', 'value3']
    }
    assert differ(data1, data2) == exp_res


def test_compar_values():

    key = 'key'
    data = {}
    attributes1 = [' ', 'old_value']
    attributes2 = [None, None]
    compar_values(key, data, attributes1, attributes2)
    assert data == {'key': ['-', 'old_value']}

    data = {}
    attributes1 = [None, None]
    attributes2 = [' ', 'new_value']
    compar_values(key, data, attributes1, attributes2)
    assert data == {'key': ['+', 'new_value']}

    data = {}
    attributes1 = [' ', 'old_value']
    attributes2 = [' ', 'new_value']
    compar_values(key, data, attributes1, attributes2)
    assert data == {'key': ['*', 'old_value', 'new_value']}

    data = {}
    attributes1 = [' ', 'old_value']
    attributes2 = [' ', 'old_value']
    compar_values(key, data, attributes1, attributes2)
    assert data == {'key': [' ', 'old_value']}


file1_json = 'tests/fixtures/file1.json'
file2_json = 'tests/fixtures/file2.json'

file3_json = 'tests/fixtures/file3.json'
file4_json = 'tests/fixtures/file4.json'

file1_yaml = 'tests/fixtures/file1.yaml'
file2_yaml = 'tests/fixtures/file2.yml'

file3_yaml = 'tests/fixtures/file3.yaml'
file4_yaml = 'tests/fixtures/file4.yml'

expected_result_to_flat_json = 'tests/fixtures/res_flat_json.txt'
expected_result_to_nested_json = 'tests/fixtures/res_nested_json.txt'

expected_result_to_flat_yaml = 'tests/fixtures/res_flat_yaml.txt'
expected_result_to_nested_yaml = 'tests/fixtures/res_nested_yaml.txt'


def test_generate_diff_for_flat_structures():
    with open(expected_result_to_flat_json, 'r') as file:
        exp_flat = file.read()

    assert generate_diff(file1_json, file2_json) == exp_flat

    with open(expected_result_to_flat_yaml, 'r') as file:
        exp_flat = file.read()

    assert generate_diff(file1_yaml, file2_yaml) == exp_flat


def test_generate_diff_for_nested_structures():
    with open(expected_result_to_nested_json, 'r') as file:
        exp_nested = file.read()

    assert generate_diff(file3_json, file4_json) == exp_nested

    with open(expected_result_to_nested_yaml, 'r') as file:
        exp_nested = file.read()

    assert generate_diff(file3_yaml, file4_yaml) == exp_nested

    with open('tests/fixtures/res_plain_out.txt', 'r') as file:
        exp_nested = file.read()

    assert generate_diff(file3_json, file4_json, 'plain') == exp_nested

    # with open('tests/fixtures/res_json_out.txt', 'r') as file:
    #     exp_nested = file.read()

    # assert generate_diff(file3_json, file4_json, 'json') == exp_nested
