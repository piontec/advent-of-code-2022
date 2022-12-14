from dataclasses import dataclass

Pos = tuple[int, int]


@dataclass
class Node:
    height: int
    cost_here: int
    next: list[Pos]


def run(lines: list[str]) -> int:
    area: dict[Pos, Node] = {}
    start = (0, 0)
    end = (0, 0)
    inf = len(lines) * len(lines[0]) + 1
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "S":
                start = (x, y)
                height = 0
            elif lines[y][x] == "E":
                end = (x, y)
                height = 25
            else:
                height = ord(lines[y][x]) - 97
            pos = (x, y)
            area[pos] = Node(height, inf, [])

    for y in range(len(lines)):
        for x in range(len(lines[y])):
            pos = (x, y)
            for neigh in [(pos[0] - 1, pos[1]),
                          (pos[0] + 1, pos[1]),
                          (pos[0], pos[1] - 1),
                          (pos[0], pos[1] + 1)]:
                if neigh[0] < 0 or neigh[0] >= len(lines[0]) or neigh[1] < 0 or neigh[1] >= len(lines):
                    continue
                if area[neigh].height - area[pos].height <= 1:
                    area[pos].next.append(neigh)
    unvisited = set(area.keys())
    area[start].cost_here = 0
    current = start
    while len(unvisited) > 0:
        if current == end:
            break
        for n in area[current].next:
            if n not in unvisited:
                continue
            new_dist = area[current].cost_here + 1
            if new_dist < area[n].cost_here:
                area[n].cost_here = new_dist
        unvisited.remove(current)
        min_unvisited_dist = inf
        for n in unvisited:
            if area[n].cost_here < min_unvisited_dist:
                min_unvisited_dist = area[n].cost_here
                current = n

    return area[end].cost_here


def main() -> None:
    with open("i12.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


def test() -> None:
    lines = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".splitlines()
    assert run(lines) == 31


if __name__ == "__main__":
    test()
    main()
