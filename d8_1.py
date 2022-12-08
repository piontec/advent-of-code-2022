def run(lines: list[str]) -> int:
    area = []
    for line in lines:
        area.append([[int(c), 0] for c in line])

    for row_ind in range(len(area)):
        scan_row(area, row_ind, from_left=True)
        scan_row(area, row_ind, from_left=False)

    for col_ind in range(len(area[0])):
        scan_col(area, col_ind, from_top=True)
        scan_col(area, col_ind, from_top=False)

    visible = 0
    for row in area:
        for cell in row:
            visible += cell[1]
    return visible

def scan_row(area, row_ind, from_left: bool):
    row_len = len(area[0])
    edge = area[row_ind][0] if from_left else area[row_ind][row_len - 1]
    edge[1] = 1
    best_so_far = edge[0]
    rng = range(1, len(area[row_ind]) - 1) if from_left else range(row_len - 2, 0)
    for i in rng:
        if area[row_ind][i][0] > best_so_far:
            area[row_ind][i][1] = 1
            best_so_far = area[row_ind][i][0]

def scan_row(area, row_ind, from_left: bool):
    row_len = len(area[0])
    edge = area[row_ind][0] if from_left else area[row_ind][row_len - 1]
    edge[1] = 1
    highest_so_far = edge[0]
    rng = range(1, len(area[row_ind]) - 1) if from_left else range(row_len - 2, 0, -1)
    for i in rng:
        if area[row_ind][i][0] > highest_so_far:
            area[row_ind][i][1] = 1
            highest_so_far = area[row_ind][i][0]

def scan_col(area, col_ind, from_top: bool):
    col_len = len(area)
    edge = area[0][col_ind] if from_top else area[col_len - 1][col_ind]
    edge[1] = 1
    highest_so_far = edge[0]
    rng = range(1, col_len - 1) if from_top else range(col_len - 2, 0, -1)
    for i in rng:
        if area[i][col_ind][0] > highest_so_far:
            area[i][col_ind][1] = 1
            highest_so_far = area[i][col_ind][0]

def main() -> None:
    with open("i8.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


def test() -> None:
    lines = """30373
25512
65332
33549
35390""".splitlines()
    assert run(lines) == 21


if __name__ == "__main__":
    test()
    main()
