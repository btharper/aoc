from collections import defaultdict, Counter, deque
from functools import cache
from itertools import cycle, product, pairwise
from multiprocessing import Pool
from typing import Tuple, Dict, List
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

@cache
def dirac(player: int, score: Tuple[int], pos: Tuple[int], roll: int, acc):
    score = [*score,]
    pos = [*pos,]
    new_pos = (pos[player] + roll) % 10
    pos[player] = new_pos
    if acc == 3:
        score[player] += new_pos + 1
        if score[player] >= 21:
            ret = [0, 0]
            ret[player] += 1
            return ret
        player = 1 - player
    acc %= 3
    u1 = dirac(player, (*score,), (*pos,), 1, acc+1)
    u2 = dirac(player, (*score,), (*pos,), 2, acc+1)
    u3 = dirac(player, (*score,), (*pos,), 3, acc+1)
    return [*map(sum, zip(u1, u2, u3))]

def d21(inp, sample=False):
    p1, p2 = 0, None

    pos = []
    score = [0, 0]
    rolls = 0
    player = 0
    for line in inp.split('\n'):
        *_, player_pos = line.split()
        pos.append(int(player_pos)-1)
#    for i, p in enumerate(pos):
#        print(f"Player {i+1} starts at {p+1}")
    u1 = dirac(0, (0, 0), (*pos,), 1, 1)
    u2 = dirac(0, (0, 0), (*pos,), 2, 1)
    u3 = dirac(0, (0, 0), (*pos,), 3, 1)
    p2 = max(map(sum, zip(u1, u2, u3)))

    dice_list = [*range(1,101,1)]
#    print(f"{min(dice_list)=} {max(dice_list)=}")
    dice = cycle(range(1, 101))
    while max(score) < 1000:
        rolla = next(dice)
        rollb = next(dice)
        rollc = next(dice)
        roll = rolla+rollb+rollc
        rolls += 3
        pos[player] = (pos[player] + roll) % 10
        score[player] += pos[player] + 1
        #if pos[player] == 0:score[player] += 9
#        print(f"Player {player+1} rolls {rolla}+{rollb}+{rollc} and moves to space {pos[player]+1} for a total score of {score[player]}")
        player = 1 - player
    p1 = min(score) * rolls
#    print(f"After {rolls} turns, losing player has {min(score)} points")

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d21(inp, sample=True)
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

    #"""
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
    #"""
