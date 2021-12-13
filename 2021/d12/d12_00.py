from collections import defaultdict, Counter, deque
from itertools import product
from multiprocessing import Pool
import math
import re

non_digits = re.compile('[^0-9]+')
def sign(a, b, step=1):
    return int(math.copysign(step, b-a))
def autorange(a,b, step=1):
    if a == b:return (a,)
    s = sign(a, b, step)
    return range(a, b+s, s)
def get_ints(line, strip_line=False):
    if strip_line:
        line = line.strip()
    return [*map(int, non_digits.split(line))]

def d12(inp, sample=False):
    p1, p2 = 0, 0

    graph = defaultdict(set)
    small = set()
    for line in inp.strip().split():
        lhs, rhs = line.split('-')
        if rhs == 'start' or lhs == 'end':
            rhs, lhs = lhs, rhs
        if lhs == 'start':
            graph['start'].add(rhs)
            if rhs not in small and 'a' <= rhs[0] <= 'z':
                small.add(rhs)
        elif rhs == 'end':
            graph[lhs].add('end')
            if lhs not in small and 'a' <= lhs[0] <= 'z':
                small.add(lhs)
        else:
            graph[lhs].add(rhs)
            graph[rhs].add(lhs)
            if rhs not in small and 'a' <= rhs[0] <= 'z':
                small.add(rhs)
            if lhs not in small and 'a' <= lhs[0] <= 'z':
                small.add(lhs)

    for k,v in graph.items():
        graph[k] = frozenset(v)

    search = deque()
    # current location, can visit twice, set(smalls)
    search.append(('start', True, set()))
    while search:
        curr, twice, prev = search.pop()
        if twice:
            nxt = graph[curr]
        else:
            nxt = graph[curr] - prev
        #print(f"From {curr} via {path} with {prev}: Checking {nxt} of {graph[curr]}")
        for node in nxt:
            if node == 'end':
                p1 += twice
                p2 += 1
            elif node in small:
                if node not in prev:
                    search.append((node, twice, prev | {node,}))
                elif twice:
                    search.append((node, False, prev | {node,}))
            else:
                search.append((node, twice, prev))

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

    """
    # Non multiprocessing version
    for case in cases:
        validate_test(*case)
    p1, p2 = main()
    print(f"p1 = {p1}\np2 = {p2}")
    """

    with Pool(processes=min(8, len(cases) + 1)) as pool:
        main_res = pool.apply_async(main)
        test_res = [pool.apply_async(validate_test, case) for case in cases]
        test_pass, do_p1, do_p2 = True, False, False
        for test in test_res:
            tp, dp1, dp2 = test.get(30)
            test_pass &= tp
            do_p1 |= dp1
            do_p2 |= dp2
        if test_pass:
            p1, p2 = main_res.get(60)
            assert do_p1 or do_p2, "Didn't run any tets"
            assert p1 is None or do_p1 == True, "Got P1 value without 'do_p1' set"
            assert p2 is None or do_p2 == True, "Got P2 value without 'do_p2' set"
            print(f"p1 = {p1}\np2 = {p2}")
