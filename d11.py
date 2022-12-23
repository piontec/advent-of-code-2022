class Monkey:
    def __init__(self, lines: list[str]) -> None:
        self.id = int(lines[0].strip(":").split(" ")[1])
        items_str = lines[1].split(":")[1].strip()
        self.items = [int(i) for i in items_str.split(",")]
        op_line = lines[2].strip().split(" ")
        if op_line[5] == "old":
            self.op = (lambda x: x + x) if op_line[4] == "+" else (lambda x: x * x)
        else:
            op_arg = int(op_line[5])
            self.op = (lambda x: x + op_arg) if op_line[4] == "+" else (lambda x: x * op_arg)
        self.test = int(lines[3].strip().split(" ")[3])
        self.next_if_true = int(lines[4].strip().split(" ")[5])
        self.next_if_false = int(lines[5].strip().split(" ")[5])
        self.inspected = 0


def run(lines: list[str], rounds: int = 20, div: bool = True) -> int:
    monkeys: list[Monkey] = []
    mod_factor = 1
    for i in range(0, len(lines), 7):
        m = Monkey(lines[i:i + 6])
        mod_factor *= m.test
        monkeys.append(m)
    for _ in range(rounds):
        for mi in range(len(monkeys)):
            for item in monkeys[mi].items:
                new_item = monkeys[mi].op(item)
                if div:
                    new_item //= 3
                new_item %= mod_factor
                next_mi = monkeys[mi].next_if_true if new_item % monkeys[mi].test == 0 else monkeys[mi].next_if_false
                monkeys[next_mi].items.append(new_item)
                monkeys[mi].inspected += 1
            monkeys[mi].items.clear()
    monkeys.sort(key=lambda m: m.inspected, reverse=True)
    res = monkeys[0].inspected * monkeys[1].inspected
    return res


def main() -> None:
    with open("i11.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)
    res = run(lines, rounds=10000, div=False)
    print(res)


def test() -> None:
    lines = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".splitlines()
    assert run(lines) == 10605
    assert run(lines, rounds=10000, div=False) == 2713310158


if __name__ == "__main__":
    test()
    main()
