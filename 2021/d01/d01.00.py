from collections import defaultdict, Counter, deque
from itertools import product
from multiprocessing import Pool

def d01(inp):
    # Initial solution
    p1, p2 = None, None

    count = 0
    inpl = list(map(lambda s:int(s.strip()), inp.split()))
    for a,b in zip(inpl, inpl[1:]):
        if b>a:
            count += 1
    p1 = count

    count = 0
    inpt = [sum([a,b,c]) for a,b,c in zip(inpl, inpl[1:], inpl[2:])]
    for a,b in zip(inpt, inpt[1:]):
        if b>a:
            count += 1
    p2 = count

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d01(inp)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
    return True

def main():
    with open('inputs/d01.input.txt') as f:
        inp = f.read().strip()
    return d01(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """199
        200
        208
        210
        200
        207
        240
        269
        260
        263""", 7, 5)
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
            assert p1 == 1676
            assert p2 == 1706
