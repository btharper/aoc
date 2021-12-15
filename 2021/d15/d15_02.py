from collections import defaultdict, Counter, deque
from itertools import product, pairwise
from multiprocessing import Pool
import heapq

def d15_part(grid, x_len, y_len, mul):
    directions = ((0,1),(1,0),(-1,0),(0,-1))
    target = (x_len*mul - 1, y_len*mul - 1)
    h_base = (x_len + y_len) * mul
    unchecked = [(h_base, 0,0)]
    seen = {(0,0),}
    g_cost = {(0,0): 0}
    while unchecked:
        _, x, y = heapq.heappop(unchecked)
        if (x,y) == target:
            return g_cost[x,y]
        for dx, dy in directions:
            pt = nx, ny = (x+dx, y+dy)
            if nx < 0 or ny < 0:
                continue
            elif nx < x_len and ny < y_len:
                d_cost = g_cost[x,y] + grid[pt]
            elif nx < x_len*mul and ny < y_len*mul:
                xd, xm = divmod(nx, x_len)
                yd, ym = divmod(ny, y_len)
                d_cost = g_cost[x,y] + (grid[xm,ym] - 1 + xd + yd) % 9 + 1
            else:
                continue
            if d_cost < g_cost.get(pt, d_cost+1):
                g_cost[pt] = d_cost
                if pt not in seen:
                    heapq.heappush(unchecked, (d_cost + h_base - nx - ny, nx, ny))
                    seen.add(pt)

def d15(inp):
    grid = {}
    lines = inp.strip().split()

    y_len = len(lines)
    x_len = len(lines[0])

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[x,y] = int(char)

    p1 = d15_part(grid, x_len, y_len, 1)
    p2 = d15_part(grid, x_len, y_len, 5)

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d15(inp)
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
            assert p1 == 790
            assert p2 == 2998
            print(f"p1 = {p1}\np2 = {p2}")
