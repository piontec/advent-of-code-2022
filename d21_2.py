from typing import Optional


class Node:
    def __init__(self, name: str, value: Optional[int] = None, op: Optional[str] = None) -> None:
        self.name = name
        self.left: Optional[str] = None
        self.right: Optional[str] = None
        self.val = value
        self.op = op

    def __repr__(self) -> str:
        return f"{self.name}"


def eval_rec(m: Node, monkeys: dict[str, Node]) -> int:
    if m.val:
        return m.val
    left_val = eval_rec(monkeys[m.left], monkeys)
    right_val = eval_rec(monkeys[m.right], monkeys)

    if m.op == "+":
        return left_val + right_val
    if m.op == "-":
        return left_val - right_val
    if m.op == "*":
        return left_val * right_val
    if m.op == "/":
        return left_val // right_val
    raise Exception("this shall not happen!")


def get_humn_root(monkeys: dict[str, Node]) -> list[str]:
    def search_node(m: Node) -> list[str]:
        if m.name == "humn":
            return ["humn"]
        for name in [m.left, m.right]:
            if name:
                path = search_node(monkeys[name])
                if path:
                    path.append(m.name)
                    return path
        return []

    return search_node(monkeys["root"])


def run(lines: list[str]) -> int:
    monkeys: dict[str, Node] = {}
    for line in lines:
        name, rest = line.split(":")
        rest_split = rest.split()
        if len(rest_split) == 1:
            monkeys[name] = Node(name, value=int(rest_split[0]))
        else:
            m = Node(name, op=rest_split[1])
            m.left = rest_split[0]
            m.right = rest_split[2]
            monkeys[name] = m

    humn_root_path = get_humn_root(monkeys)

    root = monkeys["root"]
    to_calc, to_eval = (root.left, root.right) if root.left in humn_root_path else (root.right, root.left)
    needed = eval_rec(monkeys[to_eval], monkeys)

    def calc_rec(mon: Node, n: int) -> int:
        if mon.name == "humn":
            return n
        if mon.val:
            raise Exception("This should not reach a value node")
        to_cal, to_eva, arg1_is_left = (mon.left, mon.right, False) if mon.left in humn_root_path else (
            mon.right, mon.left, True)
        arg1 = eval_rec(monkeys[to_eva], monkeys)
        if mon.op == "+":
            new_needed = n - arg1
        elif mon.op == "-":
            if arg1_is_left:
                new_needed = arg1 - n
            else:
                new_needed = arg1 + n
        elif mon.op == "*":
            new_needed = n // arg1
        elif mon.op == "/":
            if arg1_is_left:
                new_needed = arg1 // n
            else:
                new_needed = arg1 * n
        else:
            raise Exception("Unknown operand")
        return calc_rec(monkeys[to_cal], new_needed)

    res = calc_rec(monkeys[to_calc], needed)
    return res


def main() -> None:
    with open("i21.txt") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def test() -> None:
    res = run("""root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""".splitlines())
    assert res == 301


if __name__ == "__main__":
    test()
    main()
