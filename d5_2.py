Stacks = dict[int, list[str]]


def parse_stacks(lines: list[str], no_stacks: int) -> tuple[Stacks, int]:
    line_no = 0
    while lines[line_no]:
        line_no += 1
    stacks: Stacks = {}
    for i in range(no_stacks):
        stacks[i + 1] = []
    for ln in range(line_no - 2, -1, -1):
        available = (len(lines[ln]) - 3) // 4 + 1
        for si in range(available):
            char = lines[ln][si * 4 + 1]
            if char != " ":
                stacks[si + 1].append(char)
    return stacks, line_no


def run(lines: list[str], no_stacks: int) -> str:
    stacks, break_line = parse_stacks(lines, no_stacks)
    for li in range(break_line + 1, len(lines)):
        count, from_s, to_s = [int(i) for i in lines[li].replace("move ", "").replace(" from", "").replace(" to", "").split(" ")]
        tmp = []
        for ci in range(count):
            tmp.append(stacks[from_s].pop())
        for ci in range(count):
            stacks[to_s].append(tmp.pop())
    res = ""
    for si in range(no_stacks):
        if stacks[si + 1]:
            res += stacks[si + 1].pop()
    return res


def main() -> None:
    with open("i5.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines, 9)
    print(res)


def test() -> None:
    lines = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""".splitlines()
    res = run(lines, 3)
    assert res == 'MCD'


if __name__ == "__main__":
    test()
    main()
