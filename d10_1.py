def run(lines: list[str]) -> int:
    x = 1
    cycle = 0
    res: list[int] = []
    check_cycle = 20

    for line in lines:
        if line == "noop":
            check_cycle, cycle = do_cycle(check_cycle, cycle, res, x)
        else:
            check_cycle, cycle = do_cycle(check_cycle, cycle, res, x)
            check_cycle, cycle = do_cycle(check_cycle, cycle, res, x)
            x += int(line.split(" ")[1])
    return sum(res)


def do_cycle(check_cycle, cycle, res, x):
    cycle += 1
    if cycle == check_cycle and check_cycle <= 220:
        res.append(x * cycle)
        check_cycle += 40
    return check_cycle, cycle


def main() -> None:
    with open("i10.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


def test() -> None:
    lines = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""".splitlines()
    res = run(lines)
    assert res == 13140


if __name__ == "__main__":
    test()
    main()
