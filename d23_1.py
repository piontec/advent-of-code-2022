Pos = tuple[int, int]

dirs = "NSWE"
moves = ((0, -1), (0, 1), (-1, 0), (1, 0))


# noinspection PyCompatibility
def count_free_space(area: dict[int, Pos]) -> int:
    min_x = min(pos[0] for pos in area.values())
    min_y = min(pos[1] for pos in area.values())
    max_x = max(pos[0] for pos in area.values())
    max_y = max(pos[1] for pos in area.values())
    free = (max_x - min_x + 1) * (max_y - min_y + 1) - len(area)
    return free


def get_proposed(area: dict[int, Pos], ei: int, dir_index: int) -> Pos:
    busy: dict[str, bool] = {}
    pos = area[ei]
    busy["N"] = any((pos[0] + x, pos[1] - 1) in area.values() for x in (-1, 0, 1))
    busy["S"] = any((pos[0] + x, pos[1] + 1) in area.values() for x in (-1, 0, 1))
    busy["E"] = any((pos[0] + 1, pos[1] + y) in area.values() for y in (-1, 0, 1))
    busy["W"] = any((pos[0] - 1, pos[1] + y) in area.values() for y in (-1, 0, 1))
    if all(not v for v in busy.values()):
        return pos
    for offset in range(4):
        new_index = (dir_index + offset) % len(dirs)
        if not busy[dirs[new_index]]:
            proposed = pos[0] + moves[new_index][0], pos[1] + moves[new_index][1]
            return proposed
    return pos


def print_it(area: dict[int, Pos]):
    min_x = min(pos[0] for pos in area.values())
    min_y = min(pos[1] for pos in area.values())
    max_x = max(pos[0] for pos in area.values())
    max_y = max(pos[1] for pos in area.values())

    for y in range(min_y, max_y + 1):
        line = ''.join("#" if (x, y) in area.values() else "." for x in range(min_x, max_x + 1))
        print(line)


def run(lines: list[str], rounds: int = 10) -> int:
    area: dict[int, Pos] = {}
    elf_index = 0
    for li in range(len(lines)):
        line = lines[li].strip()
        for i in range(len(line)):
            if line[i] == ".":
                continue
            area[elf_index] = (i, li)
            elf_index += 1

    dir_index = 0
    # print_it(area)
    for r in range(rounds):
        proposed: dict[Pos, list[int]] = {}
        for ei in area.keys():
            pos = get_proposed(area, ei, dir_index)
            if pos in proposed.keys():
                proposed[pos].append(ei)
            else:
                proposed[pos] = [ei]
        new_area: dict[int, Pos] = {}
        for pos in proposed:
            assert len(proposed[pos]) > 0
            # only 1 elf wants this spot
            if len(proposed[pos]) == 1:
                new_area[proposed[pos][0]] = pos
            # else don't move them
            else:
                for ei in proposed[pos]:
                    new_area[ei] = area[ei]
        area = new_area
        dir_index = (dir_index + 1) % len(dirs)

        # print(f"After the end of round {r}")
        # print_it(area)
    return count_free_space(area)


def main() -> None:
    with open("i23.txt") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def test() -> None:
    res = run("""....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..""".splitlines())
    assert res == 110


if __name__ == "__main__":
    test()
    main()
