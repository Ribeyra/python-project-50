import argparse
import json


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
    file1 = json.load(open(first_file), parse_int=str)
    file2 = json.load(open(second_file), parse_int=str)

    lines = []
    for el in sorted(set(file1) | set(file2)):
        if el in file1 and el in file2:
            if file1[el] != file2[el]:
                lines.append(f'  - {el}: {replace_bool_to_str(file1[el])}\n'
                             f'  + {el}: {replace_bool_to_str(file2[el])}')
            else:
                lines.append(f'    {el}: {replace_bool_to_str(file1[el])}')
        elif el in file1:
            lines.append(f'  - {el}: {replace_bool_to_str(file1[el])}')
        elif el in file2:
            lines.append(f'  + {el}: {replace_bool_to_str(file2[el])}')

    result = '{\n' + '\n'.join(lines) + '\n}'
    return result


if __name__ == '__main__':
    main()
