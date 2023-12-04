from collections import defaultdict
import fileinput
import re
from types import SimpleNamespace


def points_for_match(match: int):
    points = 1
    for _ in range(match - 1):
        points *= 2
    return points


def parse_card(card):
    name, winning_numbers, numbers = re.split(r"[:|]", card)
    return SimpleNamespace(
        name=int(name[5:]),
        winning_numbers=[int(w.strip()) for w in winning_numbers.strip().split()],
        numbers=[int(n.strip()) for n in numbers.strip().split()],
    )


def one(input="./2023/day04.txt"):
    total = 0
    for card_string in fileinput.input(input):
        card = parse_card(card_string)
        points = 0
        if matches := [n for n in card.numbers if n in card.winning_numbers]:
            points = points_for_match(len(matches))
        total += points
    print(total)


def two(input="./2023/day04.txt"):
    copies = defaultdict(lambda: 0)
    for card_string in fileinput.input(input):
        card = parse_card(card_string)
        copies[card.name] += 1
        if matches := [n for n in card.numbers if n in card.winning_numbers]:
            for _ in range(copies[card.name]):
                for i in range(card.name + 1, card.name + 1 + len(matches)):
                    copies[i] += 1
    print(sum(copies.values()))


one()
two()
