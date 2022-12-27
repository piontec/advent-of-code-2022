Pos = tuple[int, int]


def run(lines: list[str], max_coord: int) -> int:
    sens_beacon: dict[Pos, Pos] = {}
    sens_dist: dict[Pos, int] = {}
    for line in lines:
        tmp = line.split("=")
        s_x = int(tmp[1].split(",")[0])
        s_y = int(tmp[2].split(":")[0])
        b_x = int(tmp[3].split(",")[0])
        b_y = int(tmp[4])
        s = (s_x, s_y)
        sens_beacon[s] = (b_x, b_y)
        sens_dist[s] = abs(s_x - b_x) + abs(s_y - b_y)
    p = check_circumference(max_coord, sens_beacon, sens_dist)
    return p[0] * 4000000 + p[1]


def is_possible(p: Pos, sens_beacon: dict[Pos, Pos], sens_dist: dict[Pos, int]) -> bool:
    if (p[0], p[1]) in sens_beacon.values():
        return False
    for s in sens_beacon.keys():
        cur_dist = abs(p[0] - s[0]) + abs(p[1] - s[1])
        if cur_dist <= sens_dist[s]:
            return False
    return True


def check_circumference(max_coord: int , sens_beacon: dict[Pos, Pos], sens_dist: dict[Pos, int]) -> Pos:
    for s, b in sens_beacon.items():
        r = abs(s[0] - b[0]) + abs(s[1] - b[1]) + 1
        for d in range(0, r, 1):
            points = [(s[0] + d, s[1] + r - d), (s[0] + r - d, s[1] - d), (s[0] - d, s[1] - r + d), (s[0] - r + d, s[1] + d)]
            for p in points:
                if 0 <= p[0] <= max_coord and 0 <= p[1] <= max_coord and is_possible(p, sens_beacon, sens_dist):
                    return p


def main() -> None:
    with open("i15.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines, max_coord=4000000)
    print(res)


def test() -> None:
    lines = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""".splitlines()
    assert run(lines, max_coord=20) == 56000011


if __name__ == "__main__":
    test()
    main()
