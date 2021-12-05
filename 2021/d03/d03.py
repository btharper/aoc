from collections import defaultdict, Counter, deque
from itertools import product
from multiprocessing import Pool
import re

do_p2 = False

def d03(inp):
    p1, p2 = None, None

    ga = ep = 0
    bits = defaultdict(Counter)
    for num in inp.strip().split():
        #print(num, bin(num)[2:])
        bs = num
        for i, b in enumerate(reversed(bs)):
            bits[i][b] += 1
    #print(bits)
    for k,v in bits.items():
        bit_counts = v.most_common()
        ga += (1 << (k)) * int(bit_counts[0][0])
        ep += (1 << (k)) * int(bit_counts[-1][0])
    p1 = ga * ep

    #print(*sorted(inp.split()), sep='\n')

    #### P2

    ox_n = list(sorted(inp.strip().split()))
    co_n = list(sorted(inp.strip().split()))

    ox = co = 0
    while (lox := len(ox_n)) > 1:
            n = ox_n[lox//2][0]
            ox_n = list(map(lambda x:x[1:], filter(lambda x:x[0] == n, ox_n)))
            ox *= 2
            ox += int(n)

    #print("Starting co")
    while (lco := len(co_n)) > 1:
            n = co_n[(lco)//2][0]
            #print(f"for co, found(dropping) {n}")
            co_n = list(map(lambda x:x[1:], filter(lambda x:x[0] != n, co_n)))
            co *= 2
            co += 1-int(n)
            #print(*map(lambda x:f"{bin(co)[2:]}_{x}", co_n), sep='\n', end='\n\n')
    co_w = co_n[0]
    while co_w:
        co *= 2
        co += int(co_w[0])
        co_w = co_w[1:]
    #print(f"{ox=}, {co=}")
    p2 = ox * co


    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    global do_p2
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d03(inp)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True

def main():
    with open('inputs/d03.txt') as f:
        inp = f.read().strip()
    return d03(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""", 198, 230),
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
            assert do_p2 or p2 is None, f"Got p2 value ({p2=}) without 'do_p2' set ({do_p2=})"
            print(f"p1 = {p1}\np2 = {p2}")
