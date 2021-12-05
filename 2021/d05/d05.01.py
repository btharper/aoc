from collections import defaultdict, Counter, deque
from itertools import product
from multiprocessing import Pool
import re
import math

def sign(a, b):
    return int(math.copysign(1, b-a))

def autorange(a, b):
    if a == b:
        return (a,)
    s = sign(a, b)
    return range(a, b+s, s)

def d05(inp, sample=False):
    p1, p2 = None, None
    not_digits = re.compile('[^0-9]+')

    cord = {}
    mp1 = Counter()
    mp2 = Counter()
    for line in inp.strip().split('\n'):
        #print(line, re.split('[^0-9]+', line))
        x1, y1, x2, y2 = map(int, not_digits.split(line))
        #xy1, xy2 = line.split('->')
        #x1, y1 = map(int, xy1.strip().split(','))
        #x2, y2 = map(int, xy2.strip().split(','))

        ix = autorange(x1, x2)
        iy = autorange(y1, y2)
        if x1 == x2 or y1 == y2:
            for xy in product(ix, iy):
                mp1[xy] += 1
        else:
            for xy in zip(ix, iy):
                mp2[xy] += 1

    p1 = sum(c > 1 for c in mp1.values())
    mp2 += mp1
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
