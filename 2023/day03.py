from collections import defaultdict
from dataclasses import dataclass, field
import fileinput
import operator
from pprint import pprint
import re


@dataclass
class Symbol:
    value: str
    row: int
    col: int
    numbers: set = field(default_factory=set)

    def __hash__(self):
        return (self.value, self.row, self.col).__hash__()


@dataclass
class Number:
    value: int
    row: int
    col: tuple[int, int]
    symbols: set = field(default_factory=set)

    def __hash__(self):
        return (self.value, self.row, self.col).__hash__()


def parse_line(regex, row, line):
    n = []
    s = []
    for m in re.finditer(regex, line):
        try:
            n.append(Number(value=int(m.group(1)), row=row, col=(m.start(1), m.end(1))))
        except ValueError:
            s.append(Symbol(value=m.group(1), row=row, col=(m.start(1))))
    return n, s


def surrounding_indicies(row, cols):
    v = []
    for r in range(row - 1, row + 2):
        for c in range(cols[0] - 1, cols[1] + 2):
            v.append((r, c))
    return v


def find_symbols(number, symbol_grid):
    symbols = set()
    for row, col in surrounding_indicies(number.row, number.col):
        if symbol_grid[row][col]:
            symbols.add(symbol_grid[row][col])
    return symbols


def find_numbers(symbol, number_grid):
    numbers = set()
    for row, col in surrounding_indicies(symbol.row, [symbol.col, symbol.col]):
        if number_grid[row][col]:
            numbers.add(number_grid[row][col])
    return numbers


def parse_input(lines):
    symbol_grid = defaultdict(lambda: defaultdict(lambda: None))
    symbols = set()
    number_grid = defaultdict(lambda: defaultdict(lambda: None))
    numbers = set()

    for y, line in enumerate(lines):
        line = line.strip()
        line_numbers, line_symbols = parse_line(r"([0-9]+|[^.])", y, line)

        for number in line_numbers:
            numbers.add(number)
            for column in range(*number.col):
                number_grid[number.row][column] = number

        for symbol in line_symbols:
            symbols.add(symbol)
            symbol_grid[symbol.row][symbol.col] = symbol

    return symbols, symbol_grid, numbers, number_grid


def one(input):
    total = 0
    _, symbol_grid, numbers, _ = parse_input(list(fileinput.input(input)))

    for number in numbers:
        number.symbols = find_symbols(number, symbol_grid)
        if len(number.symbols) > 0:
            total += number.value
    pprint(total)


def two(input):
    total = 0
    symbols, _, numbers, number_grid = parse_input(list(fileinput.input(input)))

    for symbol in symbols:
        if symbol.value == "*":
            symbol.numbers = find_numbers(symbol, number_grid)
            if len(symbol.numbers) == 2:
                total += operator.mul(*(n.value for n in symbol.numbers))
    print(total)

one("./2023/day03.txt")
two("./2023/day03.txt")
