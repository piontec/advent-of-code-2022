from functools import cmp_to_key


def in_order(f: list, s: list) -> int:
    min_len = min(len(f), len(s))
    for i in range(min_len):
        l = f[i]
        r = s[i]
        if type(l) == int and type(r) == int:
            if l < r:
                return -1
            if l > r:
                return 1
        else:
            internal_f = l if type(l) == list else [l]
            internal_s = r if type(r) == list else [r]
            int_res = in_order(internal_f, internal_s)
            if int_res != 0:
                return int_res
    if len(f) == len(s):
        return 0
    return -1 if len(f) < len(s) else 1

def run(lines: list[str]) -> int:
    to_sort = [eval(l) for l in lines if l != ""]
    to_sort.append([[2]])
    to_sort.append([[6]])
    sorted_vals = sorted(to_sort, key=cmp_to_key(in_order), reverse=False)

    res = (sorted_vals.index([[2]]) + 1) * (sorted_vals.index([[6]]) + 1)
    return res
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
    assert run(lines) == 140


if __name__ == "__main__":
    test()
    main()
