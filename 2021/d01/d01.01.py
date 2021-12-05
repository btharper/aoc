from collections import defaultdict, Counter, deque
from itertools import product
from multiprocessing import Pool

def d01(inp):
    # Implementation that capable of O(1) space
    p1 = p2 = 0
    itr = iter(map(lambda x:int(x.strip()), inp.split()))

    # Prime moving window
    a = b = c = 0
    try:
        a = next(itr)
        b = next(itr)
        c = next(itr)
    except:
        pass
    if a<b: p1 += 1
    if b<c: p1 += 1

    p2_nums = deque((a,b,c), maxlen=3)
    p2_a = a+b+c
    p2_b = a+b
    p2_lag = 0
    p1_lag = c

    for num in itr:
        if num > p1_lag:
            p1 += 1

        p2_a += num - p2_nums[0]
        p2_b += p1_lag - p2_lag

        if p2_a > p2_b:
            p2 += 1

        p1_lag = num
        p2_lag = p2_nums.popleft()
        p2_nums.append(num)

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
            pass
            p1, p2 = main_res.get(60)
            print(f"p1 = {p1}\np2 = {p2}")
            assert p1 == 1676
            assert p2 == 1706
