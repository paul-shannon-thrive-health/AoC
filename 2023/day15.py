from collections import defaultdict
from dataclasses import dataclass
import doctest
import fileinput
import re
import sys


def parse_input(input):
    lines = list(fileinput.input(input))
    return lines[0].strip().split(",")


def hash(string: str):
    """
    start with a current value of 0.

    Then, for each character in the string starting from the beginning:
        Determine the ASCII code for the current character of the string.
        Increase the current value by the ASCII code you just determined.
        Set the current value to itself multiplied by 17.
        Set the current value to the remainder of dividing itself by 256.

    >>> hash('HASH')
    52
    """
    current = 0
    for character in string:
        o = ord(character)
        current += o
        current *= 17
        current = current % 256
    return current


def one(input):
    result = 0
    steps = parse_input(input)
    for step in steps:
        result += hash(step)
    print(result)


@dataclass
class Lens:
    label: str
    focal_length: int


def remove_lens_from_box(lens: Lens, box: list):
    """
    remove the lens with the given label if it is present in the box.
    Then, move any remaining lenses as far forward in the box as they can go without changing their order,
    filling any space made by removing the indicated lens. (If no lens in that box has the given label, nothing happens.)
    """
    return [l for l in box if l.label != lens.label]


def upsert_lens_in_box(lens: Lens, box: list):
    """
    If the operation character is an equals sign (=),
    it will be followed by a number indicating the focal length of the lens that needs to go into the relevant box;
    be sure to use the label maker to mark the lens with the label given in the beginning of the step so you can find it later.
    There are two possible situations:
        If there is already a lens in the box with the same label, replace the old lens with the new lens:
            remove the old lens and put the new lens in its place, not moving any other lenses in the box.
        If there is not already a lens in the box with the same label, add the lens to the box immediately behind any lenses already in the box.
        Don't move any of the other lenses when you do this. If there aren't any lenses in the box, the new lens goes all the way to the front of the box.
    """
    for i, existing_lens in enumerate(box):
        if existing_lens.label == lens.label:
            box[i] = lens
            return box
    box.append(lens)
    return box


def focusing_power(box_number: int, slot_number: int, focal_length: int) -> int:
    """
    The focusing power of a single lens is the result of multiplying together:
        One plus the box number of the lens in question.
        The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
        The focal length of the lens.
    """
    return (1 + box_number) * slot_number * focal_length


def two(input):
    result = 0
    steps = parse_input(input)

    boxes: defaultdict[int, list[Lens]] = defaultdict(list)

    for step in steps:
        label, operation, focal_length = re.split("([-=])", step, maxsplit=1)
        lens = Lens(label, int(focal_length) if focal_length else None)

        box = hash(label)
        if operation == "-":
            boxes[box] = remove_lens_from_box(lens, boxes[box])
        elif operation == "=":
            boxes[box] = upsert_lens_in_box(lens, boxes[box])
        else:
            print(f"bad operation: {operation}")
            sys.exit()

    for box_number, lenses in boxes.items():
        for slot_number, lense in enumerate(lenses, start=1):
            result += focusing_power(box_number, slot_number, lense.focal_length)
    print(result)


def main():
    one("./2023/day15.txt")
    two("./2023/day15.txt")


if __name__ == "__main__":
    doctest.testmod()
    main()
