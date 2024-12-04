import operator
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from pathlib import Path
from typing import TypeVar, Generic, Callable, Generator, Iterable

from lib.protocol import Addable

T = TypeVar("T", bound=Addable)


class BoundsError(ValueError):
    """Raise when a position isn't bounded"""


UP = -1
DOWN = 1
LEFT = -1
RIGHT = 1

alpha_iterables = [
    'ABCDE',
    'FGHIJ',
    'KLMNO',
    'MNOPQ',
    'RSTUV',
]


@dataclass
class Position:
    x: int
    y: int

    def is_bounded(self, min_x: int, min_y: int, max_x: int, max_y: int) -> bool:
        return min_x <= self.x <= max_x and min_y <= self.y <= max_y

    def offset(self, direction: "Direction", length: int) -> "Position":
        new_position = Position(
            x=self.x + (length * direction.value.x),
            y=self.y + (length * direction.value.y),
        )
        return new_position


class Direction(Enum):
    N = Position(0, UP)
    NE = Position(RIGHT, UP)
    E = Position(RIGHT, 0)
    SE = Position(RIGHT, DOWN)
    S = Position(0, DOWN)
    SW = Position(LEFT, DOWN)
    W = Position(LEFT, 0)
    NW = Position(LEFT, UP)


@dataclass
class Cell(Generic[T]):
    position: Position
    content: T


@dataclass
class Grid(Generic[T]):
    """
        x=0
    y=0 ...
        ...
        ...
    """
    width: int
    height: int
    cells: list[list[Cell[T]]]

    def __iter__(self):
        for row in self.cells:
            for cell in row:
                yield cell

    def sub_grid(self, position: Position, dimensions: Position):
        return Grid(width=dimensions.x, height=dimensions.y, cells=[
            row[position.x:position.x + dimensions.x]
            for row in self.cells[position.y:position.y + dimensions.y]
        ])

    def print(self):
        for row in self.cells:
            print("".join([cell.content for cell in row]))

    @classmethod
    def from_file(cls, path: Path, func: Callable[[str], T] = str) -> "Grid[T]":
        with path.open() as open_file:
            return cls.from_iterables(open_file, func)

    @classmethod
    def from_iterables(cls, iterables: Iterable[Iterable[T]], func: Callable[[str], T] = str) -> "Grid[T]":
        lines = []
        x, y = 0, 0
        for y, line in enumerate(iterables):
            cells = []
            for x, char in enumerate(line):
                cells.append(Cell(Position(x, y), func(char)))
            lines.append(cells)
        return Grid(width=x + 1, height=y + 1, cells=lines)

    def in_bounds(self, position: Position) -> bool:
        return position.is_bounded(0, 0, self.width - 1, self.height - 1)

    def words(self, position: Position, min_length: int, max_length: int | None = None) -> Generator[T, None, None]:
        """
        >>> grid = Grid.from_iterables(alpha_iterables)
        >>> list(grid.words(Position(2,2), 3))
        ['MHC', 'MIE', 'MNO', 'MPV', 'MOT', 'MNR', 'MLK', 'MGA']
        >>> list(grid.words(Position(0,0), 5))
        ['ABCDE', 'AGMPV', 'AFKMR']
        """
        max_length = min_length if max_length is None else max_length
        for length in range(min_length, max_length + 1):
            for direction in Direction:
                try:
                    yield self.word(position, direction, length)
                except BoundsError:
                    pass

    def word(self, position: Position, direction: Direction, length: int) -> T:
        """
        >>> grid = Grid.from_iterables(alpha_iterables)
        >>> grid.word(Position(2,2), Direction.SE, 2)
        'MP'
        """
        content = [
            self.offset(position, direction, i).content
            for i in range(length)
        ]
        word = reduce(operator.add, content)
        return word

    def offset(self, position: Position, direction: Direction, length: int):
        """
        >>> grid = Grid.from_iterables(alpha_iterables)
        >>> cell = grid.offset(Position(2,2), Direction.N, 2)
        >>> cell.position == Position(2,0)
        True
        >>> cell.content
        'C'
        """
        new_position = position.offset(direction, length)
        if not self.in_bounds(new_position):
            raise BoundsError(f"Position {new_position} is outside the grid")
        return self.at(new_position)

    def at(self, position: Position) -> Cell[T]:
        """
        >>> grid = Grid.from_iterables(alpha_iterables)
        >>> cell = grid.at(Position(0,0))
        >>> cell.position == Position(0,0)
        True
        >>> cell.content
        'A'
        >>> grid.at(Position(2,1)).content
        'H'
        """
        if not self.in_bounds(position):
            raise BoundsError(f"Position {position} is outside the grid")
        cell = self.cells[position.y][position.x]
        return cell
