import re
from enum import StrEnum
from typing import cast

Pos = tuple[int, int]


class Dir(StrEnum):
    R = ">"
    L = "<"
    U = "^"
    D = "v"


class Turn(StrEnum):
    R = "R"
    L = "L"
    N = "N"


edge_to_dir = {
    0: Dir.D,
    1: Dir.L,
    2: Dir.U,
    3: Dir.R,
}


# noinspection PyCompatibility
def find_next_pos(pos: Pos, direction: Dir, steps: int, area: dict[int, list[str]]) -> Pos:
    assert steps > 0

    # noinspection PyCompatibility
    def make_one_step(p: Pos, d: Dir) -> Pos:
        match d:
            case Dir.U:
                return p[0] - 1, p[1]
            case Dir.R:
                return p[0], p[1] + 1
            case Dir.D:
                return p[0] + 1, p[1]
            case Dir.L:
                return p[0], p[1] - 1

    steps_left = steps
    new_y, new_x = pos
    last_pos = pos
    while steps_left > 0:
        new_y, new_x = make_one_step((new_y, new_x), direction)

        # check for looping around
        # lets for now accept that the tentative_pos can be outside valid area positions
        # we got too far down
        if new_y >= len(area) and direction == Dir.D:
            new_y = 0
        # we got too far up
        elif new_y < 0 and direction == Dir.U:
            new_y = len(area) - 1
        # we got too far right
        elif new_x >= len(area[new_y]) and direction == Dir.R:
            new_x = 0
        # too far left
        elif new_x < 0 and direction == Dir.L:
            new_x = len(area[new_y]) - 1

        # check for being outside valid area
        # y coordinate is already in the correct range, we have to check if x in this row exists
        if new_x > len(area[new_y]) - 1:
            continue
        # check for being "in the void"
        if area[new_y][new_x] == " ":
            continue

        # check for a wall
        if area[new_y][new_x] == "#":
            return last_pos

        assert area[new_y][new_x] == "."
        # now we actually count the step
        last_pos = (new_y, new_x)
        steps_left -= 1
    return last_pos


# noinspection PyCompatibility
def get_new_dir(current_dir: Dir, turn: Turn) -> Dir:
    if turn not in Turn._member_names_:
        raise Exception("No")
    if turn == Turn.N:
        return current_dir
    match current_dir:
        case Dir.U:
            return Dir.L if turn == Turn.L else Dir.R
        case Dir.R:
            return Dir.U if turn == Turn.L else Dir.D
        case Dir.D:
            return Dir.R if turn == Turn.L else Dir.L
        case Dir.L:
            return Dir.D if turn == Turn.L else Dir.U
        case _:
            raise Exception("WTF?")


# noinspection PyCompatibility
def run(lines: list[str], size: tuple[int, int], sides: dict[int, Pos], edges: dict[int, dict[int, tuple[int, int]]]) -> int:
    area: dict[int, list[str]] = {}
    li = 0
    for li in range(len(lines)):
        line = lines[li].rstrip()
        if not line or line == "\n":
            break
        area[li] = list(line)
    moves = lines[li + 1].strip()

    current_dir = Dir.R
    current_pos = (0, 0)
    if area[current_pos[0]][current_pos[1]] == " ":
        current_pos = find_next_pos((0, 0), current_dir, 1, area)
    while moves:
        m = re.match(r"\d+", moves)
        if not m:
            raise Exception("Couldn't find a number")
        move_len = int(m.group())
        if m.end() == len(moves):
            turn = Turn.N
        else:
            turn = cast(Turn, moves[m.end()])
        moves = moves[m.end() + 1:]

        current_pos = find_next_pos(current_pos, current_dir, move_len, area)
        current_dir = get_new_dir(current_dir, turn)

    res = 1000 * (current_pos[0] + 1) + 4 * (current_pos[1] + 1)
    match current_dir:
        case Dir.D:
            res += 1
        case Dir.L:
            res += 2
        case Dir.U:
            res += 3
    return res


def main() -> None:
    with open("i22.txt") as i:
        lines = i.readlines()
    # single map size
    size = (50, 50)
    # top-left corner of each map
    sides = {1: (0, 50), 2: (0, 100), 3: (50, 50), 4: (100, 0), 5: (100, 50), 6: (150, 0)}
    # how edges are attached to each other; starting 0 from N and in input orientation; result is
    # in format (map, edge, entry_dir)
    edges = {
        1: {
            0: (6, 3),
            1: (2, 3),
            2: (3, 0),
            3: (4, 3),
        },
        2: {
            0: (6, 2),
            1: (5, 1),
            2: (3, 1),
            3: (1, 1),
        },
        3: {
            0: (1, 2),
            1: (2, 2),
            2: (5, 0),
            3: (4, 0),
        },
        4: {
            0: (3, 3),
            1: (5, 3),
            2: (6, 0),
            3: (1, 3),
        },
        5: {
            0: (3, 2),
            1: (2, 1),
            2: (6, 1),
            3: (4, 1),
        },
        6: {
            0: (4, 2),
            1: (5, 2),
            2: (2, 0),
            3: (1, 0),
        },
    }
    res = run(lines, size, sides, edges)
    print(res)


def test() -> None:
    # single map size
    size = (4, 4)
    # top-left corner of each map
    sides = {1: (0, 8), 2: (4, 0), 3: (4, 4), 4: (4, 8), 5: (8, 8), 6: (8, 12)}
    # how edges are attached to each other; starting 0 from N and in input orientation; result is
    # in format (map, edge)
    edges = {
        1: {
            0: (2, 0),
            1: (6, 1),
            2: (4, 0),
            3: (3, 0),
        },
        2: {
            0: (1, 0),
            1: (3, 3),
            2: (5, 2),
            3: (6, 2),
        },
        3: {
            0: (1, 3),
            1: (4, 3),
            2: (5, 3),
            3: (2, 1),
        },
        4: {
            0: (1, 2),
            1: (6, 0),
            2: (5, 0),
            3: (3, 1),
        },
        5: {
            0: (4, 2),
            1: (6, 3),
            2: (2, 3),
            3: (3, 2),
        },
        6: {
            0: (4, 1),
            1: (1, 3),
            2: (2, 3),
            3: (5, 1),
        },
    }
    res = run("""        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""".splitlines(), size, sides, edges)
    assert res == 5031


if __name__ == "__main__":
    test()
    main()
