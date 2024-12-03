#!/usr/bin/python3
import re

from shared import data

"""https://regex101.com/"""

mul_pattern = r"(mul)\((\d{1,3}),(\d{1,3})\)"
do_pattern = r"(do)\(\)"
dont_pattern = r"(don't)\(\)"

valid_instruction_re = re.compile("|".join([mul_pattern,do_pattern,dont_pattern]))

enabled = True
result = 0
for instruction in valid_instruction_re.findall(data()):
    if enabled:
        if instruction[0] == "mul":
            result += int(instruction[1]) * int(instruction[2])
        elif instruction[4] == "don't":
            enabled = False
    else:
        if instruction[3] == "do":
            enabled = True

print(result)

