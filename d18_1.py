from enum import IntEnum

import numpy as np


def run(lines: list[str]) -> int:
    arr: list[tuple[int]] = [tuple(int(e) for e in l.split(",")) for l in lines]
    mins = [min(v[0] for v in arr), min(v[1] for v in arr), min(v[2] for v in arr)]
    maxs = [max(v[0] for v in arr), max(v[1] for v in arr), max(v[2] for v in arr)]

    visible_faces = 0
    for view in [(0, 1, 2), (2, 1, 0), (0, 2, 1)]:
        for c0 in range(mins[view[0]], maxs[view[0]] + 1):
            for c1 in range(mins[view[1]], maxs[view[1]] + 1):
                prev_full = False
                for c2 in range(mins[view[2]], maxs[view[2]] + 1):
                    abs_coord = (c0, c1, c2) if view == (0, 1, 2) \
                        else (c2, c1, c0) if view == (2, 1, 0) \
                        else (c0, c2, c1)
                    cur_full = abs_coord in arr
                    if cur_full and not prev_full:
                        visible_faces += 1
                    prev_full = cur_full

                prev_full = False
                for c2 in range(maxs[view[2]], mins[view[2]] - 1, -1):
                    abs_coord = (c0, c1, c2) if view == (0, 1, 2) \
                        else (c2, c1, c0) if view == (2, 1, 0) \
                        else (c0, c2, c1)
                    cur_full = abs_coord in arr
                    if cur_full and not prev_full:
                        visible_faces += 1
                    prev_full = cur_full
    return visible_faces


def main() -> None:
    with open("i18.txt", "r") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def test() -> None:
    res = run("""1,1,1
2,1,1""".splitlines())
    assert res == 10

    res = run("""2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""".splitlines())
    assert res == 64


if __name__ == "__main__":
    test()
    main()
