from collections import defaultdict, Counter, deque
from functools import cache
from itertools import cycle, product, pairwise
from multiprocessing import Pool
from typing import Tuple, Dict, List
import math
import operator as oper
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

dirac_freq = ((3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1))

@cache
def dirac(curr_score, other_score, curr_pos, other_pos, roll):
    curr_pos = (curr_pos + roll) % 10
    curr_score += curr_pos + 1
    if curr_score >= 21:
        return 1, 0
    res1, res2 = 0,0
    for dice_roll, freq in dirac_freq:
        dir1, dir2 = dirac(other_score, curr_score, other_pos, curr_pos, dice_roll)
        res1 += dir1 * freq
        res2 += dir2 * freq
    return res2, res1

def d21(inp):
    pos = []
    score = [0, 0]
    for line in inp.split('\n'):
        *_, player_pos = line.split()
        pos.append(int(player_pos)-1)
    res1, res2 = 0,0
    for dice_roll, freq in dirac_freq:
        dir1, dir2 = dirac(0, 0, *pos, dice_roll)
        res1 += dir1 * freq
        res2 += dir2 * freq
    p2 = max(res1, res2)

    roll_res = (6, 9, 2, 5, 8, 1, 4, 7, 0, 3)
    rolls = 0
    player = 0
    while max(score) < 1000:
        new_pos = (pos[player] + roll_res[rolls % 10]) % 10
        rolls += 3
        score[player] += new_pos + 1
        pos[player] = new_pos
        player = 1 - player
    p1 = min(score) * rolls

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d21(inp)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d21.txt') as f:
        inp = f.read().strip()
    return d21(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """Player 1 starting position: 4
Player 2 starting position: 8""", 739785, 444356092776315),
    ]

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
            assert p1 == 604998
            assert p2 == 157253621231420
            print(f"p1 = {p1}\np2 = {p2}")
