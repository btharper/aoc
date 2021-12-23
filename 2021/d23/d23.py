from collections import defaultdict, Counter, deque
from functools import cache, partial
from itertools import product, pairwise
from multiprocessing import Pool
import math
import re
from dataclasses import dataclass, field
import heapq as hq
from pprint import pprint

non_digits = re.compile('[^0-9]+')
def sign(a, b, step=1):
    return int(math.copysign(step, b-a))
def autorange(a,b, step=1):
    if a == b:return (a,)
    s = sign(a, b, step)
    return range(a, b+s, s)

@dataclass(order=True)
class Line:
    x: int
    y: int
    want: int = None
    have: list[int] = field(default_factory=deque)
    depth: list[int] = field(default_factory=deque)
    open: bool = True
    total: int = 2
    name: string = None

    def as_tuple(self):
        return ((*self.have,), (*self.depth,), self.total, self.open, self.want, self.x, self.y, self.name)

    def copy(self):
        ret = Line(
                self.x, self.y,
                want=self.want,
                have=deque(self.have),
                depth=deque(self.depth),
                open=self.open,
                total=self.total,
                name=self.name,
            )
        return ret

    def append_tail(self, val):
        assert len(self.have) + 1 <= self.total
        # Only to be called during init
        self.have.append(val)
        self.depth.append(len(self.depth))
        if self.want is not None and val != self.want:
            # Side (bottom) rooms
            self.open = False

    def pop(self):
        assert len(self.depth) == len(self.have)
        assert len(self.have) > 0
        # Returns (pop_item, pop_cost)
        cost = self.have[0] * self.depth.popleft()
        if len(self.depth) == 0:
            self.open = True
        return self.have.popleft(), cost

    def push(self, val):
        assert self.want is None or self.want == val
        assert len(self.depth) == len(self.have)
        assert self.open
        assert len(self.have) < self.total
        # Returns cost
        cost = 0
        self.have.appendleft(val)
        self.depth.appendleft(0)
        for i,v in enumerate(self.depth):
            if v < i:
                self.depth[i] += 1
                assert self.depth[i] == i
                cost += self.have[i]
        return cost

    def full(self):
        return len(self.have) == self.total
    def empty(self):
        return len(self.have) == 0

@dataclass
class Pod:
    val: int
    cost: int = 0 #Really no_init

    def __post_init__(self):
        self.cost = pow(10, val)

def burrow_halls():
    hall = []
#    hall.append(Line(x=0, y=0, want=None,  total=1, name=f"Left-L"))
    hall.append(Line(x=1, y=0, want=None,  total=2, name=f"Left-R"))
    hall.append(Line(x=3, y=0, want=None,  total=1, name=f"Hall L"))
    hall.append(Line(x=5, y=0, want=None,  total=1, name=f"Hall M"))
    hall.append(Line(x=7, y=0, want=None,  total=1, name=f"Hall R"))
    hall.append(Line(x=9, y=0, want=None,  total=2, name="Right-L"))
#    hall.append(Line(x=10, y=0, want=None, total=1, name="Right-R"))
    return hall

def burrow_homes():
    home = []
    home.append(Line(x=2, y=1, want=1,    name=f"Home A (1)"))
    home.append(Line(x=4, y=1, want=10,   name=f"Home B (10)"))
    home.append(Line(x=6, y=1, want=100,  name=f"Home C (100)"))
    home.append(Line(x=8, y=1, want=1000, name=f"Home D (1000)"))
    return home


@dataclass(order=True)
class Burrow:
    hall: list[Line] = field(default_factory=burrow_halls)
    home: list[Line] = field(default_factory=burrow_homes)

    def cap_homes(self):
        for line in self.home:
            while line.have[-1] == line.want:
                line.have.pop()
                line.depth.pop()
                line.total -= 1

    def shallow_copy(self):
        return Burrow([*self.hall,], [*self.home,])

    def _list_as_tuple(self, src_list):
        return (*map(lambda x:x.as_tuple(), src_list),)

    def as_tuple(self):
        return (self._list_as_tuple(self.hall), self._list_as_tuple(self.home))

    def h(self):
        val = 0
        # For stacks with depth (hall), include depth + distance
        for line in self.hall:
            for pod, depth in zip(line.have, line.depth):
                tx, ty = targets[pod]
                dist = abs(line.x-tx) + abs(line.y-ty) + depth
                val += dist * pod
        # For homes, distance inclues entering/exiting the hallway
        for line in self.home:
            for pod, depth in zip(line.have, line.depth):
                if line.want == pod:
                    continue
                tx, ty = targets[pod]
                # +2 for in and back out of the hallway
                dist = abs(line.x-tx) + abs(line.y-ty) + 2 + depth
                val += dist * pod
        return val

