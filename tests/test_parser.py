from gendiff.parser import get_raw_data, parser, project_parser


def test_parser():  # noqa: C901
    expected_result = {
        'uses': 'actions/setup-python@v3',
        'name': 'Lint with flake8',
        'run':
        'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
    }
    raw_data = get_raw_data('tests/fixtures/file1.yaml')
    assert parser(raw_data) == expected_result

    path_1 = 'tests/fixtures/res_json_out.txt'
    error_1 = f"Unsupported file type: '{path_1}'"
    try:
        parser(path_1)
    except Exception as e:
        assert str(e) == error_1

    path_2 = 'tests/fixtures/res_plain_out.yaml'
    error_2 = (
        f"Error in the syntax of the file: '{path_2}'. The file may be "
        f"corrupted or contain syntax errors in YAML or JSON format."
    )
    try:
        parser(path_2)
    except Exception as e:
        assert str(e) == error_2

    path_3 = 'tests/fixtures/res_plain_out.yml'
    error_3 = (f"File not found: '{path_3}'")
    try:
        parser(path_3)
    except Exception as e:
        assert str(e) == error_3


def test_project_parser():
    json = {
        'host': 'hexlet.io',
        'timeout': 50,
        'proxy': '123.234.53.22',
        'follow': False
    }
    assert project_parser('tests/fixtures/file1.json') == json

    yaml = {
        'uses': 'actions/setup-python@v3',
        'name': 'Lint with flake8',
        'run':
        'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
    }
    assert project_parser('tests/fixtures/file1.yaml') == yaml

    try:
        project_parser('tests/fixtures/res_json_out.txt')
    except Exception as e:
        assert str(e) == "Unsupported file type"
