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

def d11(inp, sample=False):
    p1, p2 = 0, None

    grid = {}
    max_x, max_y = 0, 0
    for y, line in enumerate(inp.strip().split()):
        max_y = max(y + 1, max_y)
        for x, char in enumerate(line):
            max_x = max(x + 1, max_x)
            grid[x,y] = int(char)

    for i in range(1000):
        round = 0
        if i % 10 == 0 or i < 10:
            print(f"step {i}:", end='')
            for y in range(max_y):
                for x in range(max_x):
                    if x == 0:
                        print("")
                    print(grid[x,y], end='')
            print("\n")
        flash = set()
        spent = set()
        for x in range(max_x):
            for y in range(max_y):
                grid[x,y] += 1
                if grid[x,y] > 9:
                    flash.add((x,y))
        while flash:
            x,y = p = flash.pop()
            round += 1
            spent.add(p)
            for dx, dy in product(range(-1,2), range(-1,2)):
                if dx == 0 and dy == 0:
                    continue
                dp = (x+dx, y+dy)
                if dp in spent or dp not in grid:
                    continue
                val = grid[dp]
                if val >= 9:
                    flash.add(dp)
                else:
                    grid[dp] = val + 1
        for p in spent:
            grid[p] = 0
        if i < 100:
            p1 += round
        if round == 100 and p2 is None:
            p2 = i + 1
            break

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d11(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d11.txt') as f:
        inp = f.read().strip()
    return d11(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""", 1656, 195),
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
