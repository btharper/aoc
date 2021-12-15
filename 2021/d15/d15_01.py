from collections import defaultdict, Counter, deque
from functools import cache
from itertools import product, pairwise
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

def remap(grid, x, y, x_len, y_len):
    xd, xm = divmod(x, x_len)
    yd, ym = divmod(y, y_len)
    if xd > 4 or yd > 4:
        return None
    v = grid[xm,ym]
    return (v-1+xd+yd) % 9 + 1

def d15(inp, sample=False):
    p1, p2 = None, None

    lines = inp.strip().split('\n')
    y_len = len(lines)
    x_len = len(lines[0])
    grid = {}
    cost = {(0,0):0, (-1,0):-int(inp[0])}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            val = int(char)
            grid[x,y] = val
            c_u = cost.get((x,y-1), cost.get((x-1,y), None))
            c_l = cost.get((x-1,y), cost.get((x,y-1), None))
            cost[x,y] = min(c_u, c_l) + val

    check = deque()
    check_set = set()
    for c_round in range(5):
        if c_round == 4:
            check_set.clear()
        for x in range(x_len * 5):
            for y in range(y_len * 5):
                c_c = cost.get((x,y), None)
                if c_c is not None:
                    c_u = cost.get((x-1,y), c_c)
                    c_d = cost.get((x+1,y), c_c)
                    c_l = cost.get((x,y-1), c_c)
                    c_r = cost.get((x,y+1), c_c)
                    c_min = min(min(c_u, c_d), min(c_l, c_r))
                    c_new = c_min + remap(grid, x,y, x_len, y_len)
                    if c_new < c_c:
                        for node in [(x,y), (x-1,y), (x+1, y), (x, y+1), (x, y-1)]:
                            if node not in check_set:
                                check_set.add(node)
                                #check.append(node)
                        cost[x,y] = c_new
                else: # c_c is None
                    assert c_round == 0
                    c_u = cost.get((x-1,y), cost.get((x,y-1), None))
                    c_l = cost.get((x,y-1), cost.get((x-1,y), None))
                    c_d = cost.get((x+1,y), c_u)
                    c_r = cost.get((x,y+1), c_l)
                    c_min = min(min(c_u, c_d), min(c_r, c_l))
                    cost[x,y] = c_min + remap(grid, x,y, x_len, y_len)
    print(f"Want to check {len(check_set)} points")
    while check_set:
        x,y = check_set.pop()
        if x < 0 or y < 0:
            continue
        if remap(grid, x, y, x_len, y_len) is None:
            continue
        c_c = cost[x,y]
        c_u = cost.get((x,y-1), c_c)
        c_d = cost.get((x,y+1), c_c)
        c_l = cost.get((x-1,y), c_c)
        c_r = cost.get((x+1,y), c_c)
        c_min = min(min(c_u, c_d), min(c_l, c_r))
        c_new = c_min + remap(grid, x, y, x_len, y_len)
        if c_new < c_c:
            check_set.update([(x,y), (x-1,y), (x+1, y), (x, y+1), (x, y-1)])
            cost[x,y] = c_new
    p1 = cost[x_len-1, y_len-1]
    p2 = cost[x_len*5-1, y_len*5-1]

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d15(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d15.txt') as f:
        inp = f.read().strip()
    return d15(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""", 40, 315),
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
