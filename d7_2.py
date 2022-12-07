from dataclasses import dataclass
from typing import Optional, cast, Callable


@dataclass
class Entry:
    name: str
    parent: Optional['Entry']
    size: int


@dataclass
class Dir(Entry):
    entries: list[Entry]


@dataclass
class File(Entry):
    pass


def filter_entries(d: Dir, fun: Callable[[Entry], bool]) -> list[Entry]:
    res = []
    if fun(d):
        res.append(d)
    dirs = [cast(Dir, dn) for dn in d.entries if type(dn) is Dir]
    for dn in dirs:
        res += filter_entries(dn, fun)
    return res


def set_dir_size(d: Dir) -> int:
    files = sum([f.size for f in d.entries if type(f) is File])
    dirs = sum([set_dir_size(cast(Dir, nd)) for nd in d.entries if type(nd) is Dir])
    total = files + dirs
    d.size = total
    return total


def run(lines: list[str]) -> int:
    root = Dir("/", None, 0, [])
    current = root
    for line in lines:
        if line == "$ cd /":
            current = root
        elif line.startswith("$ ls"):
            pass
        elif line.startswith("$ cd"):
            dn = line[5:]
            if dn == "..":
                current = current.parent
            else:
                current = [d for d in current.entries if type(d) is Dir and d.name == dn][0]
        elif line.startswith("dir "):
            dn = line[4:]
            d = Dir(dn, current, 0, [])
            if d not in current.entries:
                current.entries.append(d)
        else:
            size_str, name = line.split(" ")
            size = int(size_str)
            f = File(name, current, size)
            if f not in current.entries:
                current.entries.append(f)
    set_dir_size(root)
    free = 70000000 - root.size
    needed = 30000000 - free
    entries = filter_entries(root, lambda d: type(d) is Dir and d.size > needed)
    res = min(e.size for e in entries)
    return res


def main() -> None:
    with open("i7.txt", "r") as i:
        lines = i.readlines()
    lines = [l.rstrip('\n') for l in lines]
    res = run(lines)
    print(res)


def test() -> None:
    lines = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".splitlines()
    assert run(lines) == 24933642


if __name__ == "__main__":
    test()
    main()
