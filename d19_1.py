import re
from enum import IntEnum
from typing import Iterator

import nographs as nog


class Resources(IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


# ore, clay, obsidian, geode
Status = tuple[int, int, int, int]


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
    for bid in range(1, len(blueprints) + 1):
        blueprint = blueprints[bid]
        max_res_per_turn = [max(blueprint[t][i] for t in Resources) for i in range(4)]
        resources: Status = (0, 0, 0, 0)
        robots: Status = (1, 0, 0, 0)

        def next_vertices(status: tuple[Status, Status], t) -> Iterator[tuple[tuple[Status, Status], int]]:
            if t.depth >= max_time:
                return
            res, bots = status
            new_res = tuple(res[i] + bots[i] for i in range(len(res)))
            # case: can build a robot
            for res_type in Resources.GEODE, Resources.OBSIDIAN, Resources.ORE, Resources.CLAY:
                if all(bot_cost <= res for bot_cost, res in zip(blueprint[res_type], res)):
                    # skip if making a new bot of this type doesn't make sense
                    if res_type < Resources.GEODE and bots[res_type] >= max_res_per_turn[res_type]:
                        continue
                    upd_bots = list(bots)
                    upd_bots[res_type] += 1
                    upd_res = list(new_res)
                    for i in range(4):
                        upd_res[i] -= blueprint[res_type][i]
                    yield (tuple(upd_res), tuple(upd_bots))

            # case: don't build a robot, just collect resources
            yield (new_res, bots)

        traversal = nog.TraversalDepthFirst(next_vertices).start_from((resources, robots))
        traversal.go_for_depth_range(max_time, max_time + 1)
        best = 0
        for vertex in traversal:
            if traversal.depth >= max_time and vertex[0][Resources.GEODE] > best:
                print(vertex, traversal.depth)
                best = vertex[0][Resources.GEODE]


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
