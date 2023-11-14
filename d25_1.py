def snafu_to_dec(snafu: str) -> int:
    n = 0
    for i in range(0, len(snafu)):
        snafu_dig = snafu[len(snafu) - i - 1]
        if snafu_dig == "=":
            n += -2 * 5 ** i
        elif snafu_dig == "-":
            n += -1 * 5 ** i
        elif snafu_dig == "1":
            n += 1 * 5 ** i
        if snafu_dig == "2":
            n += 2 * 5 ** i
    return n

def dec_to_snafu(n: int) -> str:
    max_pow = 0
    rest = n
    while True:
        rest = n // 5 ** max_pow
        if rest < 5:
            break
        max_pow += 1
    base_5: list[int] = []
    while max_pow >= 0:
        digit = n // 5 ** max_pow
        n -= digit * 5 ** max_pow
        max_pow -= 1
        base_5.append(digit)
    base_5_str = 
    print(f"base_5: {".join(base_5)}")
    base_5_rev: list[int] = []
    for i in range(len(base_5) -1, -1, -1):
        base_5_rev.append(base_5[i])
    res = ""
    for i in range(len(base_5_rev)):
        if base_5_rev[i] <= 2:
            res += str(base_5_rev[i])
        else: 
            if base_5_rev[i] == 3:
                res += "="
            if base_5_rev[i] == 4:
                res += "-"
            if i == len(base_5_rev) - 1:
                base_5_rev.append(1)
            else:
                base_5_rev[i + 1] += 1
    rev_res = ""
    for i in range(len(res) - 1, -1, -1):
        rev_res += res[i]
    return rev_res

def run(lines: list[str]) -> str:
    sum_dec = sum(snafu_to_dec(l.strip()) for l in lines)
    print(f"dec sum: {sum_dec}")
    res = dec_to_snafu(sum_dec)
    return res

def main() -> None:
    with open("i25.txt") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)
    print(snafu_to_dec("2=-----11--01=-100"))


def test() -> None:
    res = run("""1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
""".splitlines())
    assert res == "2=-1=0"


if __name__ == "__main__":
    test()
    main()