log_map = {1:1, 10:2, 100:3, 1000:4}
pow_map = {1:1, 2:10, 3:100, 4:1000}
targets = {1:(1,1), 10:(3,1), 100:(5,1), 1000:(7,1)}

def d23(inp, sample=False):
    inp2 = "##\n  #D#C#B#A#\n  #D#B#A#C#\n  #".join(inp.split('##\n  #'))
#    print(inp)
#    print('\n\n')
#    print(inp.split('\n  #'))
#    print('\n\n')
#    print(inp2)
    p1 = solution(inp)
    p2 = solution(inp2, total=4)
    assert p1 is not None
    assert p2 is not None
    return p1, p2


def solution(inp, total=2):
    soln = None
    burrow = Burrow()
    for line in burrow.home:
        line.total = total
    for line in filter(None, map(lambda s: s.strip(' .#'), inp.split('\n'))):
        #print(f"{line=}")
        for i, val in enumerate(map(lambda c: ord(c) - ord('A'), line.split('#'))):
#            print(f"From {line=} {i=} is {val=}", end='')
#            print(f"({chr(val + ord('A'))})")
            burrow.home[i].append_tail(pow(10, val))
    burrow.cap_homes()

#    print(burrow)
#    print(*burrow.home, sep='\n')

    stack = []
    #(fscore, gscore, state)
    stack.append((burrow.h(), 0, burrow))
    seen = {}

    while stack:
        # Fetch
        item_fscore, item_gscore, item = hq.heappop(stack)
#        print(item_gscore, [(home_line.open, home_line.full()) for home_line in item.home])
        # Check for termination
        if all(home_line.open and home_line.full() for home_line in item.home):
            print(f"Found result {item_gscore=} {item_fscore=}")
#            pprint(item.home)
#            pprint(item.hall)
            if soln is None or item_gscore < soln:
                soln = item_gscore
            stack = [*filter(lambda x:x[1]<=soln, stack)]
            hq.heapify(stack)
#            stack.clear()
#            break
        # Go through neighbors - All moves are bottom rooms to hall or hall to rooms
        # Hallway to room movement
        for (src_idx, src), (dst_idx, dst) in product(enumerate(item.hall), enumerate(item.home)):
            if src.empty():
                continue
            if not dst.open:
                continue
            pod = src.have[0]
            if dst.want != pod:
                continue
#            dst_idx = log_map[pod] - 1
#            dst = item.home[dst_idx]
            # 01234567890
            # 01 2 3 4 56 - src_idx
            #   0 1 2 3   - dst_idx
#            src_off = (0,1,3,5,7,9,10)[src_idx]
#            dst_off = (2,4,6,8)[dst_idx]
            if any(blocker.full() and (src.x < blocker.x < dst.x or src.x > blocker.x > dst.x) for blocker in item.hall):
                continue
#            if src.x < dst.x and any(blocker.full() and src.x < blocker.x < dst.x for blocker in item.hall):
#                continue
#            elif src.x > dst.x and any(blocker.full() and dst.x < blocker.x < src.x for blocker in item.hall):
#                continue
#            elif src_idx > dst_idx + 2 and any(item.hall[h_i].full() for h_i in range(src_idx-1, dst_idx-1, -1)):
#                continue
#            print(f"Moving from src:{src.name!r} to dst:{dst.name!r}\n{src=}\n\n{dst=}")
            # Reachable, calculate distance
            dist = abs(dst.x-src.x) + abs(dst.y-src.y)
            n_gscore = dist * pod + item_gscore
            # generate next state
            state = item.shallow_copy()
            # Copy
            state.hall[src_idx] = state.hall[src_idx].copy()
            state.home[dst_idx] = state.home[dst_idx].copy()
            assert state.hall[src_idx].have[0] == pod, f"{pod=}\n{state.hall[src_idx].have[0]=}"
            # Pop src / Push dst
            pop_item, pop_cost = state.hall[src_idx].pop()
