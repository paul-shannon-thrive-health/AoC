from pathlib import Path
from types import SimpleNamespace


def sample_counts(game_samples):
    results = SimpleNamespace(red={0}, green={0}, blue={0})
    for game_sample in game_samples.split("; "):
        for colour_sample in game_sample.split(", "):
            sample_size, sample_colour = colour_sample.split()
            getattr(results, sample_colour).add(int(sample_size))
    return results


def fewest_possible(samples):
    return SimpleNamespace(
        red=max(getattr(samples, 'red')),
        green=max(getattr(samples, 'green')),
        blue=max(getattr(samples, 'blue')),
    )


total = 0

for game_line in (Path(__file__).parent / "input").read_text().splitlines():
    game_id, game_samples = game_line.split(": ")
    bag = fewest_possible(sample_counts(game_samples))
    total += bag.red * bag.blue * bag.green

print(f"Total ({Path(__file__).stem.title()}): {total}")
