Pos = tuple[int, int]

def parse_area(lines: list[str]) -> dict[Pos, str]:
    area: dict[Pos, str] = {}
    for line in lines:
        pairs = [(int(a[0]), int(a[1])) for a in [p.split(',') for p in line.split(" -> ")]]
        prev = pairs[0]
        for ni in range(1, len(pairs)):
            n = pairs[ni]
            if prev[0] == n[0]:
                increasing = 1 if n[1] - prev[1] > 0 else -1
                for y in range(prev[1], n[1] + increasing, increasing):
                    area[(prev[0], y)] = "#"
            elif prev[1] == n[1]:
                increasing = 1 if n[0] - prev[0] > 0 else -1
                for x in range(prev[0], n[0] + increasing, increasing):
                    area[(x, prev[1])] = "#"
            else:
                raise Exception("WTF")
            prev = n
    return area

def run(lines: list[str]) -> int:
    area = parse_area(lines)
    max_y = max(p[1] for p in area)
    fell_down = False
    while not fell_down:
        sand = (500, 0)
        while True:
            if sand[1] > max_y:
                fell_down = True
                break
            if not (sand[0], sand[1] + 1) in area:
                sand = (sand[0], sand[1] + 1)
                continue
            if not (sand[0] - 1, sand[1] + 1) in area:
                sand = (sand[0] - 1, sand[1] + 1)
                continue
            if not (sand[0] + 1, sand[1] + 1) in area:
                sand = (sand[0] + 1, sand[1] + 1)
                continue
            area[sand] = "o"
            break
    cnt = len([k for k in area.values() if k == "o"])
    return cnt



def main() -> None:
    with open("i14.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


def test() -> None:
    lines = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""".splitlines()
    assert run(lines) == 24


if __name__ == "__main__":
    test()
    main()
