from typing import Optional


class Node:
    def __init__(self, value: int,  cur_index: int) -> None:
        self.next: Node = Optional[None]
        self.prev: Node = Optional[None]
        self.val = value
        self.cur_index = cur_index

    def move(self, total_len: int) -> None:
        move = self.val
        if move == 0:
            return
        # remove itself from the list
        self.prev.next = self.next
        self.next.prev = self.prev
        mv = move % total_len if move > 0 else (-move) % total_len
        cur = self
        if move > 0:
            # find new place and update indices
            for i in range(mv):
                cur = cur.next
                cur.cur_index -= 1
            cur.next.prev = self
            cur.next = self
            self.cur_index += mv
        else:
            for i in range(mv):
                cur = cur.prev
                cur.cur_index += 1
            cur.prev.next = self
            cur.prev = self
            self.cur_index -= 1


def run(lines: list[str]) -> int:
    nums: list[int] = [int(line) for line in lines]
    msg: dict[int, Node] = {i: Node(nums[i], i) for i in range(len(nums))}
    msg_len = len(msg)
    for k, v in msg.items():
        v.next = msg[(k + 1) % msg_len]
        msg[(k + 1) % msg_len].prev = v
    for orig_index in msg.keys():
        msg[orig_index].move(msg_len)
    res = 0
    new_heads = [n for n in msg.values() if n.cur_index == 0]
    assert len(new_heads) == 1
    new_head = new_heads[0]
    for offset in [1000, 2000, 3000]:
        cur = new_head
        off = offset % msg_len
        for _ in range(off):
            cur = cur.next
        res += cur.val
    return res


def main() -> None:
    with open("i20.txt", "r") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def test() -> None:
    res = run("""1,1,1
2,1,1""".splitlines())
    assert res == 10

    res = run("""1
2
-3
3
-2
0
4""".splitlines())
    assert res == 3


if __name__ == "__main__":
    test()
    main()
