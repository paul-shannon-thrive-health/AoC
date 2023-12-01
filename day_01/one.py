from pathlib import Path
import string
import re

input = (Path(__file__).parent / "input").read_text()

total = 0
for line in input.splitlines():
    digits = [c for c in line if c in string.digits]
    value = int(f"{digits[0]}{digits[-1]}")
    total += value
print(f"Total (One): {total}")
