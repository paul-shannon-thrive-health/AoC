from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path


@dataclass
class Report:
    levels: list[int]

    @classmethod
    def from_line(cls, line: str):
        """
        >>> Report.from_line("1 2 3")
        Report(levels=[1, 2, 3])
        """
        return cls(levels=list(map(int, line.split())))

    @property
    def safe(self) -> bool:
        return (self.increasing or self.decreasing) and self.are_differences_bounded(min_value=1, max_value=3)

    @property
    def potentially_safe(self) -> bool:
        """
        >>> Report.from_line("7 6 4 2 1").potentially_safe
        True
        >>> Report.from_line("1 2 7 8 9").potentially_safe
        False
        >>> Report.from_line("9 7 6 2 1").potentially_safe
        False
        >>> Report.from_line("1 3 2 4 5").potentially_safe
        True
        >>> Report.from_line("8 6 4 4 1").potentially_safe
        True
        >>> Report.from_line("1 3 6 7 9").potentially_safe
        True
        """
        if self.safe:
            return True
        for i in range(len(self.levels)):
            if Report(self.levels[:i] + self.levels[i + 1:]).safe:
                return True
        return False

    @property
    def decreasing(self) -> bool:
        """
        >>> Report.from_line("1 2 3").decreasing
        False
        >>> Report.from_line("3 2 1").decreasing
        True
        """
        return all(map(lambda a: a[0] > a[1], pairwise(self.levels)))

    @property
    def increasing(self) -> bool:
        """
        >>> Report.from_line("1 2 3").increasing
        True
        >>> Report.from_line("3 2 1").increasing
        False
        """
        return all(map(lambda a: a[0] < a[1], pairwise(self.levels)))

    @property
    def differences(self):
        return map(lambda a: abs(a[0] - a[1]), pairwise(self.levels))

    def are_differences_bounded(self, min_value: int, max_value: int) -> bool:
        """
        >>> Report.from_line("1 2 3").are_differences_bounded(min_value=1, max_value=3)
        True
        >>> Report.from_line("30 2 1").are_differences_bounded(min_value=1, max_value=3)
        False
        >>> Report.from_line("30 30 29").are_differences_bounded(min_value=1, max_value=3)
        False
        """
        return all(map(lambda a: min_value <= a <= max_value, self.differences))


def data(stem="input.txt"):
    input_path = Path(__file__).parent / stem
    with open(input_path) as open_file:
        for line in open_file:
            yield Report.from_line(line)
