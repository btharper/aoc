from collections import defaultdict, Counter, deque
from functools import cache
from itertools import product, pairwise
from multiprocessing import Pool
import math
import re
from dataclasses import dataclass
from typing import Optional,List,Dict

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

@dataclass(order=True)
class Point:
    x: int
    y: int
    z: int

    def delta(self, dx = 0, dy = 0, dz = 0):
        return Point(self.x + dx, self.y + dy, self.z + dz)

@dataclass
class Cuboid:
    lo: Point
    hi: Point

    def overlap(self, other):
        assert isinstance(other, Cuboid)
        assert isinstance(self.lo, Point)
        assert isinstance(self.hi, Point)
        assert isinstance(other.lo, Point)
        assert isinstance(other.hi, Point)
        # No overlap
        if self.hi.x < other.lo.x or other.hi.x < self.lo.x:
            return False
        if self.hi.y < other.lo.y or other.hi.y < self.lo.y:
            return False
        if self.hi.z < other.lo.z or other.hi.z < self.lo.z:
            return False
        return True

    def size(self):
        return (self.hi.x - self.lo.x + 1) * (self.hi.y - self.lo.y + 1) * (self.hi.z - self.lo.z + 1)

@dataclass
class CuboidSplits:
    sub: deque[Optional[Cuboid]] = None

    def __post_init__(self):
        # Add sentinel
        self.sub = deque()
        assert None not in self.sub
        self.sub.append(None)

    def add(self, cub):
        self.sub.rotate(1)
        self.sub.append(cub)
        self.sub.rotate(-1)

    def size(self):
        assert self.sub[-1] is None
        self.sub.pop()
        res = sum(cub.size() for cub in self.sub)
        self.sub.append(None)
        return res

    def remove(self, other):
        assert self.sub[-1] is None
#        print(f"Removing {other}")
        while self.sub[0] is not None:
#            print(f"\t",end='')
#            print(*self.sub, sep='\n\t')
            if not self.sub[0].overlap(other):
                self.sub.rotate(-1)
                continue
            old = self.sub.popleft()
            # Split and save old.lo section
            if old.lo.x < other.lo.x <= old.hi.x:
                new_cub = Cuboid(old.lo.delta(), old.hi.delta())
                new_cub.hi.x = other.lo.x - 1
                old.lo.x = other.lo.x
                self.sub.append(new_cub)
            # Split and save old.hi section
            if old.hi.x > other.hi.x >= old.lo.x:
                new_cub = Cuboid(old.lo.delta(), old.hi.delta())
                new_cub.lo.x = other.hi.x + 1
                old.hi.x = other.hi.x
                self.sub.append(new_cub)
            # Split and save old.lo section
            if old.lo.y < other.lo.y <= old.hi.y:
                new_cub = Cuboid(old.lo.delta(), old.hi.delta())
                new_cub.hi.y = other.lo.y - 1
                old.lo.y = other.lo.y
                self.sub.append(new_cub)
            # Split and save old.hi section
            if old.hi.y > other.hi.y >= old.lo.y:
                new_cub = Cuboid(old.lo.delta(), old.hi.delta())
                new_cub.lo.y = other.hi.y + 1
                old.hi.y = other.hi.y
                self.sub.append(new_cub)
            # Split and save old.lo section
            if old.lo.z < other.lo.z <= old.hi.z:
                new_cub = Cuboid(old.lo.delta(), old.hi.delta())
                new_cub.hi.z = other.lo.z - 1
                old.lo.z = other.lo.z
                self.sub.append(new_cub)
            # Split and save old.hi section
            if old.hi.z > other.hi.z >= old.lo.z:
                new_cub = Cuboid(old.lo.delta(), old.hi.delta())
                new_cub.lo.z = other.hi.z + 1
                old.hi.z = other.hi.z
                self.sub.append(new_cub)
#            # Split and save old.lo section
#            if old.lo.y < other.lo.y <= old.hi.y:
#                new_pt = old.hi.delta()
#                new_pt.y = other.lo.y-1
#                new_val = Cuboid(lo=old.lo.delta(0), hi=new_pt)
#                old.lo.y = other.lo.y
#                self.sub.append(new_val)
#            # Split and save old.hi section
#            if old.hi.y > other.hi.y >= old.lo.y:
#                new_pt = old.lo.delta()
#                new_pt.y = other.hi.y+1
#                new_val = Cuboid(lo=new_pt, hi=old.hi.delta(0))
#                old.hi.y = other.hi.y
#                self.sub.append(new_val)
#            # Split and save old.lo section
#            if old.lo.z < other.lo.z <= old.hi.z:
#                new_pt = old.hi.delta()
#                new_pt.z = other.lo.z-1
#                new_val = Cuboid(lo=old.lo.delta(0), hi=new_pt)
#                old.lo.z = other.lo.z
#                self.sub.append(new_val)
#            # Split and save old.hi section
#            if old.hi.z > other.hi.z >= old.lo.z:
#                new_pt = old.lo.delta()
#                new_pt.z = other.hi.z+1
#                new_val = Cuboid(lo=new_pt, hi=old.hi.delta(0))
#                old.hi.z = other.hi.z
#                self.sub.append(new_val)
#            print(f"Discarding {old}\n\t",end='')
            del old
        self.sub.rotate(-1)
        assert self.sub[-1] is None

def d22(inp, sample=False):
    p1, p2 = None, None

    cubes = {}
    inst = []
    splits = CuboidSplits()
    for line in inp.split('\n'):
#        print('\n\nSplits:\n\t', end='')
#        print(*splits.sub, sep='\n\t')
        state, coord = line.split()
        state = state == 'on'
        coords_xyz = (*map(lambda x:(*map(int, x.split('..')),), map(lambda x: x.split('=')[-1], coord.split(','))),)
        #print(*coords_xyz, sep=' ^^^ ')
        inst.append((state, coords_xyz))
        #print(*zip(*coords_xyz), sep=' *** ')
        cub = Cuboid(*map(lambda p:Point(*p), zip(*coords_xyz)))
        splits.remove(cub)
        if state:
            splits.add(cub)
        coords_xyz = [*map(lambda x: range(x[0], x[1]+1), coords_xyz)]
#        print(coords_xyz)
        if all(-50 <= coords.start <= 50 or -50 <= coords.stop - 1 <= 50 for coords in coords_xyz):
            for x,y,z in product(*coords_xyz):
                if -50 <= x <= 50 and -50 <= y <= 50 and -50 <= z <= 50:
                    cubes[x,y,z] = state
#    print('\n\nFinal splits:\n\t', end='')
#    print(*splits.sub, sep='\n\t')
    p1 = sum(cubes.values())
    p2 = splits.size()

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d22(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d22.txt') as f:
        inp = f.read().strip()
    return d22(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        ("u1", """on x=1..3,y=1..3,z=1..3
off x=2..2,y=2..2,z=1..2""", 25, 25),
        ("u2", """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15""", 590784, 590784),
        (0, """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10""", 39, 39),
        (1, """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""", 590784, None),
        (2, """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507""", 474140, 2758514936282235),
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
