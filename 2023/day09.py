from collections import defaultdict
from dataclasses import dataclass, field
import doctest
from enum import Enum
import fileinput
from functools import reduce, total_ordering
from itertools import accumulate, cycle, pairwise, repeat
import operator
from pprint import pprint
import re
from typing import Iterable, Optional, Union


class Node:
    def __init__(self, value, next_node=None, prev_node=None):
        self.value = value
        self.next_node = next_node
        self.prev_node = prev_node

    def set_next_node(self, next_node):
        self.next_node = next_node

    def get_next_node(self):
        return self.next_node

    def set_prev_node(self, prev_node):
        self.prev_node = prev_node

    def get_prev_node(self):
        return self.prev_node

    def get_value(self):
        return self.value


class DoublyLinkedList:
    def __init__(self, iterable: Iterable):
        self.head_node = None
        self.tail_node = None
        for i in iterable:
            self.add_to_tail(i)

    def __repr__(self) -> str:
        return str([i for i in self])

    def __iter__(self):
        self.iterate = self.head_node
        return self

    def __next__(self):
        n = self.iterate
        if not n:
            raise StopIteration
        self.iterate = n.next_node
        return n.value

    def add_to_head(self, new_value):
        new_head = Node(new_value)
        current_head = self.head_node

        if current_head != None:
            current_head.set_prev_node(new_head)
            new_head.set_next_node(current_head)

        self.head_node = new_head

        if self.tail_node == None:
            self.tail_node = new_head

    def add_to_tail(self, new_value):
        new_tail = Node(new_value)
        current_tail = self.tail_node

        if current_tail != None:
            current_tail.set_next_node(new_tail)
            new_tail.set_prev_node(current_tail)

        self.tail_node = new_tail

        if self.head_node == None:
            self.head_node = new_tail

    def remove_head(self):
        removed_head = self.head_node

        if removed_head == None:
            return None

        self.head_node = removed_head.get_next_node()

        if self.head_node != None:
            self.head_node.set_prev_node(None)

        if removed_head == self.tail_node:
            self.remove_tail()

        return removed_head.get_value()

    def remove_tail(self):
        removed_tail = self.tail_node

        if removed_tail == None:
            return None

        self.tail_node = removed_tail.get_prev_node()

        if self.tail_node != None:
            self.tail_node.set_next_node(None)

        if removed_tail == self.head_node:
            self.remove_head()

        return removed_tail.get_value()

    def remove_by_value(self, value_to_remove):
        node_to_remove = None
        current_node = self.head_node

        while current_node != None:
            if current_node.get_value() == value_to_remove:
                node_to_remove = current_node
                break

            current_node = current_node.get_next_node()

        if node_to_remove == None:
            return None

        if node_to_remove == self.head_node:
            self.remove_head()
        elif node_to_remove == self.tail_node:
            self.remove_tail()
        else:
            next_node = node_to_remove.get_next_node()
            prev_node = node_to_remove.get_prev_node()
            next_node.set_prev_node(prev_node)
            prev_node.set_next_node(next_node)

        return node_to_remove


def make_zero(data_tree: list[DoublyLinkedList]) -> list[DoublyLinkedList]:
    data_tree.append(
        DoublyLinkedList([j - i for i, j in pairwise(data_tree[-1])])
    )
    if any(data_tree[-1]):
        return make_zero(data_tree)
    return data_tree


def extrapolate(samples: DoublyLinkedList):
    tree = make_zero(
        [
            samples,
        ]
    )
    tree[-1].add_to_head(0)
    tree[-1].add_to_tail(0)
    for bottom, top in pairwise(reversed(tree)):
        top.add_to_head(top.head_node.value - bottom.head_node.value)
        top.add_to_tail(top.tail_node.value + bottom.tail_node.value)
    return tree


def one(input):
    result = 0
    for sample_string in fileinput.input(input):
        samples = DoublyLinkedList([int(s) for s in sample_string.strip().split(" ")])
        extrapolated = extrapolate(samples)
        result += extrapolated[0].tail_node.value
    print(result)


def two(input):
    result = 0
    for sample_string in fileinput.input(input):
        samples = DoublyLinkedList([int(s) for s in sample_string.strip().split(" ")])
        extrapolated = extrapolate(samples)
        result += extrapolated[0].head_node.value
    print(result)


def main():
    one("./2023/day09.txt")
    two("./2023/day09.txt")


if __name__ == "__main__":
    doctest.testmod()
    main()
