from collections import OrderedDict, defaultdict
from dataclasses import dataclass, field
import fileinput
from itertools import zip_longest
import math
from pprint import pprint
import re
from types import SimpleNamespace
from typing import Optional


def grouper(iterable, n, *, incomplete="fill", fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == "fill":
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == "strict":
        return zip(*args, strict=True)
    if incomplete == "ignore":
        return zip(*args)
    else:
        raise ValueError("Expected fill, strict, or ignore")


@dataclass
class Item:
    type: str
    value: int
    length: int = 1


@dataclass
class MapRange:
    type: str
    start: int
    end: int = field(init=None)

    destination_type: str
    destination_start: int
    destination_end: int = field(init=None)

    length: int

    def __post_init__(self):
        self.end = self.start + self.length - 1
        self.destination_end = self.destination_start + self.length - 1

    def __repr__(self) -> str:
        return (
            f"{self.type}:{self.start}:{self.end}>{self.destination_type}{self.destination_start}:{self.destination_end}"
        )

    @classmethod
    def from_line(cls, source_type, destination_type, line):
        destination, source, length = (int(n) for n in line.split())
        return cls(
            type=source_type,
            start=source,
            destination_type=destination_type,
            destination_start=destination,
            length=length,
        )

    def __contains__(self, item: int):
        return self.start <= item <= self.end

    def __getitem__(self, index):
        if index not in self:
            raise ValueError
        return Item(
            type=self.destination_type,
            value=self.destination_start + (index - self.start),
        )

    def next(self):
        for i in range(self.start, self.end + 1):
            yield Item(type=self.type, value=i)


@dataclass
class Map:
    type: str
    destination_type: str
    partial_ranges: list[MapRange] = field(default_factory=list)
    map: OrderedDict[int, MapRange] = field(init=False)

    def __repr__(self) -> str:
        return f"{self.type}>{self.destination_type}"

    def __post_init__(self):
        self.map = OrderedDict()

        self.partial_ranges.sort(key=lambda r: r.start)

        common = dict(
            type=self.type,
            destination_type=self.destination_type,
        )

        last = SimpleNamespace(end=-1)
        for current in self.partial_ranges:
            if current.start > last.end + 1:
                gap = MapRange(
                    start=last.end + 1,
                    destination_start=last.end + 1,
                    length=current.start - last.end - 1 ,
                    **common,
                )
                self.map[gap.start] = gap
                last = gap
            self.map[current.start] = current
            last = current
        # Final Range
        self.map[last.end + 1] = MapRange(
            start=last.end + 1,
            destination_start=last.end + 1,
            length=math.inf,
            **common,
        )

    def __contains__(self, item: int):
        for map_range in self.map.values():
            if item in map_range:
                return True
        return False

    def __getitem__(self, index):
        for map_range in self.map.values():
            if index in map_range:
                return map_range[index]
        raise ValueError


def common_range(a_start, a_end, b_start, b_end):
    if a_start > b_end or b_start > a_end:
        return None, None
    return max(a_start, b_start), min(a_end, b_end)


def get_ranges(ranges, start, end):
    result = []
    for range in ranges:
        if range.end < start:
            continue
        elif range.start > end:
            break
        result.append(range)
    return result


def remap(a_map: Map, b_map: Map):
    ranges = []

    common = dict(
        type=a_map.type,
        destination_type=b_map.destination_type,
    )

    for a_range in a_map.map.values():
        for b_range in get_ranges(
            b_map.map.values(), a_range.destination_start, a_range.destination_end
        ):
            start, end = common_range(
                a_range.destination_start,
                a_range.destination_end,
                b_range.start,
                b_range.end,
            )
            ranges.append(
                MapRange(
                    start=a_range.start + a_range.destination_start - start,
                    destination_start=b_range.end - end - end - start,
                    length=end - start,
                    **common,
                )
            )
    return Map(partial_ranges=ranges, **common)


def seed_parser_one(seeds: tuple[int]):
    return [Item(type="seed", value=seed) for seed in seeds]


def seed_parser_two(seeds: tuple[int]):
    result = []
    for start, length in grouper(seeds, 2):
        result.append(Item(type="seed", value=start, length=length))
    return result


def parse_file_input(file_input, seed_parser):
    data = defaultdict(list)
    seeds = []
    ranges = []

    lines = list(file_input)
    seeds = seed_parser([int(v) for v in lines[0].strip().split(":")[1].split()])

    header = None
    for line in lines[1:]:
        if ":" in line:
            header = line[:-5]
        elif line.strip():
            data[header].append(line.strip())

    maps = dict()
    for header, lines in data.items():
        source_type, _, destination_type = header.strip().split("-")
        maps[source_type] = Map(
            type=source_type.strip(),
            destination_type=destination_type,
            partial_ranges=[
                MapRange.from_line(source_type, destination_type, line)
                for line in data[header]
            ],
        )
    return seeds, maps


def one(input):
    lowest = SimpleNamespace(value=math.inf)
    seeds, maps = parse_file_input(fileinput.input(input), seed_parser_one)
    for seed in seeds:
        item = seed
        while item.type != "location":
            item = maps[item.type][item.value]
        if item.value < lowest.value:
            lowest = item
    print(lowest.value)


def reverse_range(range: MapRange):
    return MapRange(
        type=range.destination_type,
        start=range.destination_start,
        destination_type=range.type,
        destination_start=range.start,
        length=range.length,
    )


def reverse_map(map: Map):
    return Map(
        type=map.destination_type,
        destination_type=map.type,
        partial_ranges=[reverse_range(r) for r in map.partial_ranges],
    )


def contains(seeds, value):
    for seed in seeds:
        if seed.value <= value <= (seed.value + seed.length):
            return True
    return False


def two(input):
    seeds, maps = parse_file_input(fileinput.input(input), seed_parser_two)
    seeds.sort(key=lambda s: s.value)
    reverse_maps = {m.destination_type: reverse_map(m) for m in maps.values()}

    i = Item("location", 0)
    while True:
        if i.value % 100000 == 0:
            print(i.value)

        output = []
        current = i
        seed = None

        output.append(f"{current.type}:{current.value} > ")
        while current.type != "seed":
            current = reverse_maps[current.type][current.value]
            output.append(f"{current.type}:{current.value} > ")
        seed = current

        if contains(seeds, seed.value):
            output.append(current.value)
            print("\n".join([str(i) for i in output]))
            exit()

        i = Item("location", i.value + 1)



input = "./2023/day05.txt"
one(input)
two(input)
