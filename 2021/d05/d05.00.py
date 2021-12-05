from collections import defaultdict, Counter, deque
from itertools import product
from multiprocessing import Pool
import re

do_p2 = False

def d05(inp, sample=False):
    p1, p2 = None, None

    cord = {}
    mp = Counter()
    mp2 = Counter()
    for line in inp.strip().split('\n'):
        #print(line)
        xy1, xy2 = line.split('->')
        x1, y1 = map(int, xy1.strip().split(','))
        x2, y2 = map(int, xy2.strip().split(','))

        if x1 != x2 and y1 != y2:
            ix, iy = x1, y1
            while ix != x2 and iy != y2:
                mp2[ix, iy] += 1
                if x2 > x1:
                    ix += 1
                else:
                    ix -= 1
                if y2 > y1:
                    iy += 1
                else:
                    iy -= 1
            mp2[ix, iy] += 1
            continue

        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        #print(f"in line with {xy1=} & {xy2=}")
        for xy in product(range(x1, x2+1), range(y1, y2+1)):
            #print(f"\tAdding {xy=}")
            mp[xy] += 1
    p1 = sum(c > 1 for c in mp.values())
    mp2 += mp
    p2 = sum(c > 1 for c in mp2.values())

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d05(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d05.txt') as f:
        inp = f.read().strip()
    return d05(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""", 5, 12),
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
