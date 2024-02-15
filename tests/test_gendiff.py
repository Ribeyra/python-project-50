from gendiff.gendiff import generate_diff


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


def test_formater():

    file3_json = 'tests/fixtures/file3.json'
    file4_json = 'tests/fixtures/file4.json'

    exp_error = 'Unknown format of output: "plian"'
    assert generate_diff(file3_json, file4_json, 'plian') == exp_error

    with open('tests/fixtures/res_plain_out.txt') as file:
        exp_nested = file.read()

    assert generate_diff(file3_json, file4_json, 'plain') == exp_nested

    with open('tests/fixtures/res_json_out.txt') as file:
        exp_nested = file.read()

    assert generate_diff(file3_json, file4_json, 'json') == exp_nested


def test_error():
    file3_json = 'tests/fixtures/file3.json'
    path = 'tests/fixtures/res_json_out.txt'
    exp_error = f"Unsupported file type: '{path}'"
    error = generate_diff(file3_json, path)
    assert str(error) == exp_error
