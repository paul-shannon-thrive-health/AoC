from pathlib import Path


def data(stem="input.txt"):
    input_path = Path(__file__).parent / stem
    return input_path.read_text()
