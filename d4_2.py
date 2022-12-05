def run(lines: list[str]) -> int:
    res = 0
    for line in lines:
        min1, max1, min2, max2 = [int(n) for n in line.replace(",", "-").split("-")]
        if (min1 < min2 and max1 < min2) or (min2 < min1 and max2 < min1):
            continue
        res += 1
    return res


def main() -> None:
    with open("i4.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


def test() -> None:
    lines = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""".splitlines()
    res = run(lines)
    assert res == 4


if __name__ == "__main__":
    test()
    main()
