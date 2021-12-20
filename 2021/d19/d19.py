from collections import defaultdict, Counter, deque
from dataclasses import dataclass
from functools import cache
from itertools import product, pairwise, permutations, combinations
from multiprocessing import Pool
import copy
import math
import random
import re
import operator as oper
from typing import List, Set, Any, Dict

@dataclass(order=True)
class Point:
    x: int = 0
    y: int = 0
    z: int = 0

    def rot_xy(self):
        self.x, self.y = self.y, -self.x
    def rot_yz(self):
        self.y, self.z = self.z, -self.y
    def rot_xz(self):
        self.x, self.z = self.z, -self.x
    def rot_yx(self):
        self.y, self.x = self.x, -self.y
    def rot_zy(self):
        self.z, self.y = self.y, -self.z
    def rot_zx(self):
        self.z, self.x = self.x, -self.z
    def neg_xy(self):
        self.x, self.y = -self.x, -self.y
    def neg_yz(self):
        self.y, self.z = -self.y, -self.z
    def neg_xz(self):
        self.x, self.z = -self.x, -self.z

    def __add__(self, other):
        return Point(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z
            )

    def __sub__(self, other):
        return Point(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z
            )

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __int__(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def reduce(self):
        x,y,z = xyz = self.astuple()
        pt = Point(*sorted(map(abs, xyz)))
        if 0 in xyz or pt.x == pt.y or pt.y == pt.z:
            return pt
        edit = 1
        if x < 0: edit *= -1
        if y < 0: edit *= -1
        if z < 0: edit *= -1
        x,y,z = abs(x), abs(y), abs(z)
        if x > y or x > z:
            if y < z:
                x, y = y, x
            else:
                x, z = z, x
            edit *= -1
            assert x == min((x,y,z))
        if y > z:
            y, z = z, y
            edit *= -1
            assert x <= y
            assert y <= z
        pt.z *= edit
        return pt

    def astuple(self):
        return (self.x, self.y, self.z)

def run_safety_checks():
    assert_test = (
            (596, -804, -596),
            (23, 35, -35),
            (-23, -35, 35),
            (35, 35, 23),
            (-23, 35, 35),
            (-35, -35, 23),
            (0,0,-5),
            (1,0,3),
            (-2,0,2),
            (0,0,0),
            (random.randint(-5,5), random.randint(-5,5), random.randint(-5,5)),
            (random.randint(-5,5), random.randint(-5,5), random.randint(-5,5)),
            (random.randint(-5,5), random.randint(-5,5), random.randint(-5,5)),
            (random.randint(-5,5), random.randint(-5,5), random.randint(-5,5)),
            (random.randint(-5,5), random.randint(-5,5), random.randint(-5,5)),
            (random.randint(-5,5), random.randint(-5,5), random.randint(-5,5)),
            (random.randint(-5,5), random.randint(-5,5), random.randint(-5,5)),
            (random.randint(-5,5), random.randint(-5,5), random.randint(-5,5)),
            (random.randint(-5,5), random.randint(-5,5), random.randint(-5,5)),
        )
    for case in assert_test:
        case_pt = Point(*case)
        red = case_pt.reduce()
        for _ in range(48):
            if random.random() < 0.5:
                case_pt.rot_yz()
            else:
                case_pt.neg_xy()
            shifted = case_pt.reduce()
            assert shifted == red, f"\n{shifted=	}\n{red=		}\n{case_pt=	}"

@dataclass
class Scanner:
    name: str
    beacons: List[Point]
    sentinel: Point = None
    offset: Point = None

    def __post_init__(self):
        self.sentinel = Point(1,2,3)
        self.offset = Point(0,0,0)

    def __matmul__(self, other):
        return self.offset - other.offset

    def __int__(self):
        return int(self.offset)

    def adjust(self):
        return (*self.beacons, self.sentinel, self.offset)

    def rot_xy(self):
        [entry.rot_xy() for entry in self.adjust()]
    def rot_yz(self):
        [entry.rot_yz() for entry in self.adjust()]
    def rot_zx(self):
        [entry.rot_zx() for entry in self.adjust()]
    def rot_yx(self):
        [entry.rot_yx() for entry in self.adjust()]
    def rot_zy(self):
        [entry.rot_zy() for entry in self.adjust()]
    def rot_xz(self):
        [entry.rot_xz() for entry in self.adjust()]
    def neg_xy(self):
        [entry.neg_xy() for entry in self.adjust()]
    def neg_yz(self):
        [entry.neg_yz() for entry in self.adjust()]
    def neg_xz(self):
        [entry.neg_xz() for entry in self.adjust()]

    def add_offset(self, offset):
        offset -= self.offset
        for b in self.beacons:
            b += offset
        self.offset += offset

    def extend(self, vals):
        if isinstance(vals, Scanner):
            return self.extend(vals.beacons)
        if isinstance(vals, Point):
            assert False, f"Got Point in call to Scanner.extend(): {vals}"
        if isinstance(vals, List):
            for val in vals:
                assert isinstance(val, Point), f"Got non-Point in call to Scanner.extend();\n\n{'*'*20}\n{val}\n{'*'*20}"
                self.beacons.append(Point(val.x, val.y, val.z))

    def astuple(self):
        assert len(self.beacons)
        ret = self.name, self.beacons[0].astuple()
        assert ret[1] in map_astuple(self), f"Couldn't find self in `astuple` call {ret}\n{ret[1]=}\n\n{chr(10).join(map(str, sorted(map_astuple(self))))}"
        return ret

def get_edge_deltas(scanner):
    edge_set = set()
    for beacon in scanner.beacons:
        x, y, z = beacon.x, beacon.y, beacon.z
        for oct in range(8):
            xf = oper.ge if oct & 1 else oper.le
            yf = oper.ge if oct & 2 else oper.le
            zf = oper.ge if oct & 4 else oper.le
            side_beacons = [*filter(lambda other: xf(x, other.x) and yf(y, other.y) and zf(z, other.z), scanner.beacons)]
            if len(side_beacons) < 5:
                # Set to "< 4" to assume 1 point might be missing, but not too many missing
                for a, b in permutations((beacon, *side_beacons), 2):
                    if a == b: continue
                    if xf(a.x, b.x) and yf(a.y, b.y) and zf(a.z, b.z):
                        delta = a - b
                        edge_set.add((
                                delta.reduce().astuple(),
                                delta.astuple(),
                                a.astuple(),
                                b.astuple(),
                            ))

    return edge_set

def map_astuple(scanner):
    return {*map(lambda x:x.astuple(), scanner.beacons),}

def d19(inp, sample=False):
    # Convert input into data structures
    scanners_proc = {}
    for scanner_inp in inp.split('\n\n'):
        scan_iter = iter(scanner_inp.split('\n'))
        scanner_inp_name = next(scan_iter).strip('- ')
        points = [Point(*map(int, line.split(','))) for line in scan_iter]
        scanners_proc[scanner_inp_name] = Scanner(scanner_inp_name, points)

    # Set origin and orientation based on 'scanner 0' if present, else pick arbitrarily
    scanner_0 = 'scanner 0'
    if scanner_0 in scanners_proc:
        base_k, base_v = scanner_0, scanners_proc.pop(scanner_0)
    else:
        base_k,base_v = scanners_proc.popitem()

    # Create groupings of "solved" scanners

    # Scanner holding solved solution
    assembled = set() #Scanner('assembled', [])
    # Mapping of name to solved version of Scanner
    in_assembled = {}
    # Mapping of reduced deltas to set of containing (solved) Scanners
    edge_to_scanner_sets = defaultdict(set)
    # Mapping from (scanner_name, (delta_start_point)) to full delta entry
    scanner_edges = {}

    assembled.update(map_astuple(base_v))
    in_assembled[base_k] = base_v
    base_deltas = get_edge_deltas(base_v)
    for b_delta in base_deltas:
        edge_to_scanner_sets[b_delta[0]].add(base_k)
        scanner_edges[base_k, b_delta[0]] = b_delta
    del base_k
    del base_v

    # Map (scanner_name, Scanner.beacons[0].astuple()) (latter to ensure mutations not silent)
    edge_delta_cache = {}
    for scanner_k, scanner_v in scanners_proc.items():
        edge_delta_cache[scanner_v.astuple] = get_edge_deltas(scanner_v)
        #for scanner_result in scanner_edges_results:
        #    scanner_edges[scanner_k, scanner_result[0]] = scanner_result

    stalled = False
    # While not everything is assembled
    while scanners_proc:
        scanner_t = None
        assert stalled == False
        stalled = True
        for scanner_k, orig_scanner_v in [*scanners_proc.items()]:
            # Invalid after rotation
            scanner_t = orig_scanner_v.astuple()
            scanner_v = copy.deepcopy(orig_scanner_v)
            # add lazily
            if scanner_t not in edge_delta_cache:
                edge_delta_cache[scanner_t] = get_edge_deltas(orig_scanner_v)
            delta_set = {*edge_delta_cache[scanner_t]}
            while delta_set:
                delta = delta_set.pop()
                if delta[0] not in edge_to_scanner_sets:
                    continue
                others = edge_to_scanner_sets[delta[0]]
                for other_k in [*others]:
                    if other_k == scanner_k or scanner_k in in_assembled:
                        assert stalled == False
                        break
                    if scanner_t is None:
                        scanner_v = copy.deepcopy(orig_scanner_v)
                        scanner_t = scanner_v.astuple()
                    assert scanner_t[1] in map_astuple(scanner_v), f"\n{scanner_t=}\n\n{scanner_t in edge_delta_cache=}\n\n{scanner_t[1]=}\n\n{scanner_v}"
                    assert delta[2] in map_astuple(scanner_v), f"\n{delta=}\n\n{delta[2]=}\n\n{scanner_t=}\n\n{scanner_v}"
                    assert delta[3] in map_astuple(scanner_v), f"\n{delta=}\n\n{delta[3]=}\n\n{scanner_t=}\n\n{scanner_v}"
                    other_v = in_assembled[other_k]
                    my_delta = Point(*delta[1])
                    other_delta = Point(*scanner_edges[other_k, delta[0]][1])
                    corner_point = Point(*delta[2])
                    corner_friend = Point(*delta[3])
                    rot_group = [scanner_v, my_delta, corner_point, corner_friend]
                    def checks():
                        assert corner_point in scanner_v.beacons
                        assert corner_friend in scanner_v.beacons
                        assert my_delta.reduce() == other_delta.reduce(), f"\n{my_delta.reduce()=}\t{my_delta.astuple()}\n{other_delta.reduce()=}\t{other_delta.astuple()}"
                    assert my_delta.reduce() == other_delta.reduce()
                    scanner_t = None
                    if abs(other_delta.x) != abs(my_delta.x):
                        if abs(other_delta.x) == abs(my_delta.y):
                            [entry.rot_yx() for entry in rot_group]
                        else:
                            [entry.rot_zx() for entry in rot_group]
                        checks()
                    assert abs(other_delta.x) == abs(my_delta.x)
                    if abs(other_delta.y) != abs(my_delta.y):
                        [entry.rot_yz() for entry in rot_group]
                        checks()
                    assert abs(other_delta.x) == abs(my_delta.x)
                    assert abs(other_delta.y) == abs(my_delta.y)
                    assert abs(other_delta.z) == abs(my_delta.z)
                    if other_delta.x != my_delta.x:
                        if other_delta.y != my_delta.y:
                            [entry.neg_xy() for entry in rot_group]
                            checks()
                        else:
                            [entry.neg_xz() for entry in rot_group]
                            checks()
                    assert my_delta.x == other_delta.x
                    checks()
                    if other_delta.y != my_delta.y:
                        [entry.neg_yz() for entry in rot_group]
                    assert my_delta.x == other_delta.x
                    assert my_delta.y == other_delta.y, f"{my_delta=}; {other_delta}"
                    checks()

                    if other_delta.z != my_delta.z:
                        # Parity difference, either a zero or duplicates exist
                        if my_delta.x == 0:
                            [entry.neg_xz() for entry in rot_group]
                        elif abs(my_delta.x) == abs(my_delta.y):
                            [entry.rot_xy() for entry in rot_group]
                            [entry.neg_yz() for entry in rot_group]
                        elif abs(my_delta.x) == abs(my_delta.z):
                            [entry.rot_xz() for entry in rot_group]
                            assert my_delta.x == other_delta.x
                        else:
                            assert False, f"\n{my_delta=}\n{other_delta=}"

                    checks()
                    assert my_delta == other_delta, f"{my_delta=} --- {other_delta=}"
                    dest = Point(*scanner_edges[other_k, delta[0]][2])
                    offset = dest - corner_point
                    corner_point += offset
                    scanner_v.add_offset(offset)
                    assert corner_point in scanner_v.beacons
                    intersection = map_astuple(scanner_v) & map_astuple(other_v)
                    if len(intersection) >= 12:
                        stalled = False
                        delta_set.clear()
                        assert scanner_k in scanners_proc
                        scanners_proc.pop(scanner_k)
                        assembled.update(map_astuple(scanner_v))
                        in_assembled[scanner_k] = scanner_v
                        base_deltas = get_edge_deltas(scanner_v)
                        for b_delta in base_deltas:
                            edge_to_scanner_sets[b_delta[0]].add(scanner_k)
                            scanner_edges[scanner_k, b_delta[0]] = b_delta
                        break

    p1 = len(assembled)
    p2 = max(map(int, map(lambda x:x[0] @ x[1], combinations(in_assembled.values(), 2))))

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d19(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d19.txt') as f:
        inp = f.read().strip()
    return d19(inp)

if __name__ == '__main__':

    # Testing problem properties

    cases = [
        #(id, inp, p1, p2),
        (0, """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14""", 79, 3621),
    ]

    #"""
    # Non multiprocessing version
    run_safety_checks()
    for case in cases:
        validate_test(*case)
    p1, p2 = main()
    assert p1 == 472
    assert p2 == 12092
    print(f"p1 = {p1}\np2 = {p2}")


    """
    with Pool(processes=min(8, len(cases) + 2)) as pool:
        validation = pool.apply_async(run_safety_checks)
        main_res = pool.apply_async(main)
        test_res = [pool.apply_async(validate_test, case) for case in cases]
        test_pass, do_p1, do_p2 = True, False, False
        for test in test_res:
            tp, dp1, dp2 = test.get(30)
            test_pass &= tp
            do_p1 |= dp1
            do_p2 |= dp2
        validation.get(30)
        if test_pass:
            p1, p2 = main_res.get(60)
            assert do_p1 or do_p2, "Didn't run any tets"
            assert p1 is None or do_p1 == True, "Got P1 value without 'do_p1' set"
            assert p2 is None or do_p2 == True, "Got P2 value without 'do_p2' set"
            assert p1 == 472
            assert p2 == 12092
            print(f"p1 = {p1}\np2 = {p2}")
    #"""
