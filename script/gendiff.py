#!/usr/bin/env python3
from gendiff.cli import cli_parser
from gendiff.gendiff import generate_diff


def main():
    path1, path2, formater = cli_parser()
    print(generate_diff(path1, path2, formater))


if __name__ == '__main__':
    main()
