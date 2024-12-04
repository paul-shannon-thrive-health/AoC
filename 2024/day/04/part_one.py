#!/usr/bin/python3
from lib.grid import Grid
from shared import data

grid: Grid = data()

xs = filter(lambda cell: cell.content == "X", grid)

xmas_count = 0

for x in xs:
    words = list(grid.words(x.position, 4))
    xmas_count += len(list(filter(lambda word: word == "XMAS", words)))

print(xmas_count)
