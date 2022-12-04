def prio(char: str) -> int:
    offset = 96 if char.islower() else 38
    res = bytes(char, encoding="ascii")[0] - offset
    return res


def run(lines: list[str]) -> int:
    prios = 0
    for line in lines:
        half = len(line) // 2
        left = line[:half]
        right = line[half:]
        char: str = ""
        for c in left:
            if c in right:
                char = c
                break
        prios += prio(char)
    return prios


def main() -> None:
    with open("i3.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


def test() -> None:
    lines = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""".splitlines()
    res = run(lines)
    assert res == 157


if __name__ == "__main__":
    test()
    main()
