def in_order(f: list, s: list) -> str:
    min_len = min(len(f), len(s))
    for i in range(min_len):
        l = f[i]
        r = s[i]
        if type(l) == int and type(r) == int:
            if l < r:
                return "f"
            if l > r:
                return "s"
        else:
            internal_f = l if type(l) == list else [l]
            internal_s = r if type(r) == list else [r]
            int_res = in_order(internal_f, internal_s)
            if int_res != "e":
                return int_res
    if len(f) == len(s):
        return "e"
    return "f" if len(f) < len(s) else "s"

def run(lines: list[str]) -> int:
    ind_sum = 0
    for pi in range(0, len(lines), 3):
        first = eval(lines[pi])
        second = eval(lines[pi + 1])
        if in_order(first, second) == "f":
            ind = (pi // 3) + 1
            ind_sum += ind
    return ind_sum
def main() -> None:
    with open("i13.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


def test() -> None:
    lines = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".splitlines()
    assert run(lines) == 13


if __name__ == "__main__":
    test()
    main()
