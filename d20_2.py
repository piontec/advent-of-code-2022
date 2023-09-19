from typing import Optional


# key = 1
key = 811589153
# rounds = 1
rounds = 10
jumps_mod = 0


class Node:
    def __init__(self, value: int) -> None:
        self.next: Node = Optional[None]
        self.prev: Node = Optional[None]
        self.val = value

    def __repr__(self) -> str:
        return f"{self.val * key}"

    def move(self) -> None:
        if self.val % jumps_mod == 0:
            return
        move = (self.val * key) % jumps_mod if self.val > 0 else -((-self.val * key) % jumps_mod)
        # remove itself from the list
        self.prev.next = self.next
        self.next.prev = self.prev

        cur = self
        if move > 0:
            # find new place and update indices
            for i in range(move):
                cur = cur.next
            cur.next.prev = self
            self.next = cur.next
            cur.next = self
            self.prev = cur
        else:
            for i in range(abs(move)):
                cur = cur.prev
            cur.prev.next = self
            self.prev = cur.prev
            cur.prev = self
            self.next = cur


def run(lines: list[str]) -> int:
    nums: list[int] = [int(line) for line in lines]
    msg: dict[int, Node] = {i: Node(nums[i]) for i in range(len(nums))}
    msg_len = len(msg)
    global jumps_mod
    jumps_mod = msg_len - 1
    zero_index = -1
    for k, v in msg.items():
        v.next = msg[(k + 1) % msg_len]
        msg[(k + 1) % msg_len].prev = v
        if v.val == 0:
            zero_index = k
    for _ in range(rounds):
        for orig_index in msg.keys():
            msg[orig_index].move()

    res = 0
    for offset in [1000, 2000, 3000]:
        off = offset % msg_len
        cur = msg[zero_index]
        for _ in range(off):
            cur = cur.next
        res += cur.val * key
    return res


def main() -> None:
    with open("i20.txt") as i:
        lines = i.readlines()
    res = run(lines)
    print(res)


def test() -> None:
    res = run("""1
2
-3
3
-2
0
4""".splitlines())
    # assert res == 3
    assert res == 1623178306


if __name__ == "__main__":
    test()
    main()
