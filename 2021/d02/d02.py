from collections import defaultdict, Counter, deque
from itertools import product
from multiprocessing import Pool
import re

def d02(inp):
    p1, p2 = None, None

    inp = re.sub(r"up\s(\d+)", r"-\1j", inp)
    inp = re.sub(r"down\s(\d+)", r"\1j", inp)
    inp = re.sub(r"forward\s(\d+)", r"\1", inp)

    #print(*map(complex, inp.split()[:5]))
    p1_c = sum(map(complex, inp.split()))
    p1 = int(p1_c.real * p1_c.imag)

    inpn = list(map(complex, inp.split()))
    aim = 0
    depth = 0
    fwd = 0
    for num in inpn:
        aim += int(num.imag)
        depth += int(aim * num.real)
        fwd += int(num.real)
    p2 = depth * fwd

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d02(inp)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
    return True

def main():
    with open('../inputs/d02.txt') as f:
        inp = f.read().strip()
    return d02(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """forward 5
        down 5
        forward 8
        up 3
        down 8
        forward 2""", 150, 900),
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
        if all(test.get(30) for test in test_res):
            p1, p2 = main_res.get(60)
            print(f"p1 = {p1}\np2 = {p2}")
