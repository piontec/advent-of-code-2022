from dataclasses import dataclass, field
from functools import cache
from queue import PriorityQueue
from typing import Tuple


@dataclass
class Valve:
    label: str
    flow: int
    next_valves: list[str]


@dataclass(order=True, frozen=True)
class State:
    # current_loc(mine, elephant)
    current_loc: tuple[str, str] = field(compare=False)
    target_loc: tuple[str, str] = field(compare=False)
    released: int
    opened: frozenset[str] = field(compare=False)
    time_passed: int = field(compare=False)

    # def __hash__(self) -> int:
    #     op_str = list(self.opened).sort()
    #     return hash(self.current_loc) + hash(self.target_loc) + hash(self.released) + hash(op_str) + hash(
    #         self.time_passed)


@dataclass(frozen=True)
class FlowState:
    current_locs: frozenset[str]
    opened: frozenset[str]

    # def __hash__(self) -> int:
    #     cl_str = list(self.current_locs).sort()
    #     op_str = list(self.opened).sort()
    #     return hash(cl_str) + hash(op_str)


def all_shortest_paths(vlvs: dict[str, Valve]) -> Tuple[dict[str, dict[str, int]], dict[str, dict[str, str]]]:
    inf = len(vlvs) + 1
    res = {ls: {dl: inf for dl in vlvs.keys()} for ls in vlvs.keys()}
    next_valve = {ls: {dl: "" for dl in vlvs.keys()} for ls in vlvs.keys()}

    for vl in vlvs.keys():
        res[vl][vl] = 0
        next_valve[vl][vl] = vl
        for dl in vlvs[vl].next_valves:
            res[vl][dl] = 1
            next_valve[vl][dl] = dl

    for k in vlvs.keys():
        for i in vlvs.keys():
            for j in vlvs.keys():
                if res[i][j] > res[i][k] + res[k][j]:
                    res[i][j] = res[i][k] + res[k][j]
                    next_valve[i][j] = next_valve[i][k]

    return res, next_valve


valves: dict[str, Valve] = {}
next_valves: dict[str, dict[str, str]] = {}


# @cache
def next_states(s: State, max_time: int = 26) -> list[State]:
    global valves
    global next_valves
    flow_delta_per_sec = sum(v.flow for v in [valves[vl] for vl in s.opened])
    released = s.released + flow_delta_per_sec
    assert s.time_passed < max_time
    time = s.time_passed + 1
    next_positions: tuple[list[tuple[str, str]], list[tuple[str, str]]] = ([], [])
    new_opened = s.opened.copy()

    for i in range(2):
        # we only consider actions possible in 1 unit of time
        cur = s.current_loc[i]
        assert cur != ''
        tgt = s.target_loc[i]
        assert tgt != ''
        if cur != tgt:
            assert (next_valves[cur][tgt], tgt) != ("", "")
            next_positions[i].append((next_valves[cur][tgt], tgt))
        # if only we can, we use 1 sec of time to open local valve
        elif cur not in s.opened and valves[cur].flow > 0:
            new_opened = s.opened | {cur}
            flow_delta_per_sec += valves[cur].flow
            assert (cur, tgt) != ("", "")
            next_positions[i].append((cur, tgt))
        else:
            not_opened = [k for k in valves.keys() if k not in new_opened and valves[k].flow > 0]
            if len(not_opened) == 0:
                total_released = released + (max_time - time) * flow_delta_per_sec
                assert s.current_loc != ("", "")
                return [State(s.current_loc, s.target_loc, total_released, new_opened, max_time)]
            for nvl in not_opened:
                assert (next_valves[cur][nvl], nvl) != ("", "")
                next_positions[i].append((next_valves[cur][nvl], nvl))
    ns: list[State] = []
    for my_index in range(len(next_positions[0])):
        for el_index in range(len(next_positions[1])):
            if next_positions[0][my_index][1] == next_positions[1][el_index][1]:
                continue
            new_locs = (next_positions[0][my_index][0], next_positions[1][el_index][0])
            assert new_locs != ('', '')
            new_tgts = (next_positions[0][my_index][1], next_positions[1][el_index][1])
            ns.append(State(new_locs, new_tgts, released, new_opened, time))
    return ns


def run(lines: list[str], max_time: int = 26) -> int:
    global valves
    global next_valves
    valves = {}
    next_valves = {}
    for line in lines:
        tmp = line.split(" ")
        label = tmp[1]
        flow = int(tmp[4].split("=")[1].strip(";"))
        nxt = [n.strip(",") for n in tmp[9:]]
        v = Valve(label, flow, list(nxt))
        valves[label] = v
    state = State(("AA", "AA"), ("AA", "AA"), 0, frozenset(), 0)
    shortest_paths, next_valves = all_shortest_paths(valves)
    best_flowstates: dict[FlowState, tuple[int, int]] = {}
    best = state
    q = PriorityQueue()
    q.put((state.released * -1, state))
    max_flow = sum(valves[v].flow for v in valves.keys())

    while len(q.queue) > 0:
        _, s = q.get()
        for ns in next_states(s, max_time=max_time):
            if ns.time_passed == max_time:
                if ns.released > best.released:
                    best = ns
            else:
                new_poss = frozenset((ns.current_loc[0], ns.current_loc[1]))
                flow_state = FlowState(new_poss, ns.opened)
                if flow_state in best_flowstates and best_flowstates[flow_state][0] > ns.released and \
                        best_flowstates[flow_state][1] <= ns.time_passed:
                    continue
                best_flowstates[flow_state] = (ns.released, ns.time_passed)

                unopened = [v for v in valves.keys() if v not in ns.opened and valves[v].flow > 0]
                closest_unopened_valve = min(shortest_paths[ns.current_loc[i]][v] for v in unopened for i in (0, 1))
                upper_release_left_bound = (max_time - ns.time_passed - closest_unopened_valve) * max_flow
                if ns.released + upper_release_left_bound < best.released:
                    continue

                q.put((ns.released * -1, ns))
    return best.released


def main() -> None:
    with open("i16.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


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
    assert run(lines) == 1706


if __name__ == "__main__":
    test()
    main()
