from collections import defaultdict, Counter, deque
from dataclasses import dataclass
from functools import cache
from itertools import product, pairwise, permutations
from multiprocessing import Pool
import copy
import math
import re
import operator as oper
from typing import List, Set, Any, Dict

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

major_set = frozenset({'x', 'y', 'z'})

@dataclass
class Orientation:
    sign: int
    major: string

    def check(self):
        assert abs(sign) == 1
        assert major in ('x', 'y', 'z')

@dataclass(order=True)
class Point:
    x: int = 0
    y: int = 0
    z: int = 0

    def rot_front(self):
        self.x, self.z = self.z, -self.x

    def rot_top(self):
        self.y, self.z = self.z, -self.y

    def rot_pos(self):
        self.x, self.y, self.z = self.y, self.z, self.x

    def rot_neg_xy(self):
        self.x, self.y = -self.x, -self.y

    def rot_xy_swap(self):
        self.x, self.y = self.y, -self.x

    def rot_neg_yz(self):
        self.y, self.z = -self.y, -self.z

    def rot_yz_swap(self):
        self.y, self.z = self.z, -self.y

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

    def __neg__(self, other):
        return Point(
                -self.x,
                -self.y,
                -self.z
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

    def reduce(self):
        red = Point(self.x, self.y, self.z)
        if abs(red.y) > abs(red.z):
            red.rot_yz_swap()
        if abs(red.x) > abs(red.y):
            red.rot_xy_swap()
        if red.x < 0:
            red.rot_neg_xy()
        if red.y < 0:
            red.rot_neg_yz()
        if red.z < 0 and red.x == 0:
            print(f"Have zeros:\n0\t{red.astuple()}")
            if red.y == 0:
                red.rot_neg_yz()
                print(f"1\t{red.astuple()}\nEnd case y == 0")
                assert red.x == 0
                assert red.y == 0
                assert red.z > 0
            elif red.x == 0:
                red.rot_neg_xy()
                print(f"1\t{red.astuple()}")
                red.rot_neg_yz()
                print(f"2\t{red.astuple()}")
                assert red.x == 0
                assert red.y > 0
                assert red.z > 0
        return red

    def astuple(self):
        return (self.x, self.y, self.z)

@dataclass
class Scanner:
    name: str
    beacons: List[Point]
    sentinel: Point = None
    offset: Point = None
    deltas: Dict[Point, Set[Point]] = None

    def __post_init__(self):
        assert self.deltas is None, "Don't set deltas. TODO: Use dataclass fields entry"
        self.deltas = {}
        self.sentinel = Point(1,2,3)
        self.offset = Point(0,0,0)

    def __str__(self):
        # Pretty print
        """
        Scanner(
                name='scanner 1',
                beacons=[
                        Point(x=686, y=422, z=578),
                        Point(x=605, y=423, z=415),
                        Point(x=515, y=917, z=-361),
                        Point(x=-336, y=658, z=858), Point(x=95, y=138, z=22), Point(x=-476, y=619, z=847),
                        Point(x=-340, y=-569, z=-846), Point(x=567, y=-361, z=727), Point(x=-460, y=603, z=-452),
                        Point(x=669, y=-402, z=600), Point(x=729, y=430, z=532), Point(x=-500, y=-761, z=534),
                        Point(x=-322, y=571, z=750), Point(x=-466, y=-666, z=-811), Point(x=-429, y=-592, z=574),
                        Point(x=-355, y=545, z=-477), Point(x=703, y=-491, z=-529), Point(x=-328, y=-685, z=520), Point(x=413, y=935, z=-424), Point(x=-391, y=539, z=-444), Point(x=586, y=-435, z=557), Point(x=-364, y=-763, z=-893), Point(x=807, y=-499, z=-711), Point(x=755, y=-354, z=-619),
                        Point(x=553, y=889, z=-390)
                    ],
                sentinel=Point(x=1, y=2, z=3),
                offset=Point(x=0, y=0, z=0),
                deltas={}
            )
        """
        tab = '  '
        nl = '\n'
        return f"Scanner(\n{tab*2}name={self.name!r},\n{tab*2}beacons=[\n{tab*4}{(','+nl+tab*4).join(map(str, sorted(self.beacons)))}\n{tab*3}],\n{tab*2}sentinel={self.sentinel},\n{tab*2}offset={self.offset},\n{tab*2}deltas={self.deltas}\n{tab*1})"

    def rot_front(self):
        for b in self.beacons:
            b.rot_front()
        self.sentinel.rot_front()

    def rot_top(self):
        for b in self.beacons:
            b.rot_top()
        self.sentinel.rot_top()

    def rot_pos(self):
        for b in self.beacons:
            b.rot_pos()
        self.sentinel.rot_pos()

    def rot_neg_xy(self):
        for b in self.beacons:
            b.rot_neg_xy()
        self.sentinel.rot_neg_xy()

    def rot_xy_swap(self):
        for b in self.beacons:
            b.rot_xy_swap()
        self.sentinel.rot_xy_swap()

    def rot_neg_yz(self):
        for b in self.beacons:
            b.rot_neg_yz()
        self.sentinel.rot_neg_yz()

    def rot_yz_swap(self):
        for b in self.beacons:
            b.rot_yz_swap()
        self.sentinel.rot_yz_swap()

    def get_deltas(self, cols):
        if (cols, self.sentinel) in self.deltas:
            return self.deltas[cols, self.sentinel]
        pass

    def add_offset(self, offset):
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
                                scanner.name
                            ))

    #print(edge_to_scanner_sets)
    return edge_set

