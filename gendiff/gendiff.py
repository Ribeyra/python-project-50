from formater.json import json
from formater.plain import plain
from formater.stylish import stylish
from gendiff.parser import get_raw_data, parser
from gendiff.collect_diff import collect_diff


def generate_diff(file1, file2, formater='stylish'):
    if formater not in (None, 'stylish', 'plain', 'json'):
        return f'Unknown format of output: "{formater}"'

    try:
        raw_data1 = get_raw_data(file1)
        raw_data2 = get_raw_data(file2)
        data1 = parser(raw_data1)
        data2 = parser(raw_data2)
    except Exception as e:
        return e

    raw_diff = collect_diff(data1, data2)

    if formater == 'plain':
        return plain(raw_diff)
    elif formater == 'json':
        return json(raw_diff)
    return stylish(raw_diff)
