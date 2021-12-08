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

def d08(inp, sample=False):
    p1, p2 = 0, 0

    straight = {
        1: 'cf',
        7: 'acf',
        4: 'bcdf',
        2: 'acdeg',
        3: 'acdfg',
        5: 'abdfg',
        0: 'abcefg',
        6: 'abdefg',
        9: 'abcdfg',
        8: 'abcdefg',
    }
    straight = {k: set(v) for k,v in straight.items()}

    grid = {}
    #for a,b in product(straight.items(), straight.items()):
    for ik in straight.keys():
        k = (
            len(straight[ik] ^ straight[1]),
            len(straight[ik] & straight[1]),
            len(straight[ik] ^ straight[7]),
            len(straight[ik] & straight[7]),
            len(straight[ik] ^ straight[4]),
            len(straight[ik] & straight[4]),
            )
        assert k not in grid
        grid[k] = ik

    for line in inp.strip().split("\n"):
        lhs, rhs = line.split("|")
        for digit in rhs.strip().split():
            if len(digit) in (2, 4, 3, 7):
                p1 += 1
        ref = {}
        unref = {}
        for digit in lhs.strip().split():
            if len(digit) == 2:
                ref[1] = set(digit)
                unref[frozenset(digit)] = 1
            elif len(digit) == 3:
                ref[7] = set(digit)
                unref[frozenset(digit)] = 7
            elif len(digit) == 4:
                ref[4] = set(digit)
                unref[frozenset(digit)] = 4
            elif len(digit) == 7:
                ref[8] = set(digit)
                unref[frozenset(digit)] = 8

        assert 1 in ref, f"{digit=}, {frozenset(digit)=}\n{ref=}"

        for digit in lhs.strip().split():
            if len(digit) in (2,3,4,7):
                continue
            digit_set = set(digit)
            k = (
                    len(digit_set ^ ref[1]),
                    len(digit_set & ref[1]),
                    len(digit_set ^ ref[7]),
                    len(digit_set & ref[7]),
                    len(digit_set ^ ref[4]),
                    len(digit_set & ref[4]),
                )
            ref[grid[k]] = set(digit)
            unref[frozenset(digit)] = grid[k]
        assert len(ref.keys()) == 10, f"Not enough numbers"

        display_num = 0
        for digit in rhs.strip().split():
            display_num *= 10
            display_num += unref[frozenset(digit)]
        p2 += display_num


    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d08(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d08.txt') as f:
        inp = f.read().strip()
    return d08(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""", 26, 61229),
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
