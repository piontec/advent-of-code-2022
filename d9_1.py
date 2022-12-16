def run(lines: list[str]) -> int:
    h = (0, 0)
    t = (0, 0)
    t_pos = {(0, 0)}
    for line in lines:
        move, cnt = line.split(" ")
        count = int(cnt)
        for c in range(count):
            if move == "U":
                h = (h[0], h[1] + 1)
            elif move == "D":
                h = (h[0], h[1] - 1)
            elif move == "R":
                h = (h[0] + 1, h[1])
            elif move == "L":
                h = (h[0] - 1, h[1])
            else:
                raise Exception("wrong move")
            if abs(t[0] - h[0]) > 1 or abs(t[1] - h[1]) > 1:
                if t[0] == h[0]:
                    t = (t[0], t[1] + (1 if h[1] > t[1] else -1))
                elif t[1] == h[1]:
                    t = (t[0] + (1 if h[0] > t[0] else -1), t[1])
                elif abs(h[0] - t[0]) == 2:
                    t = ((h[0] + 1) if t[0] > h[0] else (h[0] - 1), h[1])
                elif abs(h[1] - t[1]) == 2:
                    t = (h[0], (h[1] + 1) if t[1] > h[1] else (h[1] - 1))
                t_pos.add(t)
    return len(t_pos)



def main() -> None:
    with open("i9.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


def test() -> None:
    lines = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".splitlines()
    assert run(lines) == 13


if __name__ == "__main__":
    test()
    main()
