from collections import namedtuple
import re
from enum import IntEnum
from typing import Iterator
import math

# X, Y
Pos = tuple[int, int]
# blizzard_pos, blizzard_type
Blizzard = tuple[Pos, str]
Blizzards = list[Blizzard]

State = namedtuple('State', ['pos', 't'])

moves = (0, 0), (-1, 0), (0, -1), (1, 0), (0, 1)

def run(lines: list[str]) -> int:
    size = len(lines[0].strip()), len(lines)

    # parse entry
    start_point = lines[0].find("."), 0
    # parse exit
    exit_point = lines[size[1] - 1].find("."), size[1] - 1
    # parse the rest
    starting_blizzards: Blizzards = []
    for li in range(1, size[1] - 1):
        line = lines[li].strip()
        for ci in range(1, len(line) - 1):
           if line[ci] != ".":
               starting_blizzards.append(((ci, li), line[ci]))
    timed_blizzards: dict[int, Blizzards] = {0: starting_blizzards}

    def get_blizzards_in_time(minute: int) -> Blizzards:
        if minute in timed_blizzards:
            return timed_blizzards[minute]
        previous = get_blizzards_in_time(minute - 1)
        new_blizzards: Blizzards = []

        for bliz in previous:
            bliz_loc, bliz_type = bliz
            if bliz_type == ">":
                new_x, new_y = bliz_loc[0] + 1, bliz_loc[1]
                if new_x >= size[0] - 1:
                    new_x = 1
            elif bliz_type == "v":
                new_x, new_y = bliz_loc[0], bliz_loc[1] + 1
                if new_y >= size[1] - 1:
                    new_y = 1
            elif bliz_type == "<":
                new_x, new_y = bliz_loc[0] - 1, bliz_loc[1]
                if new_x == 0:
                    new_x = size[0] - 2
            elif bliz_type == "^":
                new_x, new_y = bliz_loc[0], bliz_loc[1] - 1
                if new_y == 0:
                    new_y = size[1] - 2
            new_bliz = (new_x, new_y), bliz_type
            new_blizzards.append(new_bliz)

        timed_blizzards[minute] = new_blizzards
        return new_blizzards
            


    def heuristic(vertex: Pos, exit: Pos) -> float:
        return math.dist(vertex, exit)

    # gets vertex, returns iterable of vertex, distance
    def next_edges(vertex: Pos, t: int, start: Pos, exit: Pos) -> Iterator[State]:
        new_t = t + 1
        blizzards = get_blizzards_in_time(new_t)
        for move in moves:
            new_pos = vertex[0] + move[0], vertex[1] + move[1]
            if new_pos == start or new_pos == exit:
                yield State(new_pos, new_t)
            # check if we don't go into a wall
            if new_pos[0] < 1 or new_pos[1] < 1 or new_pos[0] > size[0] - 2 or new_pos[1] > size[1] - 2:
                continue
            # check if we don't go into a blizzard
            collision = False
            for b in blizzards:
                if b[0] == new_pos:
                   collision = True
                   break
            if collision:
                continue
           
            yield State(new_pos, new_t)

    start_time = 0
    for points in ((start_point, exit_point), (exit_point, start_point), (start_point, exit_point)):
        start, exit = points
        start_state = State(start, start_time)
        states: set[State] = {start_state}
        best_time = math.inf
        checked_states: set[State] = {start_state}
        while len(states) > 0:
            # choose best state to evaluate
            best_state = min(states, key=lambda s: heuristic(s.pos, exit))
            states.remove(best_state)
            checked_states.add(best_state)
            # expand it
            next_states = set(next_edges(best_state.pos, best_state.t, start, exit))
            found = set(filter(lambda s: s.pos == exit, next_states))
            if found:
                best_time = min(best_time, min(found, key=lambda s: s.t).t)
                next_states.difference_update(found)
            next_states.difference_update(checked_states) 
            states.update(next_states)
            # prune set
            worse_states = list(filter(lambda s: s.t > best_time, states))
            states.difference_update(worse_states)
        start_time = best_time
    return start_time


def main() -> None:
    with open("i24.txt", "r") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def test() -> None:
    res = run("""#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""".splitlines())
    assert res == 54


if __name__ == "__main__":
    test()
    main()
