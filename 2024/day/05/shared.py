from collections import defaultdict
from pathlib import Path
from typing import TypeAlias

Rule: TypeAlias = tuple[int, int]
Rules: TypeAlias = dict[int, list[Rule]]
Update: TypeAlias = tuple[int, ...]
Updates: TypeAlias = list[Update]


def data(stem: str = "input.txt") -> tuple[Rules, Updates]:
    rules = defaultdict(list)
    updates = []

    update = False
    input_path = Path(__file__).parent / stem
    with open(input_path) as open_file:
        for line in open_file:
            if line.strip() == "":
                update = True
                continue
            if update:
                updates.append(tuple(map(int, line.split(","))))
            else:
                rule = tuple(map(int, line.split("|")))
                rules[rule[0]].append(rule)
                rules[rule[1]].append(rule)
    return rules, updates


def update_is_ordered(update: Update, rules: Rules) -> bool:
    for page in update:
        for lower_page, higher_page in rules[page]:
            if lower_page in update and higher_page in update:
                if update.index(lower_page) > update.index(higher_page):
                    return False
    return True


def middle_page(update: Update) -> int:
    """
    >>> middle_page((1, 2, 3, 4, 5))
    3
    """
    index = (len(update) - 1) // 2
    return update[index]
