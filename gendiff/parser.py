import yaml
import json


def parser(path):
    try:
        if path.endswith(('.json', '.yaml', '.yml')):
            with open(path) as file:
                data = yaml.load(file, Loader=yaml.Loader)
        else:
            raise Exception(f"Unsupported file type: '{path}'")
    except yaml.scanner.ScannerError:
        raise Exception(
            f"Error in the syntax of the file: '{path}'. The file may be "
            f"corrupted or contain syntax errors in YAML or JSON format."
        )
    except FileNotFoundError:
        raise Exception(f"File not found: '{path}'")
    return data


def project_parser(path):
    """
    This function is not used in the application.
    Demonstrates the solution as part of the fifth step of the project
    """
    if path.endswith('.json'):
        with open(path) as file:
            data = json.load(file)
    elif path.endswith(('.yaml', '.yml')):
        with open(path) as file:
            data = yaml.load(file, Loader=yaml.Loader)
    else:
        raise Exception("Unsupported file type")
    return data
