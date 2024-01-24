import yaml


def parser(path):
    with open(path) as file:
        data = yaml.load(file, Loader=yaml.Loader)

    return data
