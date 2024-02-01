from formater.json import json
from gendiff.parser import parser

with open('tests/fixtures/res_json_out.txt') as file:
    exp_res = file.read()


def test_json():
    raw_diff = parser('tests/fixtures/raw_diff.yaml')
    assert json(raw_diff) == exp_res
