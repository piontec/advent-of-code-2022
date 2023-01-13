from enum import IntEnum

import numpy as np


class Types(IntEnum):
    EMPTY = 0
    WALL = 1
    STABLE = 2
    FALLING = 3


shapes = {
    0: np.array([[Types.FALLING] * 4]),  # -
    1: np.array([[Types.EMPTY, Types.FALLING, Types.EMPTY],  # +
                 [Types.FALLING] * 3,
                 [Types.EMPTY, Types.FALLING, Types.EMPTY]]),
    2: np.array([[Types.FALLING] * 3,
                 [Types.EMPTY, Types.EMPTY, Types.FALLING],
                 [Types.EMPTY, Types.EMPTY, Types.FALLING]]),  # mirrored L
    3: np.array([Types.FALLING] * 4).reshape(4, 1),  # |
    4: np.array([Types.FALLING] * 4).reshape(2, 2),  # .
}


def run(moves: str, rocks_limit: int) -> int:
    cave = np.array([[Types.WALL] * 9], dtype=np.int8)
    moves_counter = 0
    for rock_index in range(rocks_limit):
        last_row_with_rock_ind = cave.shape[0] - 1
        while True:
            if last_row_with_rock_ind == 0:
                break
            row = cave[last_row_with_rock_ind]
            row_i_has_solid = np.any(row[1:8] == Types.STABLE)
            if row_i_has_solid:
                break
            last_row_with_rock_ind -= 1
        add_rows = 7 - (cave.shape[0] - last_row_with_rock_ind - 1)
        vspace = np.array(([Types.WALL] + [Types.EMPTY] * 7 + [Types.WALL]) * add_rows).reshape(add_rows, 9)
        cave = np.vstack((cave, vspace))
        shape: np.ndarray = shapes[rock_index % 5].copy()
        shape_pos = (last_row_with_rock_ind + 4, 3)
        while True:
            # view_cave = cave.copy()
            # view_cave[shape_pos[0]:shape_pos[0] + shape.shape[0], shape_pos[1]:shape_pos[1] + shape.shape[1]] += shape

            # apply jet
            jet_move = moves[moves_counter % len(moves)]
            moves_counter += 1
            shape_pos = apply_jet(jet_move, shape_pos, shape, cave)
            # move down
            new_shape_pos = (shape_pos[0] - 1, shape_pos[1])
            cave_after_move = cave[new_shape_pos[0]:new_shape_pos[0] + shape.shape[0],
                                   new_shape_pos[1]:new_shape_pos[1] + shape.shape[1]] + shape

            # view_cave = cave.copy()
            # view_cave[shape_pos[0]:shape_pos[0] + shape.shape[0], shape_pos[1]:shape_pos[1] + shape.shape[1]] += shape

            has_collision = np.any(cave_after_move[:][:] > Types.FALLING)
            if has_collision:
                shape[shape == Types.FALLING] = Types.STABLE
                cave[shape_pos[0]:shape_pos[0] + shape.shape[0], shape_pos[1]:shape_pos[1] + shape.shape[1]] += shape
                break
            shape_pos = new_shape_pos
    top_offset = 0
    while True:
        row = cave[cave.shape[0] - top_offset - 1]
        row_has_solid = np.any(row[1:8] == Types.STABLE)
        if row_has_solid:
            return cave.shape[0] - top_offset - 1
        top_offset += 1


def apply_jet(jet_move: str, shape_pos: tuple[int, int], shape: np.ndarray, cave: np.ndarray) -> tuple[int, int]:
    new_x_pos = shape_pos[1] - 1 if jet_move == "<" else shape_pos[1] + 1
    # hitting wall - don't move
    if new_x_pos < 1 or (new_x_pos + shape.shape[1] - 1) > 7:
        return shape_pos
    # not hitting wall and at or above new empty rows - move
    if shape_pos[0] >= cave.shape[0] - 3:
        return shape_pos[0], new_x_pos
    cave_after_move = cave[shape_pos[0]:shape_pos[0] + shape.shape[0], new_x_pos:new_x_pos + shape.shape[1]] + shape
    has_collision = np.any(cave_after_move[:][:] > Types.FALLING)
    return shape_pos if has_collision else (shape_pos[0], new_x_pos)


def main() -> None:
    with open("i17.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines[0], rocks_limit=2022)
    print(res)


def test() -> None:
    res = run(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>", rocks_limit=2022)
    assert res == 3068


if __name__ == "__main__":
    test()
    main()
