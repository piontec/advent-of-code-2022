import re
from enum import IntEnum
from time import perf_counter
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


def run(lines: list[str]) -> list[int]:
    line_regexp = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    blueprints: dict[int, npt.NDArray[np.uint]] = {}
    max_time = 32
    for line in lines:
        match = re.match(line_regexp, line)
        bprint = np.array([
            (int(match.group(2)), 0, 0, 0),
            (int(match.group(3)), 0, 0, 0),
            (int(match.group(4)), int(match.group(5)), 0, 0),
            (int(match.group(6)), 0, int(match.group(7)), 0)], dtype=np.ubyte
        )
        bid = int(match.group(1))
        blueprints[bid] = bprint
        if bid >= 3:
            break

    blueprint_qualities: list[int] = []
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

        to_check: dict[bytes, World] = {current_world.tobytes(): current_world}
        checked: set[bytes] = set()
        max_geodes = 0
        current_world = None
        current_world_hash = None
        while len(to_check) > 0:
            # current_world = to_check.pop()
            # use max heuristic to find the best value in the to_check dict
            cwh = -1
            for k, w in to_check.items():
                if cwh == -1:
                    current_world = w
                    cwh = heuristic(w)
                    current_world_hash = k
                    continue
                wh = heuristic(w)
                if wh > cwh:
                    current_world = w
                    cwh = wh
                    current_world_hash = k
            del to_check[current_world_hash]
            checked.add(current_world_hash)

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
                        print( f"BID {blueprint_id} got new best: {max_geodes}; [{nw[W_TIME_INDEX]}], res: {nw[W_RES_SLICE]}, bots: {nw[W_BOTS_SLICE]}, to_check: {len(to_check)}, checked: {len(checked)}")
                else:
                    nw_hash = nw.tobytes()
                    if nw_hash in checked:
                        continue
                    to_check[nw_hash] = nw

        blueprint_qualities.append(max_geodes)
        print(f"BID {blueprint_id} got: {max_geodes}")
    return blueprint_qualities


def main() -> None:
    with open("i19.txt", "r") as i:
        lines = i.readlines()
    res = run(lines)
    print(res[0] * res[1] * res[2])


def test() -> None:
    res = run(
        """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian. 
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""".splitlines()
    )
    assert res[0] == 56
    assert res[1] == 62


if __name__ == "__main__":
    # t1 = perf_counter()
    # test()
    # print(f"Time: {perf_counter() - t1}")
    main()
