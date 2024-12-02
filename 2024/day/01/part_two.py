#!/usr/bin/python3
from collections import defaultdict

from shared import data

left_column, right_column = data()

similarity = 0

right_column_count = defaultdict(int)

for right in right_column:
    right_column_count[right] += 1
for left in left_column:
    similarity += left * right_column_count[left]

print(similarity)