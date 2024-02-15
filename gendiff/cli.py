import argparse


def cli_parser():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference. \
        Files for comparison must be in yaml (yml) or json format.'
    )

    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output: \
        stylish(default), plain or json')

    args = parser.parse_args()

    return args.first_file, args.second_file, args.format
