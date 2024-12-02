from collections import defaultdict
from dataclasses import dataclass
import doctest
from enum import Enum
import fileinput
from itertools import chain, combinations
from pathlib import Path
from typing import Iterable
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, GridNode
from pathfinding.finder.a_star import AStarFinder


def write_matrix(matrix: Iterable[Iterable], output: Path):
    output.write_text(Grid(matrix=matrix).grid_str())

Matrix = list[list[str]]
GROUND = "."
START = "S"
ROCK = "#"


Direction = Enum("Direction", ["N", "E", "S", "W"])


def opposing(direction: Direction):
    if direction is Direction.N:
        return Direction.S
    if direction is Direction.E:
        return Direction.W
    if direction is Direction.S:
        return Direction.N
    if direction is Direction.W:
        return Direction.E


@dataclass
class Position:
    x: int
    y: int

    def __eq__(self, __value: object) -> bool:
        return self.__hash__() == __value.__hash__()

    def __hash__(self) -> int:
        product = (self.x + 1) * (self.y + 1)
        return product if self.y > self.x else -product

    def neighbour(self, direction: Direction):
        if direction is Direction.N:
            return Position(self.x, self.y - 1)
        if direction is Direction.S:
            return Position(self.x, self.y + 1)
        if direction is Direction.E:
            return Position(self.x + 1, self.y)
        if direction is Direction.W:
            return Position(self.x - 1, self.y)
    
    def get_from(self, matrix: Matrix):
        try:
            return matrix[self.y][self.x]
        except IndexError:
            return None

def parse_input(input):
    matrix = []
    for y, line in enumerate(fileinput.input(input)):
        matrix.append([])
        for x, char in enumerate(line.strip()):
            matrix[y].append(char)
            if char == START:
                start = Position(x, y)
    return start, matrix

def navigate(positions: set[Position], matrix: Matrix) -> set[Position]:
    output = set()
    for position in positions:
        for direction in Direction:
            neighbour = position.neighbour(direction)
            cell = neighbour.get_from(matrix)
            if cell and cell != ROCK:
                output.add(neighbour)
    return output

def one(input):
    start, matrix = parse_input(input)
    positions = set([start])

    for _ in range(64):
        positions = navigate(positions, matrix)

    print(len(positions))


def blank_matrix(x, y, blank=1):
    return [[blank] * x for _ in range(y)]


def main():
    one("./2023/day21.txt")
    # two("./2023/day10.txt")

    # width= 5
    # height=5
    # matrix = [[1] * width for _ in range(height)]
    # matrix[4][0] = 0
    # write_matrix(matrix, Path("./2023/day10output.txt"))


if __name__ == "__main__":
    doctest.testmod()
    main()
