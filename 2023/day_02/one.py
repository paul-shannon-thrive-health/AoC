from pathlib import Path
from types import SimpleNamespace

bag = SimpleNamespace(red=12, green=13, blue=14)


def sample_counts(game_samples):
    results = SimpleNamespace(red={0}, green={0}, blue={0})
    for game_sample in game_samples.split("; "):
        for colour_sample in game_sample.split(", "):
            sample_size, sample_colour = colour_sample.split()
            getattr(results, sample_colour).add(int(sample_size))
    return results


def possible(samples):
    for colour in ("red", "green", "blue"):
        if max(getattr(samples, colour)) > getattr(bag, colour):
            return False
    return True


total = 0

for game_line in (Path(__file__).parent / "input").read_text().splitlines():
    game_id, game_samples = game_line.split(": ")
    if possible(sample_counts(game_samples)):
        total += int(game_id[5:])

print(f"Total ({Path(__file__).stem.title()}): {total}")
