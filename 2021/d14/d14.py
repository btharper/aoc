from functools import cache
from collections import defaultdict, Counter, deque
from itertools import product, pairwise
from multiprocessing import Pool
import math
import re

def orda(char):
    return ord(char) - ord('A')

@cache
def expand_inner(rules, a, b, depth):
    if b is None:
        res = [0] * 26
        res[a] = 1
        return res
    if depth <= 0:
        return expand_inner(rules, a, None, depth)
    c = rules[a*26+b]
    return (*map(sum, zip(
            expand_inner(rules, a, c, depth-1),
            expand_inner(rules, c, b, depth-1),
        )),)

def expand(rules, ord_tup, depth):
    counts = [expand_inner(rules, a, b, depth) for a, b in pairwise(ord_tup)]
    tail = expand_inner(rules, ord_tup[-1], None, depth)

    res = (*filter(None, map(sum, zip(*counts, tail))),)

    return max(res) - min(res)

def parse_rules(rule_list):
    rules = list([None] * 26 * 26)
    for rule in rule_list.split('\n'):
        a,b,c = (ord(char) - ord('A') for char in rule if 'A' <= char <= 'Z')
        rules[a*26+b] = c
    return (*rules,)

def d14(inp, sample=False):
    p1, p2 = None, None

    start_str, rule_list = inp.split('\n\n')
    rules = parse_rules(rule_list)

    start = (*map(orda, start_str),)
    p1 = expand(rules, start, 10)
    p2 = expand(rules, start, 40)

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d14(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d14.txt') as f:
        inp = f.read().strip()
    return d14(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""", 1588, 2188189693529),
    ]

    main_rules = parse_rules(cases[0][1].split('\n\n')[-1])
    assert 0 == expand(main_rules, (*map(orda, 'CB'),), 0) #CB
    assert 0 == expand(main_rules, (*map(orda, 'CB'),), 1) #CHB
    assert 1 == expand(main_rules, (*map(orda, 'CB'),), 2) #CBHCB
    assert 2 == expand(main_rules, (*map(orda, 'CB'),), 3) #CHBHHBCHB

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
