def run(lines: list[str], top: int = 1) -> int:
    best = [0] * top
    current = 0
    for line in lines:
        if line:
            current += int(line)
        else:
            for i in range(len(best)):
                if best[i] < current:
                    for j in range(len(best) - 1, i, -1):
                        best[j] = best[j - 1]
                    best[i] = current
                    break
            current = 0
    return sum(best)


def main() -> None:
    with open("i1.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    lines.append("")
    res = run(lines)
    print(res)
    res = run(lines, top=3)
    print(res)


def test() -> None:
    lines = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

""".splitlines()
    res = run(lines)
    assert res == 24000
    res = run(lines, top=3)
    assert res == 45000


if __name__ == "__main__":
    test()
    main()
