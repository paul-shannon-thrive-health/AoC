from collections import defaultdict
from dataclasses import dataclass, field
import doctest
from enum import Enum
import fileinput
from functools import reduce, total_ordering
from itertools import accumulate, cycle, pairwise, repeat
import operator
from pathlib import Path
from pprint import pprint
import re
import time
from typing import DefaultDict, Iterable, Optional, Union
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid as PathGrid, GridNode
from pathfinding.finder.a_star import AStarFinder

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
class Tile:
    char: str
    x: int
    y: int

    @property
    def pos(self):
        return self.x, self.y

    def __eq__(self, __value: object) -> bool:
        return self.__hash__() == __value.__hash__()

    def __hash__(self) -> int:
        product = (self.x + 1) * (self.y + 1)
        return product if self.y > self.x else -product


@dataclass
class Pipe(Tile):
    connections: dict[Direction, bool] = field(default_factory=dict)

    __eq__ = Tile.__eq__
    __hash__ = Tile.__hash__


@dataclass
class Ground(Tile):
    pass


char_map = {
    "|": (
        Pipe,
        {Direction.N: True, Direction.E: False, Direction.S: True, Direction.W: False},
    ),
    "-": (
        Pipe,
        {Direction.N: False, Direction.E: True, Direction.S: False, Direction.W: True},
    ),
    "L": (
        Pipe,
        {Direction.N: True, Direction.E: True, Direction.S: False, Direction.W: False},
    ),
    "J": (
        Pipe,
        {Direction.N: True, Direction.E: False, Direction.S: False, Direction.W: True},
    ),
    "7": (
        Pipe,
        {Direction.N: False, Direction.E: False, Direction.S: True, Direction.W: True},
    ),
    "F": (
        Pipe,
        {Direction.N: False, Direction.E: True, Direction.S: True, Direction.W: False},
    ),
    ".": (Ground,),
    "S": (
        Pipe,
        {
            Direction.N: False,
            Direction.E: False,
            Direction.S: False,
            Direction.W: False,
        },
    ),
}


@dataclass
class Grid:
    tiles: DefaultDict[int, list] = None
    start: Tile = None

    map = {
        Direction.N: (-1, 0),
        Direction.E: (0, 1),
        Direction.S: (1, 0),
        Direction.W: (0, -1),
    }

    def neighbour(self, tile: Tile, direction: Direction):
        y = tile.y + self.map[direction][0]
        x = tile.x + self.map[direction][1]
        return None if -1 in {x, y} else self.tiles[y][x]

    def navigate(self, route: list[tuple[Direction, Tile]]):
        arrival, tile = route[-1]
        direction = next(
            direction
            for direction, connected in tile.connections.items()
            if opposing(direction) != arrival and connected
        )
        route.append((direction, self.neighbour(tile, direction)))
        return route

    def __init__(self, lines):
        self.tiles = defaultdict(list)
        for y, line in enumerate(lines):
            for x, tile in enumerate(line.strip()):
                Klass, *directions = char_map[tile]
                self.tiles[y].append(Klass(tile, x, y, *directions))
                if tile == "S":
                    self.start = self.tiles[y][x]
        neighbours = {
            direction: self.neighbour(self.start, direction)
            for direction in self.start.connections.keys()
        }
        for direction, neighbour in neighbours.items():
            if (
                isinstance(neighbour, Pipe)
                and neighbour.connections[opposing(direction)]
            ):
                self.start.connections[direction] = True

    def print(self, bounds: tuple[int, int, int, int] = None):
        if not bounds:
            bounds = (0, 0, len(self.tiles[0]), len(self.tiles))
        min_x, min_y, max_x, max_y = bounds
        for y, row in self.tiles.items():
            if min_y <= y <= max_y:
                print("".join([tile.char for tile in row[min_x:max_x]]))


