from pathlib import Path
import string
import re

input = (Path(__file__).parent / "input").read_text()

words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

forward_pattern = re.compile(r"(" + "|".join(words) + "|[0-9]{1})")
reverse_pattern = re.compile(r"(" + "|".join([w[::-1] for w in words]) + "|[0-9]{1})")

lookup = {
    **{word: i + 1 for i, word in enumerate(words)},
    **{word: i + 1 for i, word in enumerate([w[::-1] for w in words])},
}


class Digit:
    def __init__(self, match) -> None:
        self.string = match.group(1)
        self.int = (
            int(self.string) if self.string in string.digits else lookup[self.string]
        )

    def __repr__(self) -> str:
        return self.string



def find_digits(pattern, string):
    return [Digit(i) for i in pattern.finditer(string)]


total = 0
for line in input.splitlines():
    forward_digits = find_digits(forward_pattern, line)
    reverse_digits = find_digits(reverse_pattern, line[::-1])
    value = int(f"{forward_digits[0].int}{reverse_digits[0].int}")
    total += value

print(f"Total (Two): {total}")
