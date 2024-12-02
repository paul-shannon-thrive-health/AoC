from collections import defaultdict
from dataclasses import dataclass
import doctest
import fileinput
from itertools import chain, combinations
from pathlib import Path
from typing import Iterable
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, GridNode
from pathfinding.finder.a_star import AStarFinder


def write_matrix(matrix: Iterable[Iterable], output: Path):
    output.write_text(Grid(matrix=matrix).grid_str())


@dataclass
class Position:
    x: int
    y: int

    def __eq__(self, __value: object) -> bool:
        return self.__hash__() == __value.__hash__()

    def __hash__(self) -> int:
        product = (self.x + 1) * (self.y + 1)
        return product if self.y > self.x else -product


char_map = {".": 1, "#": 0}


def parse_input(input):
    lines = list(fileinput.input(input))
    height = len(lines)
    width = len(lines[0])
    matrix = Matrix(None, width, height)
    for x, line in enumerate(lines):
        for y, char in enumerate(line.strip()):
            matrix.set(Position(x, y), 0 if char == "#" else 1)
    return matrix


def one(input):
    result = 0
    matrix = parse_input(input).expand()
    galaxies = [position for position, item in matrix.items() if item == 0]
    for a, b in combinations(galaxies, 2):
        distance_matrix = Matrix(width=matrix.width, height=matrix.height)
        distance_matrix.set(a, 0)
        distance_matrix.set(b, 0)
        distance_matrix.distance(a, b)
        pass



def blank_matrix(x, y, blank=1):
    return [[blank] * x for _ in range(y)]


@dataclass
class Matrix:
    width: int
    height: int
    data: list[list[int]]

    def __init__(self, data=None, width=0, height=0):
        if data:
            self.data = data
            self.height = len(data)
            self.width = len(data[0])
        else:
            self.height = height
            self.width = width
            self.data = [[1] * self.width for _ in range(self.height)]

    def set(self, position, value):
        self.data[position.x][position.y] = value

    def get(self, position):
        return self.data[position.x][position.y]

    def items(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                yield Position(x, y), cell

    def as_string(self):
        return Grid(matrix=self.data).grid_str(empty_chr=".")

    def transpose(self):
        new = Matrix(width=self.height, height=self.width)
        for position, value in self.items():
            new.data[position.x][position.y] = value
        return new

    def expand(self):
        return self.expand_rows().expand_cols()

    def expand_rows(self):
        output = []
        for row in self.data:
            output.append(row)
            if set(row) == {1}:
                output.append(row)
        return Matrix(output)

    def expand_cols(self):
        return self.transpose().expand_rows().transpose()

    def distance(self, a, b):
        grid = Grid(matrix=self.data)
        start = grid.node(a.y, a.x)
        end = grid.node(b.y, b.x)
        path, runs = AStarFinder().find_path(start, end, grid)
        print(Grid(matrix=self.data).grid_str(path=path, start=start, end=end, empty_chr="."))

@dataclass
class Item:
    type: str
    position: Position
    value: int

    def __eq__(self, __value: object) -> bool:
        return self.__hash__() == __value.__hash__()

    def __hash__(self) -> int:
        return self.position.__hash__()


def main():
    one("./2023/day11example.txt")
    # two("./2023/day10.txt")

    # width= 5
    # height=5
    # matrix = [[1] * width for _ in range(height)]
    # matrix[4][0] = 0
    # write_matrix(matrix, Path("./2023/day10output.txt"))


if __name__ == "__main__":
    doctest.testmod()
    main()
