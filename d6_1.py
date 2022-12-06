
def run(line: str) -> int:
    for ind in range (3, len(line)):
        s = set(line[ind - 3:ind + 1])
        if len(s) == 4:
            return ind + 1


def main() -> None:
    with open("i6.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines[0])
    print(res)


def test() -> None:
    assert run("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert run("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert run("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert run("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11


if __name__ == "__main__":
    test()
    main()
