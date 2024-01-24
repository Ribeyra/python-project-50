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


def generate_diff(first_file, second_file):
    file1 = parser(first_file)
    file2 = parser(second_file)

    lines = []
    for el in sorted(set(file1) | set(file2)):
        if el in file1 and el in file2:
            value1 = replace_bool_to_str(file1[el])
            value2 = replace_bool_to_str(file2[el])
            if value1 != value2:
                lines.append(f'  - {el}: {value1}\n'
                             f'  + {el}: {value2}')
            else:
                lines.append(f'    {el}: {value1}')
        elif el in file1:
            value1 = replace_bool_to_str(file1[el])
            lines.append(f'  - {el}: {value1}')
        elif el in file2:
            value2 = replace_bool_to_str(file2[el])
            lines.append(f'  + {el}: {value2}')

    result = '{\n' + '\n'.join(lines) + '\n}'
    return result


if __name__ == '__main__':
    main()
