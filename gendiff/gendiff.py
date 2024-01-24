import argparse
from gendiff.parser import parser


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')

    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))


def replace_bool_to_str(value: bool) -> str:
    if value is True:
        return 'true'
    elif value is False:
        return 'false'
    return value


def assemble_string(el, value1, value2):
    if value2 is None:
        return f'  - {el}: {value1}'
    elif value1 is None:
        return f'  + {el}: {value2}'
    elif value1 != value2:
        return f'  - {el}: {value1}\n  + {el}: {value2}'
    else:
        return f'    {el}: {value1}'


def generate_diff(first_file, second_file):
    file1 = parser(first_file)
    file2 = parser(second_file)

    lines = []
    for el in sorted(set(file1) | set(file2)):
        value1 = replace_bool_to_str(file1.get(el))
        value2 = replace_bool_to_str(file2.get(el))
        lines.append(assemble_string(el, value1, value2))

    result = '{\n' + '\n'.join(lines) + '\n}'
    return result


if __name__ == '__main__':
    main()
