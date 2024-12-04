from typing import Protocol, TypeVar

T = TypeVar("T")


class Addable(Protocol):
    def __add__(self: T, other: T) -> T: ...
