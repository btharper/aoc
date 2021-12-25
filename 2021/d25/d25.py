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

grid_char = {'.': '.', (0,1): 'v', (1,0):'>'}
def d25(inp, sample=False):
    p1, p2 = None, None

    grid = {}
    max_x, max_y = 0, 0
    for y, line in enumerate(inp.split()):
        max_y = max(y+1, max_y)
        for x, char in enumerate(line):
            max_x = max(x+1, max_x)
            if char == '>':
                grid[x,y] = (1,0)
            elif char == 'v':
                grid[x,y] = (0,1)
    turn = 0
    moved = True
    n_grid = {}
    while moved:
#        if turn in (0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 55, 56, 57, 58):
#            print(f"After {turn} steps:")
#            for y in range(max_y):
#                for x in range(max_x):
#                    print(grid_char[grid.get((x,y), '.')], end='')
#                print()
        turn += 1
        moved = False
        for (x,y), (dx, dy) in grid.items():
            if dy:
                n_grid[x,y] = grid[x,y]
                continue
            nt = nx, ny = (x+dx)%max_x, (y+dy)%max_y
            if grid.get(nt, None) is None:
                n_grid[nt] = dx,dy
                moved = True
            else:
                n_grid[x,y] = dx,dy
        grid = n_grid
        n_grid = {}
        for (x,y), (dx, dy) in grid.items():
            if dx:
                n_grid[x,y] = grid[x,y]
                continue
            nt = nx, ny = (x+dx)%max_x, (y+dy)%max_y
            if grid.get(nt, None) is None:
                n_grid[nt] = dx,dy
                moved = True
            else:
                n_grid[x,y] = dx,dy
        grid = n_grid
        n_grid = {}

    p1 = turn
    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d25(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d25.txt') as f:
        inp = f.read().strip()
    return d25(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""", 58, None),
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
