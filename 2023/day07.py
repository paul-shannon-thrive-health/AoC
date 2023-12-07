from collections import defaultdict
from dataclasses import dataclass, field
import doctest
from enum import Enum
import fileinput
from functools import reduce, total_ordering
import operator
from typing import Union


def hand_type(cards: list["Card"], variant=None):
    """
    >>> hand_type(Hand('KTJJT').cards)
    <HandType.TWO: 3>
    >>> hand_type(Hand('KTJJT', variant="Joker").cards, variant="Joker")
    <HandType.FOUR: 6>
    >>> hand_type(Hand('KTKJT', variant="Joker").cards, variant="Joker")
    <HandType.FULL: 5>
    """
    jokers = (
        len(list(filter(lambda c: c.type == JokerType.J, cards)))
        if variant == "Joker"
        else 0
    )
    count = defaultdict(int)
    for card in cards:
        count[card.label] += 1
    sort = sorted(count.values())
    if sort == [5]:
        return HandType.FIVE
    elif sort == [1, 4]:
        return HandType.FIVE if jokers else HandType.FOUR
    elif sort == [2, 3]:
        return HandType.FIVE if jokers else HandType.FULL
    elif sort == [1, 1, 3]:
        return HandType.FOUR if jokers else HandType.THREE
    elif sort == [1, 2, 2]:
        if jokers == 1:
            return HandType.FULL
        elif jokers == 2:
            return HandType.FOUR
        else:
            return HandType.TWO
    elif sort == [1, 1, 1, 2]:
        return HandType.THREE if jokers else HandType.ONE
    else:
        return HandType.ONE if jokers else HandType.HIGH


HandType = Enum(
    "HandType", list(reversed(["FIVE", "FOUR", "FULL", "THREE", "TWO", "ONE", "HIGH"]))
)
CardType = Enum(
    "CardType",
    list(reversed(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"])),
)
JokerType = Enum(
    "JokerType",
    list(reversed(["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"])),
)


# @total_ordering
@dataclass
class Card:
    label: str
    variant: str = None
    type: Union[CardType, JokerType] = field(init=False)

    def __post_init__(self):
        self.type = getattr(
            JokerType if self.variant == "Joker" else CardType, self.label.upper()
        )

    def __hash__(self):
        return ord(self.label)

    def __eq__(self, other):
        return self.type == other.type

    def __lt__(self, other):
        """
        >>> Card('A') < Card('2')
        False
        >>> Card('2') < Card('J')
        True
        >>> Card('2', variant="Joker") < Card('J', variant="Joker")
        False
        """
        return self.type.value < other.type.value


@total_ordering
@dataclass
class Hand:
    cards: list[Card]
    bid: int
    variant: str = None
    type: HandType = field(init=False)

    def __init__(self, line: str, variant: str = None):
        card_string, bid_string = line.split(" ") if " " in line else (line, "")

        self.cards = [Card(c, variant=variant) for c in card_string]
        self.bid = int(bid_string) if bid_string else 0
        self.variant = variant
        self.type = hand_type(self.cards, variant=self.variant)

    def __eq__(self, other: "Hand"):
        return self.type == other.type and self.cards == other.cards

    def __lt__(self, other: "Hand"):
        """
        >>> Hand('KTJJT') < Hand('KK677')
        True
        >>> Hand('T55J5') < Hand('QQQJA')
        True
        >>> Hand('QQQJA', variant="Joker") < Hand('KTJJT', variant="Joker")
        True
        >>> Hand('T55J5', variant="Joker") < Hand('QQQJA', variant="Joker")
        True
        """
        if self.type != other.type:
            return self.type.value < other.type.value
        for i in range(5):
            if self.cards[i] != other.cards[i]:
                return self.cards[i] < other.cards[i]
        return False

    def __hash__(self):
        return reduce(operator.mul, (ord(card.label) for card in self.cards))


def one(input, variant=None):
    hands = []
    for line in fileinput.input(input):
        hand = Hand(line, variant=variant)
        hands.append(hand)

    winnings = 0
    for rank, hand in enumerate(sorted(hands), start=1):
        winnings += rank * hand.bid
    print(winnings)


def two(input):
    return one(input=input, variant="Joker")


def main():
    input = "./2023/day07.txt"
    one(input)
    two(input)


if __name__ == "__main__":
    doctest.testmod()
    main()
