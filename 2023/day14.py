from collections import defaultdict
from dataclasses import dataclass
import doctest
import fileinput
import logging
import re
import sys

Matrix = [list[list[str]]]
Position = tuple[int, int]


class Stone:
    ROUND = "O"
    SQUARE = "#"


GROUND = "."


@dataclass
class Platform:
    matrix: Matrix

    @property
    def width(self):
        return len(self.matrix[0])

    @property
    def height(self):
        return len(self.matrix)

    def __str__(self):
        """
        >>> str(Platform([[1,2,3],[4,5,6],[7,8,9]]))
        '123\\n456\\n789'
        """
        return "\n".join(["".join([str(c) for c in r]) for r in self.matrix])

    def consider(self, x, y):
        self.x = x
        self.y = y

    @property
    def current(self):
        return self.matrix[self.y][self.x]

    @current.setter
    def current(self, value):
        self.matrix[self.y][self.x] = value

    @property
    def north(self):
        return self.matrix[self.y - 1][self.x]

    @north.setter
    def north(self, value):
        self.matrix[self.y - 1][self.x] = value

    @property
    def south(self):
        return self.matrix[self.y + 1][self.x]

    @south.setter
    def south(self, value):
        self.matrix[self.y + 1][self.x] = value

    @property
    def east(self):
        return self.matrix[self.y][self.x + 1]

    @east.setter
    def east(self, value):
        self.matrix[self.y][self.x + 1] = value

    @property
    def west(self):
        return self.matrix[self.y][self.x - 1]

    @west.setter
    def west(self, value):
        self.matrix[self.y][self.x - 1] = value

    def roll(self, direction: str):
        if self.current == Stone.ROUND and getattr(self, direction) == GROUND:
            setattr(self, direction, Stone.ROUND)
            self.current = GROUND

    def roll_north(self):
        """
        >>> Platform([['O', '#', '.'],['.', '.', '.'],['O', 'O', 'O']]).roll_north().matrix
        [['O', '#', 'O'], ['O', 'O', '.'], ['.', '.', '.']]
        """
        for x in range(self.width):
            for y in range(self.height - 1, 0, -1):
                self.consider(x, y)
                self.roll("north")
        return self

    def roll_south(self):
        """
        >>> Platform([['O', 'O', 'O'], ['.', '.', '.'], ['O', '#', '.']]).roll_south().matrix
        [['.', '.', '.'], ['O', 'O', '.'], ['O', '#', 'O']]
        """
        for x in range(self.width):
            for y in range(0, self.height - 1):
                self.consider(x, y)
                self.roll("south")
        return self

    def roll_east(self):
        """
        >>> Platform([['O', '.', 'O'], ['O', '.', '.'], ['O', '#', '.']]).roll_east().matrix
        [['.', 'O', 'O'], ['.', '.', 'O'], ['O', '#', '.']]
        """
        for x in range(0, self.width - 1):
            for y in range(self.height):
                self.consider(x, y)
                self.roll("east")
        return self

    def roll_west(self):
        """
        >>> Platform([['O', '.', 'O'], ['.', 'O', '.'], ['O', '#', '.']]).roll_west().matrix
        [['O', 'O', '.'], ['O', '.', '.'], ['O', '#', '.']]
        """
        for x in range(self.width - 1, 0, -1):
            for y in range(self.height):
                self.consider(x, y)
                self.roll("west")
        return self

    def cycle(self):
        self.roll_north()
        self.roll_west()
        self.roll_south()
        self.roll_east()
        return self

    @property
    def load(self):
        """
        The amount of load caused by a single rounded rock (O) is equal to
        the number of rows from the rock to the south edge of the platform,
        including the row the rock is on.
        (Cube-shaped rocks (#) don't contribute to load.)
        So, the amount of load caused by each rock in each row is as follows:
            OOOO.#.O.. 10
            OO..#....#  9
            OO..O##..O  8
            O..#.OO...  7
            ........#.  6
            ..#....#.#  5
            ..O..#.O.O  4
            ..O.......  3
            #....###..  2
            #....#....  1
        """
        total_rows = self.height
        total_load = 0
        for y, row in enumerate(self.matrix):
            for char in row:
                if char == Stone.ROUND:
                    total_load += total_rows - y
        return total_load


def parse_input(input):
    return Platform(
        [[c for c in line.strip()] for line in list(fileinput.input(input))]
    )


def one(input):
    platform = parse_input(input)
    platform.roll_north()
    print(platform.load)


def two(input):
    platform = parse_input(input)
    for _ in range(1000000000):
        platform.cycle()
    print(platform.load)


def main():
    one("./2023/day14example.txt")
    two("./2023/day14example.txt")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    doctest.testmod()
    main()
