#!/usr/bin/python3
from dataclasses import dataclass, field
from functools import cmp_to_key

from shared import data, update_is_ordered, middle_page, Rules, Update


@dataclass
class Page:
    number: int
    rules: list[rules] = field(default_factory=list)


def compare_pages(a: Page, b: Page) -> int:
    """
    any callable that accepts two arguments, compares them, and returns
         a negative number for less-than
         zero for equality
         or a positive number for greater-than
    """
    a_first = (a.number, b.number)
    b_first = (b.number, a.number)
    if a_first in a.rules:
        return -1
    elif b_first in a.rules:
        return 1
    return 0


def ordered_update(update: Update, rules: Rules) -> tuple[int, ...]:
    pages = [Page(page, rules[page]) for page in update]
    return tuple([page.number for page in sorted(pages, key=cmp_to_key(compare_pages))])


if __name__ == '__main__':
    rules, updates = data()

    result = 0

    bad_updates = []
    for update in updates:
        if not update_is_ordered(update, rules):
            bad_updates.append(update)

    for update in bad_updates:
        result += middle_page(ordered_update(update, rules))

    print(result)
