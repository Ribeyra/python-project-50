from gendiff.gendiff import generate_diff

file1 = 'tests/fixtures/file1.json'
file2 = 'tests/fixtures/file2.json'

expected_result = 'tests/fixtures/res.txt'

with open('tests/fixtures/res.txt', 'r') as file:
    exp_res = file.read()


def test_generate_diff():
    assert generate_diff(file1, file2) == exp_res
