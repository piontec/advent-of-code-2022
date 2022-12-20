def run(lines: list[str]) -> int:
    snake: list[tuple[int, int]] = []
    for _ in range(10):
        snake.append((0, 0))
    t_pos = {(0, 0)}
    for line in lines:
        move, cnt = line.split(" ")
        count = int(cnt)
        for c in range(count):
            if move == "U":
                snake[0] = (snake[0][0], snake[0][1] + 1)
            elif move == "D":
                snake[0] = (snake[0][0], snake[0][1] - 1)
            elif move == "R":
                snake[0] = (snake[0][0] + 1, snake[0][1])
            elif move == "L":
                snake[0] = (snake[0][0] - 1, snake[0][1])
            else:
                raise Exception("wrong move")
            for i in range(1, 10):
                if abs(snake[i][0] - snake[i-1][0]) > 1 or abs(snake[i][1] - snake[i-1][1]) > 1:
                    # equal x
                    if snake[i][0] == snake[i-1][0]:
                        snake[i] = (snake[i][0], snake[i][1] + (1 if snake[i-1][1] > snake[i][1] else -1))
                    # equal y
                    elif snake[i][1] == snake[i-1][1]:
                        snake[i] = (snake[i][0] + (1 if snake[i-1][0] > snake[i][0] else -1), snake[i][1])
                    else:
                        new_x = snake[i][0] + (1 if snake[i-1][0] > snake[i][0] else -1)
                        new_y = snake[i][1] + (1 if snake[i-1][1] > snake[i][1] else -1)
                        snake[i] = (new_x, new_y)
                    t_pos.add(snake[9])
            print_snake(snake, t_pos)
    return len(t_pos)


def print_snake(snake: list[tuple[int, int]], tail_pos: set[tuple[int, int]]) -> None:
    min_x = min([x for x, _ in snake])
    max_x = max([x for x, _ in snake])
    min_y = min([y for _, y in snake])
    max_y = max([y for _, y in snake])

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            t = (x, y)
            if t in snake:
                i = snake.index(t)
                print(i, end="")
            elif t in tail_pos:
                print("#", end="")
            else:
                print(".", end="")
        print("")
    print("")


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
    assert run(lines) == 1

    lines = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""".splitlines()
    assert run(lines) == 36


if __name__ == "__main__":
    test()
    main()
