from collections import defaultdict
from dataclasses import dataclass, field
import doctest
import fileinput
import logging
import math
import operator
import re
from typing import Iterable, Optional, Union
from pprint import pprint

Operator = Union[operator.lt, operator.gt]
Range = tuple[int, int]
PartRange = dict[str, Range]
ResultDict = defaultdict[list, PartRange]


@dataclass
class Part:
    string: str
    data: dict = field(default_factory=dict)

    def __post_init__(self):
        """
        >>> Part('{x=787,m=2655,a=1222,s=2876}')
        Part(string='{x=787,m=2655,a=1222,s=2876}', data={'x': 787, 'm': 2655, 'a': 1222, 's': 2876})
        """
        for key_value in self.string.strip("{}").split(","):
            key, value = key_value.split("=")
            self.data[key] = int(value)


def overlap(x: Range, y: Range):
    assert x[0] < x[1]
    assert y[0] < y[1]
    assert y[0] < x[1]
    return max(x[0], y[0]), min(x[1], y[1])


def overlaps(x: dict[str, Range], y: dict[str, Range]):
    return {k: overlap(x[k], y[k]) for k in x.keys()}


@dataclass
class Rule:
    string: str

    destination: str = ""
    attribute: Optional[str] = None
    operator: Optional[Operator] = None
    threshold: Optional[int] = None

    match: Optional[Range] = None
    no_match: Optional[Range] = None

    pattern = re.compile("^(.*?)([<>])(\d+):(.*?)$")

    def __post_init__(self):
        """
        >>> Rule('x>10:one')
        Rule(string='x>10:one', destination='one', attribute='x', operator=<built-in function gt>, threshold=10, match=(11, 4000), no_match=(1, 10))

        >>> Rule('A')
        Rule(string='A', destination='A', attribute=None, operator=None, threshold=None, match=None, no_match=None)
        """
        if m := self.pattern.match(self.string):
            self.attribute = m.group(1)
            self.operator = {"<": operator.lt, ">": operator.gt}[m.group(2)]
            self.threshold = int(m.group(3))
            self.destination = m.group(4)

            self.match = (
                (1, self.threshold - 1)
                if self.operator == operator.lt
                else (self.threshold + 1, 4000)
            )
            self.no_match = (
                (1, self.threshold)
                if self.operator == operator.gt
                else (self.threshold, 4000)
            )
            assert (self.match[1] - self.match[0] + 1) + (
                self.no_match[1] - self.no_match[0] + 1
            ) == 4000
        else:
            self.destination = self.string

    def evaluate(self, part: Part):
        """
        >>> Rule('A').evaluate(Part('{a=1}'))
        'A'
        >>> Rule('a>10:dest').evaluate(Part('{a=1}'))
        >>> Rule('a<10:dest').evaluate(Part('{a=1}'))
        'dest'
        """
        if self.attribute is not None:
            value = part.data[self.attribute]
            return self.destination if self.operator(value, self.threshold) else None
        return self.destination

    def evaluate_range(self, part_range: PartRange):
        match = part_range.copy()

        if self.attribute is not None:
            no_match = part_range.copy()
            match[self.attribute] = overlap(match[self.attribute], self.match)
            no_match[self.attribute] = overlap(no_match[self.attribute], self.no_match)
            assert range_combinations(match) + range_combinations(
                no_match
            ) == range_combinations(part_range)
        else:
            no_match = None
            assert range_combinations(match) == range_combinations(part_range)
        return match, no_match


@dataclass
class Workflow:
    string: str
    name: str = ""
    rules: list[Rule] = field(default_factory=list)

    def __post_init__(self):
        """
        >>> Workflow('px{a<2006:qkq,m>2090:A,rfg}')
        Workflow(string='px{a<2006:qkq,m>2090:A,rfg}', name='px', rules=[Rule(string='a<2006:qkq', destination='qkq', attribute='a', operator=<built-in function lt>, threshold=2006, match=(1, 2005), no_match=(2006, 4000)), Rule(string='m>2090:A', destination='A', attribute='m', operator=<built-in function gt>, threshold=2090, match=(2091, 4000), no_match=(1, 2090)), Rule(string='rfg', destination='rfg', attribute=None, operator=None, threshold=None, match=None, no_match=None)])
        """
        self.name, part_strings = self.string.split("{")
        self.rules = []
        for part_string in part_strings.strip("}").split(","):
            self.rules.append(Rule(part_string.strip()))

    def evaluate(self, part: Part):
        for rule in self.rules:
            if destination := rule.evaluate(part):
                return destination
        return None

    def evaluate_range(self, part_range: PartRange) -> dict[str, PartRange]:
        input_combinations = range_combinations(part_range)
        results = defaultdict(list)
        for rule in self.rules:
            match, no_match = rule.evaluate_range(part_range)
            results[rule.destination].append(match)
            part_range = no_match
        assert no_match is None
        assert input_combinations == sum(
            [list_combinations(x) for x in results.values()]
        )
        return results


def parse_input(input) -> tuple[dict[str, Workflow], list[Rule]]:
    workflows = {}
    parts = []

    section = 1
    for line in list(fileinput.input(input)):
        if line.strip():
            if section == 1:
                workflow = Workflow(line.strip())
                workflows[workflow.name] = workflow
            else:
                parts.append(Part(line.strip()))
        else:
            section += 1
    return workflows, parts


def one(input):
    workflows, parts = parse_input(input)
    accepted = []
    for part in parts:
        workflow = workflows["in"]
        while True:
            destination = workflow.evaluate(part)
            if destination == "A":
                accepted.append(part)
                break
            elif destination == "R":
                break
            workflow = workflows[destination]
    pprint(sum([sum([part.data[a] for a in "xmas"]) for part in accepted]))


def range_combinations(part_range: PartRange):
    return math.prod([x - n + 1 for n, x in part_range.values()])


def list_combinations(part_ranges: Iterable[PartRange]):
    return sum([range_combinations(part_range) for part_range in part_ranges])


end_state = {"A", "R"}
part_range_max = dict(x=(1, 4000), m=(1, 4000), a=(1, 4000), s=(1, 4000))
part_range_max_combinations = range_combinations(part_range_max)


def workflow_queue(results: ResultDict) -> list[str]:
    return list(filter(lambda k: k not in end_state, results.keys()))


def two(input):
    workflows, _ = parse_input(input)

    results = defaultdict(list)
    results["in"].append(part_range_max)

    while queue := workflow_queue(results):
        for workflow_name in queue:
            for part_range_input in results[workflow_name]:
                evaluation = workflows[workflow_name].evaluate_range(part_range_input)
                for destination, part_range_outputs in evaluation.items():
                    results[destination].extend(part_range_outputs)
            del results[workflow_name]
        assert part_range_max_combinations == sum(
            [list_combinations(x) for x in results.values()]
        )

    print(list_combinations(results["A"]))


def main():
    one("./2023/day19.txt")
    two("./2023/day19.txt")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    doctest.testmod()
    main()
