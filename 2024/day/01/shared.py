from pathlib import Path


def data(stem="input.txt"):
    left_column = []
    right_column = []
    input_path = Path(__file__).parent / stem
    with open(input_path) as open_file:
        for line in open_file:
            left, right = line.split()
            left_column.append(int(left))
            right_column.append(int(right))
    return left_column, right_column
