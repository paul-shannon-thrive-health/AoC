from dataclasses import dataclass, field
import doctest
import fileinput
from itertools import cycle
import math
import operator
import re


@dataclass
class Node:
    graph: "Graph"
    label: str
    left: str
    right: str
    history: list["Node"] = field(default_factory=list)
    z_history: list[int] = field(default_factory=list)
    cadence: int = 0

    def go(self, instruction):
        node = self.graph.go(self, instruction)
        return node

    def extrapolate(self, to, intersection=None):
        result = set()
        last = max(self.z_history)
        while last < to:
            last += self.cadence
            if not intersection or last in intersection:
                result.add(last)
        self.z_history.append(last)
        return result

    @property
    def is_a(self):
        return self.label.endswith("A")

    @property
    def is_z(self):
        return self.label.endswith("Z")

    def __repr__(self) -> str:
        return f"<Node:{self.label}>"


@dataclass
class Graph:
    nodes: dict[str, Node]

    def __init__(self, nodes: list[str]):
        self.nodes = dict()
        for node in nodes:
            self.add(node)

    def add(self, line: str):
        m = re.match(r"(.{3}) = \((.{3}), (.{3})\)", line.strip())
        node = m.group(1)
        left = m.group(2)
        right = m.group(3)

        self.nodes[node] = Node(self, node, left, right)
        return self.nodes[node]

    def go(self, node: Node, instruction: str) -> Node:
        return self[getattr(node, "left" if instruction == "L" else "right")]

    def __getitem__(self, key: str) -> Node:
        return self.nodes[key]


def one(input):
    lines = list(fileinput.input(input))

    instructions = lines[0].strip()
    graph = Graph(lines[2:])
    current = graph["AAA"]
    history = []

    for instruction in cycle(instructions):
        if current.label == "ZZZ":
            print(len(history))
            break
        current = current.go(instruction)
        history.append(current)


def find_from_cadence(nodes: list[Node]):
    nodes.sort(key=lambda n: n.cadence, reverse=True)
    longest = nodes[0]
    other = nodes[1:]
    lower_bound = longest.offset
    while True:
        until = lower_bound + 2**16
        intersection = longest.extrapolate(until=until)
        print(max(intersection))
        for node in other:
            intersection = node.extrapolate(until=until, intersection=intersection)
        if len(intersection) > 0:
            return min(intersection) - 1
        until = lower_bound


def get_cadence(history: list[Node]):
    z = [index for index, node in enumerate(history) if node.is_z]
    if len(z) >= 3:
        if z[-1] - z[-2] == z[-2] - z[-3]:
            return z[-3], z[-1] - z[-2]
    return None


def follow_instructions(node: Node, instructions):
    history = []
    for instruction in instructions:
        node = node.go(instruction)
        history.append(node)
    return node, history


def find_cadence(node, instructions):
    history = []
    while True:
        node, i_history = follow_instructions(node, instructions)
        history.extend(i_history)
        cadence = get_cadence(history)
        if cadence:
            return cadence


def two(input):
    lines = list(fileinput.input(input))

    instructions = lines[0].strip()
    graph = Graph(lines[2:])

    starting_nodes = [node for node in graph.nodes.values() if node.is_a]
    candences = [find_cadence(node, instructions) for node in starting_nodes]
    print(math.lcm(*[c[1] for c in candences]))


def main():
    one("./2023/day08.txt")
    two("./2023/day08.txt")


if __name__ == "__main__":
    doctest.testmod()
    main()