def get_routes(data):
    grid = Grid(data)
    grid.print()
    routes = [
        grid.navigate(
            [
                (opposing(direction), grid.start),
            ]
        )
        for direction, connection in grid.start.connections.items()
        if connection
    ]
    while True:
        endpoints = {route[-1][1] for route in routes}
        if len(endpoints) == 1:
            return routes

        routes = [grid.navigate(route) for route in routes]


def one(input):
    data = list(fileinput.input(input))
    routes = get_routes(data)
    for i, route in enumerate(routes):
        write_route(
            width=len(data[0]),
            height=len(data),
            route=route,
            output=Path(f"./2023/day10output{i}.txt"),
        )
        print(len(routes[0]) - 1)
    return


def row_gen(data: Iterable, empty=None):
    for char in data:
        yield empty
        yield char
    yield empty


def grid_gen(width: int, height: int, data: Iterable[Iterable], empty=None):
    """
    >>> [list(row) for row in grid_gen(5, 5, [[1,2],[3,4]], empty=0)]
    [[0, 0, 0, 0, 0], [0, 1, 0, 2, 0], [0, 0, 0, 0, 0], [0, 3, 0, 4, 0], [0, 0, 0, 0, 0]]
    """
    data_iter = iter(data)
    y_blank = True
    for y in range(height):
        if y_blank:
            yield [0] * width
        else:
            yield row_gen(next(data_iter), empty=empty)
        y_blank = not y_blank


class Row(list):
    def __init__(self, input: Iterable):
        super().__init__()


class Matrix(list):
    def __init__(self, input: Iterable[Iterable]):
        super().__init__()


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


@dataclass
class Cell:
    position: Position
    value: any = None

    def __post_init__(self):
        if isinstance(self.value, str):
            Klass, *directions = char_map[self.value]
            self.value = Klass(
                self.value, self.position.x, self.position.y, *directions
            )


def get_loop(data) -> dict[Position, Tile]:
    routes = get_routes(data)

    loop = dict()
    for _, c in routes[0] + list(reversed(routes[1])):
        loop[Position(c.x * 2 + 1, c.y * 2 + 1)] = c
    return loop


def write_route(
    width: int, height: int, route: Iterable[tuple[Direction, Tile]], output: Path
):
    path = [GridNode(x=tile.x, y=tile.y) for _, tile in route]
    grid = PathGrid(matrix=list(repeat(list(repeat(1, width)), height)))
    output.write_text(grid.grid_str(path=path, start=path[0], end=path[-1]))

def write_matrix(matrix: Iterable[Iterable], output: Path):
    output.write_text(PathGrid(matrix=matrix).grid_str())


def two(input):
    data = [line.strip() for line in fileinput.input(input)]
    height = len(data) * 2 + 1
    width = len(data[0]) * 2 + 1

    cells = dict()
    data_grid = [[None] * width for _ in range(height)]
    matrix = [[1] * width for _ in range(height)]

    for y, row in enumerate(grid_gen(width, height, data)):
        for x, char in enumerate(row):
            position = Position(x, y)
            cell = Cell(position, char)
            cells[position] = cell
            data_grid[position.y][position.x] = cell
            pass
    pass

    # Block Loop
    for position, tile in get_loop(data).items():
        matrix[position.y][position.x] = 0
        for direction, connected in tile.connections.items():
            if connected:
                neighbour = position.neighbour(direction)
                matrix[neighbour.y][neighbour.x] = 0
        pass
        Path("./2023/day10output.txt").write_text(PathGrid(matrix=matrix).grid_str())
        time.sleep(0.3)
    return

    start = grid.node(0, 0)
    end = grid.node(width - 1, height - 1)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)

    print("operations:", runs, "path length:", len(path))
    Path("./2023/day10output.txt").write_text(
        grid.grid_str(path=path, start=start, end=end)
    )


def main():
    # one("./2023/day10.txt")
    two("./2023/day10.txt")

    # width= 5
    # height=5
    # matrix = [[1] * width for _ in range(height)]
    # matrix[4][0] = 0
    # write_matrix(matrix, Path("./2023/day10output.txt"))


if __name__ == "__main__":
    doctest.testmod()
    main()
