from gendiff.parser import parser

expected_result = {
    'uses': 'actions/setup-python@v3',
    'name': 'Lint with flake8',
    'run': 'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
}


def test_parser():
    assert parser('tests/fixtures/file1.yaml') == expected_result
