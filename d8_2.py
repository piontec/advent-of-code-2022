def run(lines: list[str]) -> int:
    area = []
    for line in lines:
        area.append([[int(c), 0] for c in line])

    for r in range(1, len(area) - 1):
        for c in range(1, len(area[0]) - 1):
            cur = area[r][c][0]
            vis_r, vis_l, vis_u, vis_d = 0, 0, 0, 0
            for i in range(c + 1, len(area[0])):
                vis_r += 1
                if area[r][i][0] >= cur:
                    break
            for i in range(c - 1, -1, -1):
                vis_l += 1
                if area[r][i][0] >= cur:
                    break
            for i in range(r + 1, len(area)):
                vis_d += 1
                if area[i][c][0] >= cur:
                    break
            for i in range(r - 1, -1, - 1):
                vis_u += 1
                if area[i][c][0] >= cur:
                    break
            area[r][c][1] = vis_r * vis_l * vis_d * vis_u
    best = 0
    for r in area:
        m = max(a[1] for a in r)
        if m > best:
            best = m
    return best

def main() -> None:
    with open("i8.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


def test() -> None:
    lines = """30373
25512
65332
33549
35390""".splitlines()
    assert run(lines) == 8


if __name__ == "__main__":
    test()
    main()
