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
def get_ints(line):
    return list(map(int, non_digits.split(line)))

def tri(n):
    return n * (n + 1) // 2

def d07(inp, sample=False):
    p1, p2 = None, None

    nums = get_ints(inp.strip())
    snums = list(sorted(nums))
    mid = snums[len(snums)//2]
    bestk = mid
    bestv = len(snums) * (max(snums) - min(snums))
    for i in range(mid - 2, mid + 3):
        v = sum(map(lambda x:abs(x - i), snums))
        if v < bestv:
            bestv = v
            bestk = i
    p1 = bestv

    cnums = Counter(snums)
    bestk = mid
    bestv = len(snums) * tri(max(snums) - min(snums))
    for i in range(min(snums), max(snums)+1):
        iv = sum(tri(abs(i-k)) * v for k,v in cnums.items())
        if iv < bestv:
            bestv = iv
            bestk = i
    p2 = bestv

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d07(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d07.txt') as f:
        inp = f.read().strip()
    return d07(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """16,1,2,0,4,2,7,1,2,14""", 37, 168),
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
