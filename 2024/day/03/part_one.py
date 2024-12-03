#!/usr/bin/python3
import re

from shared import data

"""https://regex101.com/"""
valid_instruction_re = re.compile(r"mul\((?P<x>\d{1,3}),(?P<y>\d{1,3})\)")

result = 0
for x, y in valid_instruction_re.findall(data()):
    result += int(x) * int(y)

print(result)