#            print(f"Popped {pop_item=} for {pop_cost=}")
            # Push dst
            push_cost = state.home[dst_idx].push(pop_item)
            # Add cost
            n_gscore += pop_cost + push_cost
            # Add new node
            n_hscore = state.h()
            n_fscore = n_gscore + n_hscore
#            print(f"Moving from src:{src.name} to dst:{dst.name}\n{item=}\n\n{state=}\n\n{n_fscore=}, {n_gscore=}, {n_hscore=}")
            state_tuple = state.as_tuple()
            if state_tuple not in seen or seen[state_tuple] > n_gscore:
                seen[state_tuple] = n_gscore
                if soln is None or n_gscore <= soln:
                    hq.heappush(stack, (n_fscore, n_gscore, state))
        # Room to Hallway movement
        for (src_idx, src), (dst_idx, dst) in product(enumerate(item.home), enumerate(item.hall)):
            if src.empty() or dst.full():
                continue
            if any(blocker.full() and (src.x < blocker.x < dst.x or src.x > blocker.x > dst.x) for blocker in item.hall):
                continue
            pod = src.have[0]
            if pod == src.want and src.open:
                assert len(src.have) < src.total or src.full()
#                assert src.
                continue
#            print(f"Could travel from room-{src_idx} to hall-{dst_idx}")
            # Calculate distance
            dist = abs(dst.x-src.x) + abs(dst.y-src.y)
            n_gscore = dist * pod + item_gscore
            ### Generate state
            state = item.shallow_copy()
            #print(f"Copied state\n\n{item=}\n\n{state=}")
#            print(f"Copied state")
#            pprint(item)
#            print()
#            pprint(state)
#            print()
            # Copy src/dst
            state.home[src_idx] = state.home[src_idx].copy()
            state.hall[dst_idx] = state.hall[dst_idx].copy()
            # Pop src/push dst
            pop_item, pop_cost = state.home[src_idx].pop()
            push_cost = state.hall[dst_idx].push(pop_item)
#            pprint(state)
#            print()
            # Tabulate
            n_gscore += pop_cost + push_cost
            n_hscore = state.h()
            n_fscore = n_gscore + n_hscore
            # Append
#            print(f"Moving from src:{src.name} to dst:{dst.name}\n{item=}\n\n{state=}\n\n{n_fscore=}, {n_gscore=}, {n_hscore=}")
#            print(f"Moving from src:{src.name} to dst:{dst.name}\n\t{n_fscore=}, {n_gscore=}, {n_hscore=}\n")
#            print([list.full() for list in item.home])
#            print("item {hall,home}")
#            pprint(item.hall)
#            pprint(item.home)
#            print("state {hall,home}")
#            pprint(state.hall)
#            pprint(state.home)
            state_tuple = state.as_tuple()
            if state_tuple not in seen or seen[state_tuple] > n_gscore:
                seen[state_tuple] = n_gscore
                if soln is None or n_gscore < soln:
                    hq.heappush(stack, (n_fscore, n_gscore, state))

    return soln

@cache
def unblocked_paths(src, full):
    assert all(isinstance(full_val, bool) for full_val in full), f"{full}"
    assert 0 <= src <= 3
    # src - room src_idx
    # full - hall full() mapping
    # hall - 01 2 3 4 56
    # room -   0 1 2 3
    res = []
    # To the left
    for i in range(src + 1, -1, -1):
        if full[i]:
            break
        res.append(i)
    # To the right
    for i in range(src + 2, 6, 1):
        if full[i]:
            break
        res.append(i)
    res.sort() # Be fancy!
    return res

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d23(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d23.txt') as f:
        inp = f.read().strip()
    return d23(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""", 12521, 44169),
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
