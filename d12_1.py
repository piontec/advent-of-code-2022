from dataclasses import dataclass, field
from queue import PriorityQueue

Pos = tuple[int, int]


@dataclass(order=True)
class State:
    dist_to_e: int
    cost_so_far: int = field(compare=False)
    visited: set[Pos] = field(compare=False)
    current: Pos = field(compare=False)


def dist(p1: Pos, p2: Pos) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def run(lines: list[str]) -> int:
    area: list[list[int]] = []
    start = (0, 0)
    end = (0, 0)
    for y in range(len(lines)):
        row: list[int] = []
        for x in range(len(lines[y])):
            if lines[y][x] == "S":
                row.append(0)
                start = (y, x)
            elif lines[y][x] == "E":
                row.append(25)
                end = (y, x)
            else:
                row.append(ord(lines[y][x]) - 97)
        area.append(row)
    start_state = State(dist(start, end), 0, set(), start)
    q = PriorityQueue()
    q.put(start_state)
    shortest = len(area) * len(area[0]) + 1
    while not q.empty():
        s: State = q.get()
        if s.dist_to_e == 0:
            if s.cost_so_far < shortest:
                shortest = s.cost_so_far
            continue
        for new_cur in [(s.current[0] - 1, s.current[1]),
                        (s.current[0] + 1, s.current[1]),
                        (s.current[0], s.current[1] - 1),
                        (s.current[0], s.current[1] + 1)]:
            if new_cur[0] < 0 or new_cur[0] >= len(area) or new_cur[1] < 0 or new_cur[1] >= len(area[0]):
                continue
            if new_cur not in s.visited and area[new_cur[0]][new_cur[1]] - area[s.current[0]][s.current[1]] <= 1:
                new_visited = s.visited.copy()
                new_visited.add(new_cur)
                new_state = State(dist(new_cur, end), s.cost_so_far + 1, new_visited, new_cur)
                has_better = False
                for st in q.queue:
                    if st.current == new_state.current and new_state.cost_so_far > st.cost_so_far:
                        has_better = True
                        break
                if not has_better:
                    q.put(new_state)
    return shortest


def main() -> None:
    with open("i12.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)
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
