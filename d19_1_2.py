import re
from collections import namedtuple
from enum import IntEnum
from typing import Iterator


class Resources(IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


# ore, clay, obsidian, geode
Status = namedtuple("Status", ["ore", "clay", "obsidian", "geode"])
# resources status, bots status, time passed
World = namedtuple("World", ["resources", "bots", "time"])


def run(lines: list[str]) -> int:
    line_regexp = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    blueprints: dict[int, tuple[Status, Status, Status, Status]] = {}
    max_time = 24
    for line in lines:
        match = re.match(line_regexp, line)
        bprint = Status(
            (int(match.group(2)), 0, 0, 0),
            (int(match.group(3)), 0, 0, 0),
            (int(match.group(4)), int(match.group(5)), 0, 0),
            (int(match.group(6)), 0, int(match.group(7)), 0),
        )
        blueprints[int(match.group(1))] = bprint
    blueprint_qualities: dict[int, int] = {}
    for blueprint_id in range(1, len(blueprints) + 1):
        blueprint = blueprints[blueprint_id]
        max_res_per_turn = [max(blueprint[t][i] for t in Resources) for i in range(4)]
        max_res_per_turn[Resources.GEODE] = float("inf")
        resources: Status = Status(0, 0, 0, 0)
        robots: Status = Status(1, 0, 0, 0)

        def next_vertices(world: World) -> Iterator[World]:
            assert world.time < max_time
            new_res = Status(*(world.resources[i] + world.bots[i] for i in range(4)))

            # case: can build a robot
            is_any_bot_building_blocked = False
            for res_type in (Resources.CLAY, Resources.ORE, Resources.OBSIDIAN, Resources.GEODE):
                # we're already producing more than enough of this resource per turn
                if world.bots[res_type] >= max_res_per_turn[res_type]:
                    continue
                if all(bot_cost <= res for bot_cost, res in zip(blueprint[res_type], world.resources)):
                    # skip if making a new bot of this type doesn't make sense
                    # it doesn't make sense if we already produce enough resource fo specific kind per turn
                    # to build geode robot in 1 turn
                    upd_bots = list(world.bots)
                    upd_bots[res_type] += 1
                    upd_res = list(new_res)
                    for i in range(4):
                        upd_res[i] -= blueprint[res_type][i]
                    yield World(Status(*upd_res), Status(*upd_bots), world.time + 1)
                else:
                    is_any_bot_building_blocked = True

            # case: don't build a robot, just collect resources - but it only makes sense, if we don't have enough
            # resources to build robots; later we always want to build one, ideally geode one
            if is_any_bot_building_blocked:
                yield World(new_res, world.bots, world.time + 1)

        # gain function
        def heuristic(world: World) -> int:
            val = (
                    world.bots[Resources.GEODE] * 1000
                    + world.bots[Resources.OBSIDIAN] * 100
                    + world.bots[Resources.CLAY] * 10
                    + world.bots[Resources.ORE]
            )
            return val
            # best_val, best_ind = -1, -1
            # for si in range(len(to_check)):
            #    bots = to_check[si][0][1]
            #    missing_to_produce_geode_each_turn = [max(needed - have, 0) for have, needed in zip(bots, blueprint[Resources.GEODE])]

            #    sum_missing = sum(missing_to_produce_geode_each_turn)
            #    if best_ind == -1 or best_val > 0 >= sum_missing or (best_val == 0 and to_check[si][1] < zero_missing_best_time):
            #        best_val = sum_missing
            #        best_ind = si
            #        if best_val == 0:
            #            zero_missing_best_time = to_check[si][1]
            # selected_world = to_check[best_ind]
            # to_check = to_check[:best_ind] + to_check[best_ind + 1:]

        to_check: set[World] = {World(resources, robots, 0)}
        checked: set[World] = set()
        max_geodes = 0
        while len(to_check) > 0:
            # find best state to expand
            best_so_far = max(to_check, key=lambda w: heuristic(w))
            to_check.remove(best_so_far)
            checked.add(best_so_far)

            # trim the tree according to the current best known state
            to_remove: set[World] = set()
            # if there's a state that produced less resources in the same or more time, we can remove it
            for w in to_check:
                if w.time >= best_so_far.time and all(w.resources[i] < best_so_far.resources[i] for i in range(4)):
                    to_remove.add(w)
            to_check.difference_update(to_remove)

            # find next states
            next_worlds = set(next_vertices(best_so_far))
            end_time = next(iter(next_worlds)).time
            if next_worlds:
                print(f"Time: {end_time}")
                if end_time == max_time:
                    batch_max = max(w.resources[Resources.GEODE] for w in next_worlds)
                    if batch_max > max_geodes:
                        max_geodes = batch_max
                else:
                    next_worlds.difference_update(checked)
                    if next_worlds:
                        to_check.update(next_worlds)

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
