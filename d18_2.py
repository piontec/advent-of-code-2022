Coord = tuple[int, int, int]


def is_bubble(loc: Coord, arr: list[Coord], known_bubble_status: dict[Coord, bool],
              mins: list[int], maxs: list[int]):
    if loc in known_bubble_status:
        return known_bubble_status[loc]
    if loc in arr:
        raise Exception("can't check if busy space is a bubble")
    visited: list[Coord] = []
    to_visit = [loc, ]
    while len(to_visit) > 0:
        cur = to_visit.pop()
        visited.append(cur)
        # we reached the edge
        if cur[0] <= mins[0] or cur[0] >= maxs[0] \
                or cur[1] <= mins[1] or cur[1] >= maxs[1] \
                or cur[2] <= mins[2] or cur[2] >= maxs[2]:
            for v in visited:
                known_bubble_status[v] = False
            return False

        for neigh in [(cur[0] - 1, cur[1], cur[2]),
                      (cur[0] + 1, cur[1], cur[2]),
                      (cur[0], cur[1] - 1, cur[2]),
                      (cur[0], cur[1] + 1, cur[2]),
                      (cur[0], cur[1], cur[2] - 1),
                      (cur[0], cur[1], cur[2] + 1)]:
            # we don't know yet - visit neighbors that are empty
            if neigh not in visited and neigh not in to_visit and neigh not in arr:
                to_visit.append(neigh)
    # we ran out of neighbours and none was on the edge - it's a bubble
    for v in visited:
        known_bubble_status[v] = True
    return True


def run(lines: list[str]) -> int:
    arr: list[Coord] = [tuple(int(e) for e in l.split(",")) for l in lines]
    mins = [min(v[0] for v in arr), min(v[1] for v in arr), min(v[2] for v in arr)]
    maxs = [max(v[0] for v in arr), max(v[1] for v in arr), max(v[2] for v in arr)]

    known_bubble_status: dict[Coord, bool] = {}
    visible_faces = 0
    for view in [(0, 1, 2), (2, 1, 0), (0, 2, 1)]:
        for c0 in range(mins[view[0]], maxs[view[0]] + 1):
            for c1 in range(mins[view[1]], maxs[view[1]] + 1):
                prev_full = False
                for c2 in range(mins[view[2]], maxs[view[2]] + 1):
                    abs_coord = to_abs_coord(c0, c1, c2, view)
                    cur_full = abs_coord in arr
                    if cur_full and not prev_full and not is_bubble(to_abs_coord(c0, c1, c2 - 1, view), arr,
                                                                    known_bubble_status, mins, maxs):
                        visible_faces += 1
                    prev_full = cur_full

                prev_full = False
                for c2 in range(maxs[view[2]], mins[view[2]] - 1, -1):
                    abs_coord = to_abs_coord(c0, c1, c2, view)
                    cur_full = abs_coord in arr
                    if cur_full and not prev_full and not is_bubble(to_abs_coord(c0, c1, c2 + 1, view), arr,
                                                                    known_bubble_status, mins, maxs):
                        visible_faces += 1
                    prev_full = cur_full
    return visible_faces


def to_abs_coord(c0: int, c1: int, c2: int, view: tuple[int, int, int]) -> tuple[int, int, int]:
    abs_coord = (c0, c1, c2) if view == (0, 1, 2) \
        else (c2, c1, c0) if view == (2, 1, 0) \
        else (c0, c2, c1)
    return abs_coord


def main() -> None:
    with open("i18.txt", "r") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def test() -> None:
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
    assert res == 58


if __name__ == "__main__":
    test()
    main()
