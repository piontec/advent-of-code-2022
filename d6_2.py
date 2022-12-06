
def run(line: str) -> int:
    for ind in range (13, len(line)):
        s = set(line[ind - 13:ind + 1])
        if len(s) == 14:
            return ind + 1


def main() -> None:
    with open("i6.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines[0])
    print(res)


def test() -> None:
    assert run("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
    assert run("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
    assert run("nppdvjthqldpwncqszvftbrmjlhg") == 23
    assert run("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
    assert run("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26


if __name__ == "__main__":
    test()
    main()