def map_astuple(scanner):
    return {*map(lambda x:x.astuple(), scanner.beacons),}

def d19(inp, sample=False):
    p1, p2 = 0, None
    tab = '  '

    # Convert input into data structures
    scanners_proc = {}
    for scanner_inp in inp.split('\n\n'):
        scan_iter = iter(scanner_inp.split('\n'))
        scanner_inp_name = next(scan_iter).strip('- ')
        points = [Point(*map(int, line.split(','))) for line in scan_iter]
        #print(scanner_name, '', *points, sep='\n')
        scanners_proc[scanner_inp_name] = Scanner(scanner_inp_name, points)
        #print(scanners_proc)

    # Fix '--- scanner 0 ---' to (0, 0, 0) if present, else pick arbitrarily
    scanner_0 = 'scanner 0'
    if scanner_0 in scanners_proc:
        base_k, base_v = scanner_0, scanners_proc.pop(scanner_0)
    else:
        base_k,base_v = scanners_proc.popitem()

    # Create groupings of "solved" scanners

    # Scanner holding solved solution
    assembled = Scanner('assembled', [])
    # Mapping of name to solved version of Scanner
    in_assembled = {}
    # Mapping of reduced deltas to set of containing (solved) Scanners
    edge_to_scanner_sets = defaultdict(set)
    # Mapping from (scanner_name, (delta_start_point)) to full delta entry
    scanner_edges = {}

    assembled.extend(base_v)
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

    # While not everything is assembled
    while scanners_proc:
        print(f"****trace**** Top of `while scanners_proc:` @289")
        print(f"\tStarting scanners_proc loop {len(scanners_proc)=}; {scanners_proc.keys()=}")
        scanner_t = None
        for scanner_k, scanner_v in [*scanners_proc.items()]:
            print(f"{tab*1}****trace**** Top of `for scanner_k, scanner_v in [*scanners_proc.items()]:` @293")
            copy_scanner_v = copy.deepcopy(scanner_v)
            scanner_t = None
            # Invalid after rotation
            scanner_t = scanner_v.astuple()
            copy_scanner_t = copy.deepcopy(scanner_t)
            # add lazily
            if scanner_t not in edge_delta_cache:
                print(f"{tab*1}\tExpanding {scanner_k=} for {scanner_t=}")
                edge_delta_cache[scanner_t] = get_edge_deltas(scanner_v)
            else:
                print(f"{tab*1}\tFound cached {scanner_t=}")
            for delta in edge_delta_cache[scanner_t]:
                #print(f"{tab*2}****trace**** Top of `for delta in edge_delta_cache[scanner_t]:` @306")
                if scanner_t is None:
                    scanner_v = copy.deepcopy(copy_scanner_v)
                    scanner_t = scanner_v.astuple()
                    assert scanner_t == copy_scanner_t
                assert scanner_t is not None
