Pos = tuple[int, int]


def run(lines: list[str], row: int) -> int:
    sens_beacon: dict[Pos, Pos] = {}
    sens_dist: dict[Pos, int] = {}
    max_dist = 0
    for line in lines:
        tmp = line.split("=")
        s_x = int(tmp[1].split(",")[0])
        s_y = int(tmp[2].split(":")[0])
        b_x = int(tmp[3].split(",")[0])
        b_y = int(tmp[4])
        s = (s_x, s_y)
        sens_beacon[s] = (b_x, b_y)
        dist = abs(s_x - b_x) + abs(s_y - b_y)
        sens_dist[s] = dist
        if dist > max_dist:
            max_dist = dist
    max_x = max(s[0] for s in sens_beacon.keys()) + max_dist
    min_x = min(s[0] for s in sens_beacon.keys()) - max_dist
    print(f"min_x = {min_x}, max_x = {max_x}")
    impossible_cnt = 0
    for x in range(min_x, max_x + 1, 1):
        if x % 1000 == 0:
            print(f"x = {x}")
        imp = False
        for s in sens_beacon.keys():
            cur_dist = abs(x - s[0]) + abs(row - s[1])
            if (x, row) in sens_beacon.values():
                continue
            if cur_dist <= sens_dist[s]:
                imp = True
                break
        if imp:
            impossible_cnt += 1
    return impossible_cnt

def main() -> None:
    with open("i15.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines, row=2000000)
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
    assert run(lines, row=10) == 26


if __name__ == "__main__":
    test()
    main()
