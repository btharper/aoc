from enum import IntFlag
from collections import defaultdict, Counter, deque
from itertools import product
from multiprocessing import Pool
import math
import re

def d12(inp, sample=False):
    p1, p2 = 0, 0

    to_int = {'start': 0, 'double': 1, 'end': 2}
    next_int = max(to_int.values()) << 1
    graph = defaultdict(int)
    edges = defaultdict(set)
    small = 0
    for line in inp.strip().split():
        lhs, rhs = nodes = line.split('-')
        for node in nodes:
            if node in to_int:
                n = to_int[node]
            else:
                to_int[node] = n = next_int
                next_int <<= 1
            if 'a' <= node[0] <= 'z':
                small |= n
        lhsi, rhsi = to_int[lhs], to_int[rhs]
        graph[lhsi] |= rhsi
        graph[rhsi] |= lhsi
        if lhsi > 0:
            edges[rhsi].add(lhsi)
        if rhsi > 0:
            edges[lhsi].add(rhsi)
    # Remove 'end' bit
    small &= ~3

    visiting = {0,}
    counts = defaultdict(Counter)
    # counts[{node}][{mask}] = {count}
    counts[0][0] = 1
    while visiting:
        curr = visiting.pop()
        mask_counts = counts[curr]
        for node in edges[curr]:
            if node & small:
                for mask, count in mask_counts.items():
                    if mask & node == 0:
                        counts[node][mask | node] += count
                        visiting.add(node)
                    elif mask & 1 == 0:
                        counts[node][mask | 1] += count
                        visiting.add(node)
            else:
                counts[node].update(mask_counts)
                if node > 2:
                    visiting.add(node)
        counts[curr].clear()

    p = [0,0]
    for mask, count in counts[2].items():
        p[mask & 1] += count
    p1 = p[0]
    p2 = sum(p)
    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d12(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d12.txt') as f:
        inp = f.read().strip()
    return d12(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """start-A
start-b
A-c
A-b
b-d
A-end
b-end""", 10, 36),
        (1, """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""", 19, 103),
        (2, """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""", 226, 3509),
    ]

#    """
    # Non multiprocessing version
    for case in cases:
        validate_test(*case)
    p1, p2 = main()
    assert p1 == 4691, "Wrong answer for p1"
    assert p2 == 140718, "Wrong answer for p2"
    print(f"p1 = {p1}\np2 = {p2}")
    """

    with Pool(processes=min(8, len(cases) + 1)) as pool:
        main_res = pool.apply_async(main)
        test_res = [pool.apply_async(validate_test, case) for case in cases]
        test_pass, do_p1, do_p2 = True, False, False
        for test in test_res:
            tp, dp1, dp2 = test.get(10)
            test_pass &= tp
            do_p1 |= dp1
            do_p2 |= dp2
        if test_pass:
            p1, p2 = main_res.get(60)
            assert p1 == 4691, "Wrong answer for p1"
            assert p2 == 140718, "Wrong answer for p2"
            assert do_p1 or do_p2, "Didn't run any tets"
            assert p1 is None or do_p1 == True, "Got P1 value without 'do_p1' set"
            assert p2 is None or do_p2 == True, "Got P2 value without 'do_p2' set"
            print(f"p1 = {p1}\np2 = {p2}")

"""#"""#"""
