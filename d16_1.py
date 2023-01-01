from dataclasses import dataclass
from queue import Queue


@dataclass
class Valve:
    label: str
    flow: int
    next_valves: list[str]


@dataclass
class State:
    current_loc: str
    released: int
    opened: list[str]
    time_passed: int


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

def next_states(s: State, valves: dict[str, Valve], shortest: dict[str, dict[str, int]]) -> list[State]:
    ns: list[State] = []
    flow_delta_per_sec = sum(v.flow for v in [valves[vl] for vl in s.opened])
    released = s.released
    new_opened = s.opened.copy()
    time = s.time_passed
    assert time < 30

    # if only we can, we use 1 sec of time to open local valve
    if s.current_loc not in s.opened and valves[s.current_loc].flow > 0:
        new_opened.append(s.current_loc)
        time += 1
        released += flow_delta_per_sec
        flow_delta_per_sec += valves[s.current_loc].flow

    not_opened = [k for k in valves.keys() if k not in new_opened and valves[k].flow > 0]
    if len(not_opened) > 0:
        for nvl in not_opened:
            time_delta = shortest[s.current_loc][nvl]
            if time + time_delta > 30:
                time_delta = 30 - time
            ns.append(State(nvl, released + flow_delta_per_sec * time_delta, new_opened, time + time_delta))
    else:
        time_left = 30 - time
        ns.append(State(s.current_loc, released + time_left * flow_delta_per_sec, new_opened, 30))
    return ns


def run(lines: list[str]) -> int:
    valves: dict[str, Valve] = {}
    for line in lines:
        tmp = line.split(" ")
        label = tmp[1]
        flow = int(tmp[4].split("=")[1].strip(";"))
        nxt = [n.strip(",") for n in tmp[9:]]
        v = Valve(label, flow, list(nxt))
        valves[label] = v
    state = State("AA", 0, [], 0)
    shortest_paths = all_shortest_paths(valves)
    best = state
    q = Queue()
    q.put(state)
    while len(q.queue) > 0:
        s = q.get()
        for ns in next_states(s, valves, shortest_paths):
            if ns.time_passed == 30:
                if ns.released > best.released:
                    best = ns
            else:
                found_better = False
                for qs in q.queue:
                    if qs.current_loc == ns.current_loc and set(qs.opened) == set(ns.opened) and qs.released > ns.released and \
                            qs.time_passed <= ns.time_passed:
                        found_better = True
                        break
                if not found_better:
                    q.put(ns)
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
    assert run(lines) == 1651


if __name__ == "__main__":
    test()
    main()
