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
    rest = n
    base_5: list[int] = []
    while rest > 0:
        digit = rest % 5
        rest //= 5
        base_5.append(digit)
    res = ""
    i = 0
    while i < len(base_5):
        digit = base_5[i]
        if digit <= 2:
            res += str(digit)
        else: 
            if digit == 3:
                res += "="
            elif digit == 4:
                res += "-"
            elif digit == 5:
                res += "0"

            if i == len(base_5) - 1:
                base_5.append(1)
            else:
                base_5[i + 1] += 1
        i += 1
    rev_res = ""
    for i in range(len(res) - 1, -1, -1):
        rev_res += res[i]
    return rev_res

def run(lines: list[str]) -> str:
    sum_dec = sum(snafu_to_dec(l.strip()) for l in lines)
    res = dec_to_snafu(sum_dec)
    return res

def main() -> None:
    with open("i25.txt") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def test() -> None:
    assert snafu_to_dec("1=-0-2") == 1747
    assert snafu_to_dec("12111") == 906
    assert snafu_to_dec("2=0=") == 198
    assert snafu_to_dec("21") == 11
    assert snafu_to_dec("2=01") == 201
    assert snafu_to_dec("111") == 31
    assert snafu_to_dec("20012") == 1257

    assert dec_to_snafu(1747) == "1=-0-2"
    assert dec_to_snafu(906) == "12111"
    assert dec_to_snafu(198) == "2=0="
    assert dec_to_snafu(11) == "21"
    assert dec_to_snafu(201) == "2=01"
    assert dec_to_snafu(31) == "111"
    assert dec_to_snafu(1257) == "20012"

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
