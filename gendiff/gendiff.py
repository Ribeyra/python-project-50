from formater.json import json
from formater.plain import plain
from formater.stylish import stylish
from gendiff.parser import parser
from gendiff.collect_diff import collect_diff


def generate_diff(file1, file2, formater='stylish'):
    if formater not in (None, 'stylish', 'plain', 'json'):
        return f'Unknown format of output: "{formater}"'

    try:
        data1 = parser(file1)
        data2 = parser(file2)
    except Exception as e:
        return e

    raw_diff = collect_diff(data1, data2)

    if formater == 'plain':
        return plain(raw_diff)
    elif formater == 'json':
        return json(raw_diff)
    return stylish(raw_diff)
