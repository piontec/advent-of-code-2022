def prio(char: str) -> int:
    offset = 96 if char.islower() else 38
    res = bytes(char, encoding="ascii")[0] - offset
    return res


def run(lines: list[str]) -> int:
    res = 0
    line_index = 0
    while line_index + 2 < len(lines):
        for char in lines[line_index]:
            if char in lines[line_index + 1] and char in lines[line_index + 2]:
                res += prio(char)
                line_index += 3
                break
    return res


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
    assert res == 70


if __name__ == "__main__":
    test()
    main()
