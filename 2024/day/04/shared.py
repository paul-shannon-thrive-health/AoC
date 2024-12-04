from pathlib import Path

from lib.grid import Grid


def data(stem="input.txt"):
    input_path = Path(__file__).parent / stem
    return Grid.from_file(input_path)
