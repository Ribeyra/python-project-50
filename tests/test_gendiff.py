from gendiff.gendiff import generate_diff

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
