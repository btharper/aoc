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

def d20(inp, sample=False):
    p1, p2 = None, None

    top, img_str = inp.split('\n\n')
    top = ''.join(top.split())

    grid = defaultdict(bool)
    min_x, max_x = 0, 1
    min_y, max_y = 0, 1
    for y, line in enumerate(img_str.split('\n')):
        min_y, max_y = min(min_y, y), max(max_y, y)
        for x, char in enumerate(line):
            min_x, max_x = min(min_x, x), max(max_x, x)
            assert char in ('#', '.')
            grid[x,y] = (char == '#')

    rule = {}
    for i, char in enumerate(top):
        assert char in ('#', '.')
        rule[i] = (char == '#')
    assert sample == False or rule[ 0] == False
    assert sample == False or rule[ 1] == False
    assert sample == False or rule[ 2] == True
    assert sample == False or rule[34] == True

    d_val = ((1,1), (0, 1), (-1, 1), (1, 0), (0, 0), (-1, 0), (1, -1), (0, -1), (-1, -1))
    default = False
    for step in range(50):
        n_grid = {}
        n_min_x, n_min_y = 1,1
        n_max_x, n_max_y = 0,0
        for x, y in product(range(min_x-1, max_x+2), range(min_y-1,max_y+2)):
            total = 0
            for i, (dx, dy) in enumerate(d_val):
                nx, ny = x + dx, y + dy
                total += grid.get((nx, ny), default) * (1 << i)
            if rule[total]:
                n_min_x, n_max_x = min(x, n_min_x), max(x, n_max_x)
                n_min_y, n_max_y = min(y, n_min_y), max(y, n_max_y)
            n_grid[x, y] = rule[total]
        min_x, min_y = min(min_x, n_min_x), min(min_y, n_min_y)
        max_x, max_y = max(max_x, n_max_x), max(max_y, n_max_y)
        default = rule[default * 511]
        grid = n_grid
        n_grid = {}
        if step == 1:
            p1 = sum(grid.values())
    p2 = sum(grid.values())

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d20(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d20.txt') as f:
        inp = f.read().strip()
    return d20(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""", 35, 3351),
    ]

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
