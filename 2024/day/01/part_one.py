#!/usr/bin/python3

from shared import data

left_column, right_column = data()

distance = 0
for first, second in zip(sorted(left_column), sorted(right_column)):
    distance += abs(first - second)
print(distance)

