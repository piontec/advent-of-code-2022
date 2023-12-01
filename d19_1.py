import re
from collections import deque
from enum import IntEnum
from queue import LifoQueue
from typing import Iterator

import numpy as np
import numpy.typing as npt


class Resources(IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


# ore, clay, obsidian, geode
Status = npt.NDArray[np.ubyte]
# resources status, bots status, time passed
World = npt.NDArray[np.ubyte]
W_RES_SLICE = slice(0, 4)
W_BOTS_SLICE = slice(4, 8)
W_TIME_INDEX = 8


def run(lines: list[str]) -> int:
    line_regexp = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    blueprints: dict[int, npt.NDArray[np.uint]] = {}
    max_time = 24
    for line in lines:
        match = re.match(line_regexp, line)
        bprint = np.array([
            (int(match.group(2)), 0, 0, 0),
            (int(match.group(3)), 0, 0, 0),
            (int(match.group(4)), int(match.group(5)), 0, 0),
            (int(match.group(6)), 0, int(match.group(7)), 0)], dtype=np.ubyte
        )
        blueprints[int(match.group(1))] = bprint
    blueprint_qualities: dict[int, int] = {}
    for blueprint_id in range(1, len(blueprints) + 1):
        blueprint = blueprints[blueprint_id]
        max_res_per_turn = np.maximum.reduce([blueprint[t] for t in Resources])
        max_res_per_turn[Resources.GEODE] = 255
        current_world = np.zeros(9, dtype=np.ubyte)
        current_world[4] = 1

        def next_vertices(world: World) -> Iterator[World]:
            assert world[W_TIME_INDEX] < max_time
            new_res = world[W_RES_SLICE] + world[W_BOTS_SLICE]

            # case: can build a robot
            is_any_bot_building_blocked = False
            for bot_type in (Resources.CLAY, Resources.ORE, Resources.OBSIDIAN, Resources.GEODE):
                # we're already producing more than enough of this resource per turn
                if world[W_BOTS_SLICE][bot_type] >= max_res_per_turn[bot_type]:
                    continue
                if np.less_equal(blueprint[bot_type], world[W_RES_SLICE]).all():
                    # skip if making a new bot of this type doesn't make sense
                    # it doesn't make sense if we already produce enough resource fo specific kind per turn
                    # to build geode robot in 1 turn
                    upd_bots = world[W_BOTS_SLICE].copy()
                    upd_bots[bot_type] += 1
                    upd_res = new_res.copy()
                    upd_res -= blueprint[bot_type]
                    yield np.concatenate((upd_res, upd_bots, [world[W_TIME_INDEX] + 1]))
                else:
                    is_any_bot_building_blocked = True

            # case: don't build a robot, just collect resources - but it only makes sense, if we don't have enough
            # resources to build robots; later we always want to build one, ideally geode one
            if is_any_bot_building_blocked:
                yield np.concatenate((new_res, world[W_BOTS_SLICE], [world[W_TIME_INDEX] + 1]))

        # gain function
        def heuristic(world: World) -> int:
            val = (
                    world[W_BOTS_SLICE][Resources.GEODE] * 1000
                    + world[W_BOTS_SLICE][Resources.OBSIDIAN] * 100
                    + world[W_BOTS_SLICE][Resources.CLAY] * 10
                    + world[W_BOTS_SLICE][Resources.ORE]
            )
            return val

        #    # best_val, best_ind = -1, -1
        #    # for si in range(len(to_check)):
        #    #    bots = to_check[si][0][1]
        #    #    missing_to_produce_geode_each_turn = [max(needed - have, 0) for have, needed in zip(bots, blueprint[Resources.GEODE])]

        #    #    sum_missing = sum(missing_to_produce_geode_each_turn)
        #    #    if best_ind == -1 or best_val > 0 >= sum_missing or (best_val == 0 and to_check[si][1] < zero_missing_best_time):
        #    #        best_val = sum_missing
        #    #        best_ind = si
        #    #        if best_val == 0:
        #    #            zero_missing_best_time = to_check[si][1]
        #    # selected_world = to_check[best_ind]
        #    # to_check = to_check[:best_ind] + to_check[best_ind + 1:]

        to_check = deque([current_world])
        checked: set[bytes] = set()
        max_geodes = 0
        while len(to_check) > 0:
            # current_world = to_check.pop()
            # use max heuristic to find the best value in the queue
            current_world = max(to_check, key=heuristic)
            to_check.remove(current_world)
            checked.add(current_world.tobytes())

            # check if we can ignore this state
            # ignore if we can't produce more geodes even in the best case scenario
            time_left = max_time - current_world[W_TIME_INDEX]
            cur_geode_bots = current_world[W_BOTS_SLICE][Resources.GEODE]
            max_geode_bots = cur_geode_bots + time_left
            our_best = current_world[W_RES_SLICE][Resources.GEODE] + (cur_geode_bots + max_geode_bots) / 2 * time_left
            if our_best < max_geodes:
                continue
            # TODO: if there's a state that produced less resources in the same or more time, we can remove it

            # find next states
            for nw in next_vertices(current_world):
                if nw[W_TIME_INDEX] == max_time:
                    if nw[W_RES_SLICE][Resources.GEODE] > max_geodes:
                        max_geodes = nw[W_RES_SLICE][Resources.GEODE]
                        print(
                            f"Got new best: {max_geodes}; [{nw[W_TIME_INDEX]}], res: {nw[W_RES_SLICE]}, bots: {nw[W_BOTS_SLICE]}")
                else:
                    nw_bytes = nw.tobytes()
                    if nw_bytes in checked:
                        continue
                    to_check.append(nw)

        blueprint_qualities[blueprint_id] = blueprint_id * max_geodes
    total = sum(blueprint_qualities.values())
    return total


def main() -> None:
    with open("i19.txt", "r") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def test() -> None:
    res = run(
        """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian. 
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""".splitlines()
    )
    assert res == 33


if __name__ == "__main__":
    test()
    main()
