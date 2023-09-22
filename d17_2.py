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


def run(moves: str, orig_rocks_limit: int) -> int:
    cave = np.array([[Types.WALL] * 9], dtype=np.int8)
    moves_counter = 0
    rocks_counter = 0
    cycle_height_start = 0
    cycle_rock_index_start, cycle_rock_index_end = 0, 0
    rocks_limit = orig_rocks_limit
    force_simulate = False
    remaining_rocks_count_cycles, cycle_len = 0, 0
    while rocks_counter < rocks_limit:
        last_row_with_rock_ind = get_first_row_with_rock(cave)
        add_rows = 7 - (cave.shape[0] - last_row_with_rock_ind - 1)
        vspace = np.array(([Types.WALL] + [Types.EMPTY] * 7 + [Types.WALL]) * add_rows).reshape(add_rows, 9)
        cave = np.vstack((cave, vspace))
        shape: np.ndarray = shapes[rocks_counter % 5].copy()
        shape_pos = (last_row_with_rock_ind + 4, 3)
        while True:
            # apply jet
            jet_move = moves[moves_counter % len(moves)]
            moves_counter += 1
            shape_pos = apply_jet(jet_move, shape_pos, shape, cave)
            # move down
            new_shape_pos = (shape_pos[0] - 1, shape_pos[1])
            cave_after_move = cave[new_shape_pos[0]:new_shape_pos[0] + shape.shape[0],
                                   new_shape_pos[1]:new_shape_pos[1] + shape.shape[1]] + shape

            has_collision = np.any(cave_after_move[:][:] > Types.FALLING)
            if has_collision:
                shape[shape == Types.FALLING] = Types.STABLE
                cave[shape_pos[0]:shape_pos[0] + shape.shape[0], shape_pos[1]:shape_pos[1] + shape.shape[1]] += shape
                break
            shape_pos = new_shape_pos
        top_rock_row_index = get_first_row_with_rock(cave)
        rocks_counter += 1

        # let's run it for all the possible combinations of rock and jet direction
        if rocks_counter < len(moves) * 5 or force_simulate:
            continue

        # we haven't found cycle yet
        if cycle_len == 0:
            # we're looking for same 3 rows: bottom one, top one, and half-way through: this means we potentialy have
            # 2 full cycles and 1st element of the 3rd one
            for start_index in range(top_rock_row_index // 2):
                mid_index = start_index + (top_rock_row_index - start_index) // 2
                if np.array_equal(cave[start_index], cave[top_rock_row_index]) and np.array_equal(cave[start_index], cave[mid_index]):
                    cycle_len = mid_index - start_index
                    cycle_height_start = top_rock_row_index
                    cycle_rock_index_start = rocks_counter
        elif cycle_rock_index_end == 0 and top_rock_row_index == cycle_height_start + cycle_len:
            cycle_rocks_delta = rocks_counter - cycle_rock_index_start
            remaining_rocks_count_cycles = (orig_rocks_limit - rocks_counter) // cycle_rocks_delta
            rocks_left = (orig_rocks_limit - rocks_counter) % cycle_rocks_delta
            assert orig_rocks_limit == rocks_counter + remaining_rocks_count_cycles * cycle_rocks_delta + rocks_left
            force_simulate = True
            rocks_counter += remaining_rocks_count_cycles * cycle_rocks_delta
    res = get_first_row_with_rock(cave)
    res += remaining_rocks_count_cycles * cycle_len
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
    res = run(lines[0], orig_rocks_limit=1000000000000)
    print(res)


def test() -> None:
    res = run(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>", orig_rocks_limit=1000000000000)
    assert res == 1514285714288


if __name__ == "__main__":
    test()
    main()
