#!/usr/bin/python3
from shared import data, update_is_ordered, middle_page

if __name__ == '__main__':
    rules, updates = data()

    result = 0

    for update in updates:
        if update_is_ordered(update, rules):
            result += middle_page(update)

    print(result)
