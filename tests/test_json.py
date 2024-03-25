from formater.json import json
from gendiff.parser import get_raw_data, parser


def test_json():
    raw_data = get_raw_data('tests/fixtures/raw_diff.yaml')
    raw_diff = parser(raw_data)

    with open('tests/fixtures/res_json_out.txt') as file:
        exp_res = file.read()

    assert json(raw_diff) == exp_res
