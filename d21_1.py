from typing import Optional


class Node:
    def __init__(self, value: Optional[int] = None, op: Optional[str] = None) -> None:
        self.left: Optional[str] = None
        self.right: Optional[str] = None
        self.val = value
        self.op = op

    def __repr__(self) -> str:
        return f"{self.val}"


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


def run(lines: list[str]) -> int:
    monkeys: dict[str, Node] = {}
    for line in lines:
        name, rest = line.split(":")
        rest_split = rest.split()
        if len(rest_split) == 1:
            monkeys[name] = Node(value=int(rest_split[0]))
        else:
            m = Node(op=rest_split[1])
            m.left = rest_split[0]
            m.right = rest_split[2]
            monkeys[name] = m
    res = eval_rec(monkeys["root"], monkeys)
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
    assert res == 152


if __name__ == "__main__":
    test()
    main()
