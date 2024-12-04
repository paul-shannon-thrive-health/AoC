#!/usr/bin/python3
from typing import Iterable

from lib.grid import Grid, Position, Cell, Direction, BoundsError
from shared import data

valid_words = {"SAM", "MAS"}


def x_words(grid: Grid, position: Position) -> Iterable[tuple[str, str]]:
    """
    >>> x_words(Grid.from_iterables(["ABC", "DEF", "GHI"]), Position(1,1))
    (('AEI', 'GEC'),)

    Not: (('BEH', 'DEF'), ('AEI', 'GEC'))
    """
    words = (
        # (
        #     grid.word(position.offset(Direction.N, 1), Direction.S, 3),
        #     grid.word(position.offset(Direction.W, 1), Direction.E, 3),
        # ),
        (
            grid.word(position.offset(Direction.NW, 1), Direction.SE, 3),
            grid.word(position.offset(Direction.SW, 1), Direction.NE, 3),
        ),
    )
    return words


def print_debug_info(grid, cell, x_words):
    sub_grid = grid.sub_grid(cell.position.offset(Direction.NW, 1), Position(3, 3))
    print(f"--{cell.position}--")
    sub_grid.print()
    print(x_words)


def is_xmas(grid: Grid, cell: Cell) -> bool:
    """
    >>> grid = Grid.from_iterables([".M.", "MAS", ".S."])
    >>> is_xmas(grid, grid.at(Position(1,1)))
    False
    >>> grid = Grid.from_iterables([".S.", "MAS", ".M."])
    >>> is_xmas(grid, grid.at(Position(1,1)))
    False
    >>> grid = Grid.from_iterables([".M.", "SAM", ".S."])
    >>> is_xmas(grid, grid.at(Position(1,1)))
    False
    >>> grid = Grid.from_iterables([".S.", "SAM", ".M."])
    >>> is_xmas(grid, grid.at(Position(1,1)))
    False

    >>> grid = Grid.from_iterables(["M.M", ".A.", "S.S"])
    >>> is_xmas(grid, grid.at(Position(1,1)))
    True
    >>> grid = Grid.from_iterables(["S.M", ".A.", "S.M"])
    >>> is_xmas(grid, grid.at(Position(1,1)))
    True
    >>> grid = Grid.from_iterables(["M.M", ".A.", "S.S"])
    >>> is_xmas(grid, grid.at(Position(1,1)))
    True
    >>> grid = Grid.from_iterables(["M.M", ".A.", "S.S"])
    >>> is_xmas(grid, grid.at(Position(1,1)))
    True
    """
    if cell.content != "A":
        return False
    try:
        for a, b in x_words(grid, cell.position):
            if a in valid_words and b in valid_words:
                # print_debug_info(grid, cell, (a,b))
                return True
    except BoundsError:
        return False
    return False


if __name__ == "__main__":
    grid: Grid = data()
    xmas_count = 0
    for cell in grid:
        if is_xmas(grid, cell):
            xmas_count += 1

    print(xmas_count)
