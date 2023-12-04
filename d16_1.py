from collections import namedtuple
from dataclasses import dataclass
from time import perf_counter


@dataclass
class Valve:
    label: str
    flow: int
    next_valves: list[str]


State = namedtuple("State", ['node', 'remaining_time', 'sum_flow'])


def all_shortest_paths(valves: dict[str, Valve]) -> dict[str, dict[str, int]]:
    inf = len(valves) + 1
    res = {ls: {dl: inf for dl in valves.keys()} for ls in valves.keys()}

    for vl in valves.keys():
        res[vl][vl] = 0
        for dl in valves[vl].next_valves:
            res[vl][dl] = 1

    for k in valves.keys():
        for i in valves.keys():
            for j in valves.keys():
                if res[i][j] > res[i][k] + res[k][j]:
                    res[i][j] = res[i][k] + res[k][j]

    return res


def run(lines: list[str], max_time: int = 30) -> int:
    valves: dict[str, Valve] = {}
    for line in lines:
        tmp = line.split(" ")
        label = tmp[1]
        flow = int(tmp[4].split("=")[1].strip(";"))
        nxt = [n.strip(",") for n in tmp[9:]]
        v = Valve(label, flow, list(nxt))
        valves[label] = v
    shortest_paths = all_shortest_paths(valves)
    # filter out zero flow nodes
    for k, v in valves.items():
        valves[k].next_valves = [v for v in valves[k].next_valves if valves[v].flow > 0]
    valves = {k: v for k, v in valves.items() if v.flow > 0 or k == "AA"}
    valve_names = list(valves.keys())
    flags = {v: 1 << flag for flag, v in enumerate(valves.keys())}

    to_check = {flags["AA"]: State("AA", max_time, 0)}
    final_states: dict[int, int] = {}
    while to_check:
        visited, state = to_check.popitem()
        for v in valve_names:
            if v == state.node:
                continue
            # we are note able to open this valve anymore
            if state.remaining_time <= shortest_paths[state.node][v] + 1:
                if visited in final_states:
                    final_states[visited] = max(final_states[visited], state.sum_flow)
                else:
                    final_states[visited] = state.sum_flow
                continue
            # we already opened this valve
            if visited & flags[v]:
                continue
            new_visited = visited | flags[v]
            new_time = state.remaining_time - shortest_paths[state.node][v] - 1
            new_flow = state.sum_flow + valves[v].flow * new_time
            new_state = State(v, new_time, new_flow)
            if new_visited in to_check:
                if to_check[new_visited].sum_flow < new_flow:
                    if to_check[new_visited].remaining_time <= new_time:
                        to_check[new_visited] = new_state
                    else:
                        raise Exception("This should not happen")
            else:
                to_check[new_visited] = new_state
    return max(final_states.values())


def main() -> None:
    t1 = perf_counter()
    with open("i16.txt") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)
    print(f"Main time: {perf_counter() - t1}")


def test() -> None:
    lines = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".splitlines()
    assert run(lines) == 1651


if __name__ == "__main__":
    test()
    main()
