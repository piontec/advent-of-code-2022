# A X - rock
# B Y - paper
# C Z - scissors

val = {"X": 1, "Y": 2, "Z": 3}

resmap = {
    "A X": 3 + 1,
    "A Y": 6 + 2,
    "A Z": 0 + 3,
    "B X": 0 + 1,
    "B Y": 3 + 2,
    "B Z": 6 + 3,
    "C X": 6 + 1,
    "C Y": 0 + 2,
    "C Z": 3 + 3,
}


def run2(lines: list[str]) -> int:
    score = 0
    for line in lines:
        score += resmap[line]
    return score


def run(lines: list[str]) -> int:
    score = 0
    for line in lines:
        their, mine = line.replace("A", "X").replace("B", "Y").replace("C", "Z").split(" ")
        if their == mine:
            score += 3
        elif (their == "X" and mine == "Y") or (their == "Y" and mine == "Z") or (their == "Z" and mine == "X"):
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
    assert res == 15


if __name__ == "__main__":
    test()
    main()
