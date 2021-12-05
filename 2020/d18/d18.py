from collections import deque
from multiprocessing import Pool
import re

def calc_p2(inp):
    # p2, but no parens
    while m := re.search(r'(?:\d+\s*\+\s*)+\d+', inp):
        val = sum(map(int, m.group().split('+')))
        #   print(f"{m.group()} = {val}")
        inp = inp.replace(m.group(0), str(val))
    prod = 1
    vals = map(int, inp.split('*'))
    for val in vals:
        prod *= val
    return prod

def recur_stack_p2(inp):
    while m := re.search(r'\(([^()]+)\)', inp):
        inp = inp.replace(m.group(0), str(calc_p2(m.group(1))))
    return calc_p2(inp)

def calc_p1(inp):
    #print(f"\t{inp}")
    while m := re.search(r'^\s*(\d+)\s*(\+|\*)\s*(\d+)', inp):
        if m.group(2) == '*':
            val = int(m.group(1)) * int(m.group(3))
        else:
            val = int(m.group(1)) + int(m.group(3))
        #print(f"\t\t{m.group(0)} = {val}")
        inp = inp.replace(m.group(0), str(val), 1)
    #print(f"\t= {inp}")
    return inp

def recur_stack_p1(inp):
    #print(inp)
    while m := re.search(r'\(([^()]+)\)', inp):
        val = calc_p1(m.group(1))
        #print(f"{m.group(0)} = {val}")
        inp = inp.replace(m.group(0), str(val), 1)
    val = int(calc_p1(inp))
    #print("=", val)
    return val

def d18(inp):
    p1, p2 = 0, 0

    for line in inp.split('\n'):
        p1 += recur_stack_p1(line)
        p2 += recur_stack_p2(line)

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    got_p1, got_p2 = d18(inp)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
    return True

def main():
    with open('../inputs/d18.txt') as f:
        inp = f.read().strip()
    return d18(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        ('1', '1 + 2 * 3 + 4 * 5 + 6', 71, 231),
        ('2', '1 + (2 * 3) + (4 * (5 + 6))', 51, 51),
        ('3', '2 * 3 + (4 * 5)', 26, 46),
        ('4', '5 + (8 * 3 + 9 + 3 * 4 * 3)', 437, 1445),
        ('5', '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))' , 12240, 669060),
        ('6', '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632, 23340),
    ]

    """
    # Non multiprocessing version
    for case in cases:
        validate_test(*case)
    p1, p2 = main()
    #assert p2 > 213702899691555
    #assert p1 == 45283905029161, "p1 broke"
    #assert p2 == 216975281211165, "p2 broke"
    print(f"p1 = {p1}\np2 = {p2}")
    exit(0)
    #"""


    #with Pool(processes=min(8, len(cases) + 1)) as pool:
    with Pool(processes=7) as pool:
        main_res = pool.apply_async(main)
        test_res = [pool.apply_async(validate_test, case) for case in cases]
        if all(test.get(30) for test in test_res):
            p1, p2 = main_res.get(60)
            assert p1 == 45283905029161, "p1 broke"
            assert p2 == 216975281211165, "p2 broke"
            print(f"p1 = {p1}\np2 = {p2}\n!")
