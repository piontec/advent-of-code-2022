from collections import namedtuple
import re
from enum import StrEnum
from typing import cast

Pos = namedtuple("Pos", ["y", "x"])

Map = list[list[str]]


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

def parse_maps(area: dict[int, list[str]], size: int, sides_top_left_corners: dict[int, Pos]) -> tuple[dict[int, Map], int]:
    maps: dict[int, Map] = {}
    for map_index in range(1, 7):
        new_map: list[list[str]] = []
        top_left = sides_top_left_corners[map_index]
        for tmp_y in range(top_left.y, top_left.y + size):
            new_map.append(area[tmp_y][top_left.x : top_left.x + size])
        maps[map_index] = new_map
    # starting map is the one in the top-left corner
    current_map_index = 1
    return maps, current_map_index

def dir_to_edge_num(direction: Dir) -> int:
    if direction == Dir.U:
        return 0
    elif direction == Dir.R:
        return 1
    elif direction == Dir.D:
        return 2
    elif direction == Dir.L:
        return 3
    else:
        raise ValueError("Invalid direction")

def get_next_pos_and_dir(y: int, x: int, edge: int, new_edge: int, size: int) -> tuple[int, int, Dir]:
    s_max = size - 1

    if new_edge == 0:
        if edge == 0:
            return 0, s_max - x, Dir.D
        elif edge == 1:
            return 0, s_max - y, Dir.D
        elif edge == 2:
            return 0, x, Dir.D
        elif edge == 3:
            return 0, y, Dir.D
        else:
            raise ValueError("Invalid edge")
    elif new_edge == 1:
        if edge == 0:
            return s_max - x, s_max, Dir.L
        elif edge == 1:
            return s_max - y, s_max, Dir.L
        elif edge == 2:
            return x, s_max, Dir.L
        elif edge == 3:
            return y, s_max, Dir.L
        else:
            raise ValueError("Invalid edge")
    elif new_edge == 2:
        if edge == 0:
            return s_max, x, Dir.U
        elif edge == 1:
            return s_max, y, Dir.U
        elif edge == 2:
            return s_max, s_max - x, Dir.U
        elif edge == 3:
            return s_max, s_max - y, Dir.U
        else:
            raise ValueError("Invalid edge")
    elif new_edge == 3:
        if edge == 0:
            return x, 0, Dir.R
        elif edge == 1:
            return y, 0, Dir.R
        elif edge == 2:
            return s_max - x, 0, Dir.R
        elif edge == 3:
            return s_max - y, 0, Dir.R
        else:
            raise ValueError("Invalid edge")
    else:
        raise ValueError("Invalid new edge")

# noinspection PyCompatibility
def find_next_pos(pos: Pos, direction: Dir, steps: int, maps: dict[int, Map], current_map_index: int, 
                  edges: dict[int, dict[int, tuple[int, int]]], size: int) -> tuple[Pos, int, Dir]:
    assert steps > 0

    # noinspection PyCompatibility
    def make_one_step(p: Pos, d: Dir) -> Pos:
        match d:
            case Dir.U:
                return p.y - 1, p.x
            case Dir.R:
                return p.y, p.x + 1
            case Dir.D:
                return p.y + 1, p.x
            case Dir.L:
                return p.y, p.x - 1

    steps_left = steps
    new_y, new_x = pos
    last_pos = pos
    current_map = maps[current_map_index]
    new_map_index = current_map_index
    while steps_left > 0:
        new_y, new_x = make_one_step(Pos(new_y, new_x), direction)
        new_direction = direction
        new_map_index = current_map_index

        # check for looping around
        # lets for now accept that the tentative_pos can be outside the current map


        if (new_y >= len(current_map) and direction == Dir.D) \
                or (new_y < 0 and direction == Dir.U) \
                or (new_x >= len(current_map[new_y]) and direction == Dir.R) \
                or (new_x < 0 and direction == Dir.L):
            edge_num = dir_to_edge_num(direction)
            exit_mapping = edges[current_map_index][edge_num]
            new_map_index = exit_mapping[0]
            new_y, new_x, new_direction = get_next_pos_and_dir(new_y, new_x, edge_num, exit_mapping[1], size)

        # check for a wall
        if maps[new_map_index][new_y][new_x] == "#":
            return last_pos, current_map_index, direction

        assert maps[new_map_index][new_y][new_x] == "."
        # now we actually count the step
        last_pos = Pos(new_y, new_x)
        current_map_index = new_map_index
        current_map = maps[current_map_index]
        direction = new_direction
        steps_left -= 1
    return last_pos, current_map_index, direction


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
def run(lines: list[str], size: int, sides_top_left_corners: dict[int, Pos], 
        edges: dict[int, dict[int, tuple[int, int]]]) -> int:
    area: dict[int, list[str]] = {}
    li = 0
    for li in range(len(lines)):
        line = lines[li].rstrip()
        if not line or line == "\n":
            break
        area[li] = list(line)
    moves = lines[li + 1].strip()
    maps, current_map_index = parse_maps(area, size, sides_top_left_corners)

    current_map = maps[current_map_index]
    current_dir = Dir.R
    current_pos = Pos(0, 0)
    if current_map[current_pos.y][current_pos.x] == "#":
        current_pos = find_next_pos((0, 0), current_dir, 1, maps, current_map_index, edges, size)
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

        current_pos, current_map_index, current_dir = find_next_pos(current_pos, current_dir, move_len, maps, current_map_index, edges, size)
        current_dir = get_new_dir(current_dir, turn)

    res = 1000 * (sides_top_left_corners[current_map_index][0] + current_pos.y + 1) \
        + 4 * (sides_top_left_corners[current_map_index][1] + current_pos.x + 1)
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
    size = 50
    # top-left corner of each map
    sides = {1: Pos(0, 50), 2: Pos(0, 100), 3: Pos(50, 50), 4: Pos(100, 0), 5: Pos(100, 50), 6: Pos(150, 0)}
    # how edges are attached to each other; starting 0 from North and in input orientation; result is
    # in format (map, edge)
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
    size = 4
    # top-left corner of each map
    sides = {1: Pos(0, 8), 2: Pos(4, 0), 3: Pos(4, 4), 4: Pos(4, 8), 5: Pos(8, 8), 6: Pos(8, 12)}
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
            2: (2, 2),
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
