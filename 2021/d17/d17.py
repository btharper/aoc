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

def inp_to_ranges(xy_strs):
    res = []
    for strs in xy_strs:
        a,b = map(int, strs.strip(',xy=').split('..'))
        res.append(range(a,b+1))
    return res

def d17(inp, sample=False):
    p1, p2 = None, 0

    _, _, *xy_strs = inp.split()
    x_range, y_range = inp_to_ranges(xy_strs)

    p1 = y_range.start
    for ixv in range(0, x_range.stop+1):
        if ixv * (ixv+1) < x_range.start * 2:
            continue
        for iyv in range(y_range.start, -y_range.start):
            x, y = 0, 0
            xv, yv = ixv, iyv
            while y > y_range.start and x < x_range.stop:
                x += xv
                y += yv
                xv = max(0, xv - 1)
                yv -= 1
                if x in x_range and y in y_range:
                    p2 += 1
                    p1 = max(p1, iyv * (iyv + 1) // 2)
                    break
    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d17(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d17.txt') as f:
        inp = f.read().strip()
    return d17(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, "target area: x=20..30, y=-10..-5", 45, 112),
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
            assert do_p1 or do_p2, "Didn't run any tests"
            assert p1 is None or do_p1 == True, "Got P1 value without 'do_p1' set"
            assert p2 is None or do_p2 == True, "Got P2 value without 'do_p2' set"
            assert p1 == 5995
            assert p2 == 3202
            print(f"p1 = {p1}\np2 = {p2}")