#                print(f"\n{scanner_t=}")
#                print(f"\n{scanner_t in edge_delta_cache=}")
#                print(f"\n{scanner_t[1]=}")
#                print(f"\n{scanner_v}")
                assert scanner_t[1] in map_astuple(scanner_v), f"\n{scanner_t=}\n\n{scanner_t in edge_delta_cache=}\n\n{scanner_t[1]=}\n\n{scanner_v}"
                assert delta[2] in map_astuple(scanner_v), f"\n{delta=}\n\n{delta[2]=}\n\n{scanner_t=}\n\n{scanner_v}"
                assert delta[3] in map_astuple(scanner_v), f"\n{delta=}\n\n{delta[3]=}\n\n{scanner_t=}\n\n{scanner_v}"
                if delta[0] not in edge_to_scanner_sets:
                    #print(f"{tab*2}\t{delta[0]=} not found in `edge_to_scanner_sets` @320")
                    #print(f"{tab*2}****trace**** End of `for delta in edge_delta_cache[scanner_t]:` @321")
                    continue
                others = edge_to_scanner_sets[delta[0]]
                nl = '\n'
                #print(f"Others found from {scanner_k} : {others=}")
                for other_k in [*others]:
                    print(f"{tab*3}****trace**** Top of `for other_k in [*others]:`")
                    if scanner_t is None:
                        scanner_v = copy.deepcopy(copy_scanner_v)
                        scanner_t = scanner_v.astuple()
                    assert scanner_t == copy_scanner_t
                    assert scanner_t[1] in map_astuple(scanner_v), f"\n{scanner_t=}\n\n{scanner_t in edge_delta_cache=}\n\n{scanner_t[1]=}\n\n{scanner_v}"
                    assert delta[2] in map_astuple(scanner_v), f"\n{delta=}\n\n{delta[2]=}\n\n{scanner_t=}\n\n{scanner_v}"
                    assert delta[3] in map_astuple(scanner_v), f"\n{delta=}\n\n{delta[3]=}\n\n{scanner_t=}\n\n{scanner_v}"
                    other_v = in_assembled[other_k]
#                    print(f"found {delta=} between\n{scanner_k=}\n{scanner_v=}\n\nand\n\n{other_v=}\n\n\n{nl.join(map(str, sorted(scanner_v.beacons)))}\n\n{nl.join(map(str, sorted(other_v.beacons)))}\n\n{delta}")
                    #print(f"{delta}\n\n{scanner_edges[other_k, delta[0]]}\n")
                    my_delta = Point(*delta[1])
                    other_delta = Point(*scanner_edges[other_k, delta[0]][1])
                    corner_point = Point(*delta[2])
                    corner_friend = Point(*delta[3])
                    rot_group = [scanner_v, my_delta, corner_point, corner_friend]
                    print(f"tfm:\tTrying to make\t{my_delta=} to {other_delta}")
                    assert my_delta.reduce() == other_delta.reduce()
                    scanner_t = None
                    assert corner_point in scanner_v.beacons
                    assert corner_friend in scanner_v.beacons
                    if abs(other_delta.x) != abs(my_delta.x):
                        if abs(other_delta.x) == abs(my_delta.z):
                            for entry in rot_group:
                                entry.rot_yz_swap()
                            assert corner_point in scanner_v.beacons
                            assert corner_friend in scanner_v.beacons
                        for entry in rot_group:
                            entry.rot_xy_swap()
                        assert corner_point in scanner_v.beacons
                        assert corner_friend in scanner_v.beacons
                    print(f"\tFixed abs(x)?\t{my_delta=} ~= {other_delta}")
                    if other_delta.x != my_delta.x:
                        for entry in rot_group:
                            entry.rot_neg_xy()
                    assert corner_point in scanner_v.beacons
                    assert corner_friend in scanner_v.beacons
                    print(f"\tProgress\t{my_delta=} ~= {other_delta}")
                    assert my_delta.reduce() == other_delta.reduce(), f"\n{my_delta.reduce()=}\n{other_delta.reduce()=}"
                    if abs(other_delta.y) != abs(my_delta.y):
                        for entry in rot_group:
                            entry.rot_yz_swap()
                    assert corner_point in scanner_v.beacons
                    assert corner_friend in scanner_v.beacons
                    assert my_delta.reduce() == other_delta.reduce()
                    if other_delta.y != my_delta.y:
                        for entry in rot_group:
                            entry.rot_neg_yz()
                    assert corner_point in scanner_v.beacons
                    assert corner_friend in scanner_v.beacons
                    assert my_delta.reduce() == other_delta.reduce()
                    # A zero is unsigned and gives more degrees of freedom
                    if my_delta.x == 0:
                        if my_delta.z != other_delta.z:
                            [entry.rot_neg_yz() for entry in rot_group]
                        if my_delta.y != other_delta.y:
                            [entry.rot_neg_xy() for entry in rot_group]
                    print(f"\tFixed?\t\t{my_delta=} == {other_delta}")
                    assert my_delta == other_delta, f"{my_delta=} --- {other_delta=}"
                    #print(f"found {delta=} between\n{scanner_k=}\n{scanner_v=}\n\nand\n\n{other_v=}\n\n\n{nl.join(map(str, sorted(scanner_v.beacons)))}\n\n{nl.join(map(str, sorted(other_v.beacons)))}\n\n{delta}")
                    #print(f"{corner_point=} offseting to {Point(*scanner_edges[other_k, delta[0]][2])}")
                    dest = Point(*scanner_edges[other_k, delta[0]][2])
                    offset = dest - corner_point
                    corner_point += offset
                    scanner_v.add_offset(offset)
                    assert corner_point in scanner_v.beacons
