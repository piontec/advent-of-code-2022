# A - rock
# B - paper
# C - scissors

# X - loose, Y - tie, Z - win

val = {"A": 1, "B": 2, "C": 3}

resmap = {
    "A X": "C",
    "A Y": "A",
    "A Z": "B",
    "B X": "A",
    "B Y": "B",
    "B Z": "C",
    "C X": "B",
    "C Y": "C",
    "C Z": "A",
}


def run(lines: list[str]) -> int:
    score = 0
    for line in lines:
        their, res = line.split(" ")
        mine = resmap[line]
        if their == mine:
            score += 3
        elif (their == "A" and mine == "B") or (their == "B" and mine == "C") or (their == "C" and mine == "A"):
            score += 6
        score += val[mine]
    return score


def main() -> None:
    with open("i2.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


def test() -> None:
    lines = """A Y
B X
C Z""".splitlines()
    res = run(lines)
    assert res == 12


if __name__ == "__main__":
    test()
    main()
