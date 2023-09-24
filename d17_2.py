import typing
from enum import IntEnum

import numpy as np


class Types(IntEnum):
    EMPTY = 0
    WALL = 1
    STABLE = 2
    FALLING = 3


RocksRow = tuple[int, int, int, int, int, int, int]
StateKey = tuple[int, int, RocksRow]
StateVal = tuple[int, int]

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


def run(moves: str, orig_rocks_limit: int) -> int:
    cave = np.array([[Types.WALL] * 9], dtype=np.int8)
    moves_counter = 0
    rocks_counter = 0
    rocks_limit = orig_rocks_limit
    force_simulate = False
    remaining_rock_cycles_count, cycle_height_delta = 0, 0
    states: dict[StateKey, StateVal] = {}
    while rocks_counter < rocks_limit:
        last_row_with_rock_ind = get_first_row_with_rock(cave)
        add_rows = 7 - (cave.shape[0] - last_row_with_rock_ind - 1)
        vspace = np.array(([Types.WALL] + [Types.EMPTY] * 7 + [Types.WALL]) * add_rows).reshape(add_rows, 9)
        cave = np.vstack((cave, vspace))
        rock_index = rocks_counter % 5
        shape: np.ndarray = shapes[rock_index].copy()
        shape_pos = (last_row_with_rock_ind + 4, 3)
        jet_move_index = 0
        while True:
            # apply jet
            jet_move_index = moves_counter % len(moves)
            jet_move = moves[jet_move_index]
            moves_counter += 1
            shape_pos = apply_jet(jet_move, shape_pos, shape, cave)
            # move down
            new_shape_pos = (shape_pos[0] - 1, shape_pos[1])
            cave_after_move = cave[new_shape_pos[0]:new_shape_pos[0] + shape.shape[0], new_shape_pos[1]:new_shape_pos[1] + shape.shape[1]] + shape

            has_collision = np.any(cave_after_move[:][:] > Types.FALLING)
            if has_collision:
                shape[shape == Types.FALLING] = Types.STABLE
                cave[shape_pos[0]:shape_pos[0] + shape.shape[0], shape_pos[1]:shape_pos[1] + shape.shape[1]] += shape
                break
            shape_pos = new_shape_pos
        rocks_counter += 1

        if force_simulate:
            continue

        top_rock_row_index = get_first_row_with_rock(cave)
        top_shape = tuple(get_top_shape(cave))
        state_key = (rock_index, jet_move_index, top_shape)
        state_val = (rocks_counter, top_rock_row_index)

        # we haven't found cycle yet
        if state_key not in states.keys():
            states[state_key] = state_val
            continue

        cycle_rocks_delta = state_val[0] - states[state_key][0]
        cycle_height_delta = state_val[1] - states[state_key][1]
        remaining_rock_cycles_count = (orig_rocks_limit - rocks_counter) // cycle_rocks_delta
        rocks_left = (orig_rocks_limit - rocks_counter) % cycle_rocks_delta
        assert orig_rocks_limit == rocks_counter + remaining_rock_cycles_count * cycle_rocks_delta + rocks_left
        force_simulate = True
        rocks_counter += remaining_rock_cycles_count * cycle_rocks_delta

    res = get_first_row_with_rock(cave)
    res += remaining_rock_cycles_count * cycle_height_delta
    return res


def get_first_row_with_rock(cave: np.ndarray) -> int:
    last_row_with_rock_ind = cave.shape[0] - 1
    while True:
        if last_row_with_rock_ind == 0:
            break
        row = cave[last_row_with_rock_ind]
        row_i_has_solid = np.any(row[1:8] == Types.STABLE)
        if row_i_has_solid:
            break
        last_row_with_rock_ind -= 1
    return last_row_with_rock_ind


def get_top_shape(cave: np.ndarray) -> RocksRow:
    res: list[int] = []
    for i in range(1, 8):
        last_row_with_rock_ind = cave.shape[0] - 1
        while True:
            loc = cave[last_row_with_rock_ind][i]
            if loc == Types.STABLE or last_row_with_rock_ind == 0:
                res.append(last_row_with_rock_ind)
                break
            last_row_with_rock_ind -= 1
    min_index = min(res)
    res = [i - min_index for i in res]
    assert len(res) == 7
    return typing.cast(RocksRow, tuple(res))


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
    with open("i17.txt") as i:
        lines = i.readlines()
    lines = [line.rstrip('\n') for line in lines]
    res = run(lines[0], orig_rocks_limit=1000000000000)
    print(res)


def test() -> None:
    res = run(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>", orig_rocks_limit=1000000000000)
    assert res == 1514285714288


if __name__ == "__main__":
    test()
    main()