#                    print(f"found {delta=} between\n{scanner_k=}\n{scanner_v=}\n\nand\n\n{other_v=}\n\n\n{nl.join(map(str, sorted(scanner_v.beacons)))}\n\n{nl.join(map(str, sorted(other_v.beacons)))}\n\n{delta}")
#                    print(f"(updated){corner_point=} offseting to {Point(*scanner_edges[other_k, delta[0]][2])}")
                    intersection = map_astuple(scanner_v) & map_astuple(other_v)
                    print(f"Intersection of scanner_v={scanner_v.name} mapped onto other_v={other_v.name}; {len(intersection)=}\n\t{(','+nl+chr(9)).join(map(str, sorted(intersection)))}\n")
                    if len(intersection) >= 12:
                        print(f"\tMatch found!!! {scanner_v.name} mapped onto {other_v.name} @ {len(intersection)} points\n\t{offset=}\n")
                        assert scanner_k in scanners_proc
                        scanners_proc.pop(scanner_k)
                        assembled.extend(scanner_v)
                        in_assembled[scanner_k] = scanner_v
                        base_deltas = get_edge_deltas(scanner_v)
                        for b_delta in base_deltas:
                            edge_to_scanner_sets[b_delta[0]].add(scanner_k)
                            scanner_edges[scanner_k, b_delta[0]] = b_delta
                        print(f"{tab*4}****trace**** End of `for other_k in [*others]:` 399")
                        break
                    else:
#                        print(f"Near match, got {len(intersection)} which is <12\n\t{(','+nl+chr(9)).join(map(str, intersection))}")
                        if scanner_k == 'scanner 2' and other_k == 'scanner 1':
#                            print(scanner_v)
#                            print(other_v)
                            print([*sorted(map_astuple(scanner_v))])
                            print([*sorted(map_astuple(other_v))])
                    print(f"{tab*3}****trace**** End of `for other_k in [*others]:` 408")
                else: # for other_k in others # nobreak (no matches found
                    print(f"{tab*3}****trace**** End of `for other_k in [*others]:` 410")
                    continue # to next scanner_{k,v}
                print(f"{tab*2}****trace**** End of `for other_k in [*others]:` 412")
                print(f"{tab*2}\tBreaking Twice")
                break # break two levels
            else:
                print(f"{tab*1}****trace**** End of `for scanner_k, scanner_v in [*scanners_proc.items()]:` @416")
                continue
            print(f"{tab*1}****trace**** End of `for scanner_k, scanner_v in [*scanners_proc.items()]:` @418")
            break # Break three levels
        else: # for scanner_k, scanner_v in [*scanners_proc.items()]
            assert len(scanners_proc) == 0, f"Thought I would have found something; {len(scanners_proc)} left {scanners_proc.keys()}" #\n{edge_to_scanner_sets}\n\n\n{scanner_edges}"
        print(f"{tab*0}****trace**** end of loop")
    # End while scanners_proc

    p1 = len(map_astuple(assembled))

    p2 = 0
    for ak, av in in_assembled.items():
        for bk, bv in in_assembled.items():
            if ak == bk:
                continue
            dist = sum(map(abs, map(lambda x:oper.sub(*x), zip(av.offset.astuple(), bv.offset.astuple()))))
            p2 = max(dist, p2)

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
    """
