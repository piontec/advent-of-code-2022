import re
from enum import IntEnum
from typing import Iterator


class Resources(IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


# ore, clay, obsidian, geode
Status = tuple[int, int, int, int]
# resources status, bots status, time passed
World = tuple[tuple[Status, Status], int]


def run(lines: list[str]) -> int:
    line_regexp = r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'
    blueprints: dict[int, tuple[Status, Status, Status, Status]] = {}
    max_time = 24
    for line in lines:
        match = re.match(line_regexp, line)
        bprint = (
            (int(match.group(2)), 0, 0, 0),
            (int(match.group(3)), 0, 0, 0),
            (int(match.group(4)), int(match.group(5)), 0, 0),
            (int(match.group(6)), 0, int(match.group(7)), 0),
        )
        blueprints[int(match.group(1))] = bprint
    blueprint_qualities: dict[int, int] = {}
    for bid in range(1, len(blueprints) + 1):
        blueprint = blueprints[bid]
        max_res_per_turn = [max(blueprint[t][i] for t in Resources) for i in range(4)]
        resources: Status = (0, 0, 0, 0)
        robots: Status = (1, 0, 0, 0)

        def next_vertices(world: World) -> Iterator[World]:
            time = world[1]
            if time >= max_time:
                return
            res, bots = world[0]
            new_res = tuple(res[i] + bots[i] for i in range(len(res)))
            # case: can build a robot
            is_any_bot_building_blocked = False
            for res_type in Resources.CLAY, Resources.ORE, Resources.OBSIDIAN, Resources.GEODE:
                if all(bot_cost <= res for bot_cost, res in zip(blueprint[res_type], res)):
                    # skip if making a new bot of this type doesn't make sense
                    # it doesn't make sense if we already produce enough resource fo specific kind per turn
                    # to build geode robot in 1 turn
                    if res_type < Resources.GEODE and bots[res_type] >= max_res_per_turn[res_type]:
                        continue
                    upd_bots = list(bots)
                    upd_bots[res_type] += 1
                    upd_res = list(new_res)
                    for i in range(4):
                        upd_res[i] -= blueprint[res_type][i]
                    yield (tuple(upd_res), tuple(upd_bots)), time + 1
                else:
                    is_any_bot_building_blocked = True

            # case: don't build a robot, just collect resources - but it only makes sense, if we don't have enough
            # resources to build robots; later we always want to build one, ideally geode one
            if is_any_bot_building_blocked:
                yield (new_res, bots), time + 1

        to_check: list[World] = [((resources, robots), 0)]
        max_geodes = 0
        zero_missing_best_time = 25
        while len(to_check) > 0:
            # world_now = to_check.pop()
            # find best state to expand
            best_val, best_ind = -1, -1
            for si in range(len(to_check)):
                bots = to_check[si][0][1]
                missing_to_produce_geode_each_turn = [max(needed - have, 0) for have, needed in zip(bots, blueprint[Resources.GEODE])]
                sum_missing = sum(missing_to_produce_geode_each_turn)
                if best_ind == -1 or best_val > 0 >= sum_missing or (best_val == 0 and to_check[si][1] < zero_missing_best_time):
                    best_val = sum_missing
                    best_ind = si
                    if best_val == 0:
                        zero_missing_best_time = to_check[si][1]
            selected_world = to_check[best_ind]
            to_check = to_check[:best_ind] + to_check[best_ind + 1:]

            # trim the tree according to the current best known state
            ind_to_remove: list[int] = []
            for si in range(len(to_check)):
                w = to_check[si]
                if w[1] >= selected_world[1] and all(w[0][1][i] < selected_world[0][1][i] for i in range(4)):
                    ind_to_remove.append(si)
            if ind_to_remove:
                new_to_check = []
                for si in range(len(to_check)):
                    if si not in ind_to_remove:
                        new_to_check.append(to_check[si])
                to_check = new_to_check

            # find next states
            next_worlds = list(next_vertices(selected_world))
            if next_worlds:
                print(f"Time: {next_worlds[0][1]}")
                if next_worlds[0][1] == max_time:
                    batch_max = max(w[0][1][Resources.GEODE] for w in next_worlds)
                    if batch_max > max_geodes:
                        max_geodes = batch_max
                else:
                    to_check.extend(next_worlds)
        blueprint_qualities[bid] = bid * max_geodes
    total = sum(blueprint_qualities.values())
    return total


def main() -> None:
    with open("i19.txt", "r") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def test() -> None:
    res = run("""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian. 
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""".splitlines())
    assert res == 33


if __name__ == "__main__":
    test()
    main()
