import fileinput


def one(input):
    t, d = tuple(fileinput.input(input))
    t = [int(v) for v in t.strip().split()[1:]]
    d = [int(v) for v in d.strip().split()[1:]]

    result = 1

    for time, record in zip(t, d):
        success = set()
        for speed in range(1, time + 1):
            distance = (time - speed) * speed
            if distance > record:
                success.add(speed)
        print(f"{time}: {len(success)}")
        result *= len(success)

    print(result)


def two(input):
    t, d = tuple(fileinput.input(input))
    time = int("".join(t.strip().split()[1:]))
    record = int("".join(d.strip().split()[1:]))

    success = set()
    for speed in range(1, time + 1):
        distance = (time - speed) * speed
        if distance > record:
            success.add(speed)

    print(len(success))


input = "./2023/day06.txt"
one(input)
two(input)
