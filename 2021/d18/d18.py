from collections import defaultdict, Counter, deque
from dataclasses import dataclass
from functools import cache
from itertools import product, pairwise, permutations
from multiprocessing import Pool
import math
import re
from typing import List, Union

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

@dataclass
class Snailfish:
    left: Union[Snailfish, int]
    right: Union[Snailfish, int]
    depth: int
    verbose: bool = False

    def __int__(self):
        mag_left = int(self.left)
        mag_right = int(self.right)
        return mag_left * 3 + mag_right * 2

    def __add__(self, other):
        ret = Snailfish(self, other, 0)
        ret.left.IncrementDepth()
        if isinstance(ret.right, Snailfish):
            ret.right.IncrementDepth()
        ret.reduce()
        return ret

    def __str__(self):
        return f"[{self.left},{self.right}]"

    def IncrementDepth(self):
        self.depth += 1
        for child in (self.left, self.right):
            if isinstance(child, Snailfish):
                child.IncrementDepth()

    def SetVerbose(self, val):
        self.verbose = val
        if isinstance(self.left, Snailfish):
            self.left.SetVerbose(val)
        if isinstance(self.right, Snailfish):
            self.right.SetVerbose(val)

    def reduce(self):
        while True:
            if self.CheckExplodes()[0]:
                continue
            if self.CheckSplits():
                continue
            break

    def CheckSplits(self):
        if isinstance(self.left, int):
            if self.left >= 10:
                self.left = Snailfish(self.left // 2, (self.left+1) // 2, self.depth + 1)
                return True
        else:
            if self.left.CheckSplits():
                return True
        if isinstance(self.right, int):
            if self.right >= 10:
                self.right = Snailfish(self.right // 2, (self.right+1) // 2, self.depth + 1)
                return True
        else:
            if self.right.CheckSplits():
                return True
        return False

    def CheckExplodes(self, final=True):
        if self.verbose:
            print(f"Checking ({self})@{self.depth} for explosions -",
                    f"{isinstance(self.left, Snailfish)}-{isinstance(self.right, Snailfish)}")
        if self.depth >= 4 and isinstance(self.left, int) and isinstance(self.right, int):
            if self.verbose:print(f"\tLeaf at {self.depth=} is exploding")
            assert not final
            return True, False, self.left, self.right
        explodes, zerod, leftward, rightward = False, True, None, None
        if isinstance(self.left, Snailfish):
            if self.verbose:print(f"\tChecking left for explosions")
            explodes, zerod, leftward, rightward = self.left.CheckExplodes(False)
            if explodes:
                if self.verbose:print(f"left child exploded {explodes=}, {zerod=}, {leftward=}, {rightward=}")
                if not zerod:
                    self.left = 0
                    zerod = True
                if rightward is not None:
                    if isinstance(self.right, Snailfish):
                        rightward = self.right.ExplosionFromLeft(rightward)
                    else:
                        assert isinstance(self.right, int)
                        self.right += rightward
                        rightward = None
                return explodes, zerod, leftward, rightward
        if isinstance(self.right, Snailfish):
            if self.verbose:print(f"\tChecking right for explosions")
            explodes, zerod, leftward, rightward = self.right.CheckExplodes(False)
            if explodes:
                if self.verbose:print(f"right child exploded {explodes=}, {zerod=}, {leftward=}, {rightward=}")
                if not zerod:
                    self.right = 0
                    zerod = True
                if leftward is not None:
                    if isinstance(self.left, Snailfish):
                        leftward = self.left.ExplosionFromRight(leftward)
                    else:
                        assert isinstance(self.left, int)
                        self.left += leftward
                        leftward = None
                return explodes, zerod, leftward, rightward
        return explodes, zerod, leftward, rightward

    def ExplosionFromLeft(self, val):
        if isinstance(self.left, int):
            self.left += val
            return None
        else:
            assert isinstance(self.left, Snailfish)
            return self.left.ExplosionFromLeft(val)

    def ExplosionFromRight(self, val):
        if isinstance(self.right, int):
            self.right += val
            return None
        else:
            assert isinstance(self.right, Snailfish)
            return self.right.ExplosionFromRight(val)

    @staticmethod
    def parse(inp: str, depth: int):
        #print(f"Parsing {inp} @ {depth=}")
        if ',' not in inp:
            return int(inp)
        vals = [[], []]
        side = 0
        sdepth = 0
        for char in inp[1:-1]:
            if char == ',' and sdepth == 0:
                left_val = Snailfish.parse(''.join(vals[0]), depth + 1)
                side = 1
            else:
                vals[side].append(char)
                if char == '[':
                    sdepth += 1
                elif char == ']':
                    sdepth -= 1
        assert sdepth == 0
        right_val = Snailfish.parse(''.join(vals[1]), depth + 1)
        return Snailfish(left_val, right_val, depth)

def d18(inp, sample=False):
    p1, p2 = None, None

    sf = None
    nums = []
    for line in inp.split('\n'):
        line_sf = Snailfish.parse(line, 0)
        nums.append(line_sf)
        if sf is None:
            sf = line_sf
        else:
            sf = sf + line_sf
    p1 = int(sf)

    biggest_mag = 0

    print('All sf nums:', *nums, sep='\n')

    for a, b in permutations(inp.split('\n'), 2):
        asf, bsf = Snailfish.parse(a, 0), Snailfish.parse(b, 0)
        mag = int(asf + bsf)
        biggest_mag = max(biggest_mag, mag)
    p2 = biggest_mag

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d18(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d18.txt') as f:
        inp = f.read().strip()
    return d18(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""", 4140, 3993),
    ]

    mag_asserts = (
        ('[[1,2],[[3,4],5]]', 143),
        ('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]', 1384),
        ('[[[[1,1],[2,2]],[3,3]],[4,4]]', 445),
        ('[[[[3,0],[5,3]],[4,4]],[5,5]]', 791),
        ('[[[[5,0],[7,4]],[5,5]],[6,6]]', 1137),
        ('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]', 3488),
        ('[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]', 3993),
    )
    for s, v in mag_asserts:
        assert int(Snailfish.parse(s, 0)) == v, f"Snailfish.parse({s}) magnitude != {v}"
        assert str(Snailfish.parse(s, 0)) == s

    explode_cases = (
        ('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]'),
        ('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]'),
        ('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]'),
        ('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'),
        ('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'),
    )

    for s, v in explode_cases:
        sf = Snailfish.parse(s, 0)
        #sf.SetVerbose(True)
        sf.CheckExplodes()
        #sf.verbose = False
        assert str(sf) == v, f"Exploding ({s}) != ({v})\n got {sf}"

    add_cases = (
        ('[1,2]', '[[3,4],5]', '[[1,2],[[3,4],5]]'),
        ('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
            '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
            '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]'),
        ('[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]',
            '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
            '[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]'),
        ('[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
            '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
            '[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]'),
    )
    for first, *oper, res in add_cases:
        reduce_sum = Snailfish.parse(first, 0)
        for second in oper:
            reduce_sum = reduce_sum + Snailfish.parse(second, 0)
        assert str(reduce_sum) == res,f"sum({tuple((first, *oper,))}) != {res}\n = {type(reduce_sum)}{reduce_sum}"


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
    #"""#"""#"""

