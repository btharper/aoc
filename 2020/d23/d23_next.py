from collections import Counter, deque, defaultdict
import re
from dataclasses import dataclass

@dataclass
class Cup:
    num: int
    next: "Cup"

    def next_3(self):
        return (self.next.next.num, self.next.next.next.num, self.next.next.next.next.num)

def d23(inp):
    p1, p2 = None, None

    start_nums = tuple(map(int, inp))
    sorted_nums = list(sorted(start_nums, reverse=True))
    max_num = sorted_nums[0]
    #next_num = dict(zip(sorted_nums, sorted_nums[1:] + sorted_nums[:1]))
    next_num = dict(zip(range(2, 1_000_001), range(1, 1_000_001)))
    next_num[1] = max_num
    assert all(k-v == 1 or k == 1 for k,v in next_num.items())

    nums = [Cup(n, None) for n in range(max(start_nums) + 1)]
    for frm, to in zip(start_nums, start_nums[1:] + start_nums[:1]):
        nums[frm].next = nums[to]
    start = nums[start_nums[0]]
    at = start.next
    #print(f"Cups: {start.num}", end='')
    #while at != start:
        #print(f", {at.num}", end='')
        #at = at.next
    #print()

    cur_cup = nums[start_nums[0]]
    for i in range(100):
        a = cur_cup.next
        b = a.next
        c = b.next
        d = c.next

        three_vals = (a.num, b.num, c.num)
        dest_num = next_num[cur_cup.num]
        while dest_num in three_vals:
            dest_num = next_num[dest_num]
        dest_cup = nums[dest_num]

        c.next = dest_cup.next
        dest_cup.next = a
        cur_cup.next = d
        cur_cup = d
        #print(cur_cup)

    p1 = 0
    cup = nums[1].next
    while cup.num != 1:
        p1 = p1 * 10 + cup.num
        cup = cup.next

    next_num[1] = 1_000_000
    #nums = [Cup(n, None) for n in range(1_000_001)]
    nums = [*range(1_000_001)]
    for frm, to in zip(start_nums + (*range(max_num + 1, 1_000_001),), start_nums[1:] + (*range(max_num + 1, 1_000_001),) + start_nums[:1]):
        nums[frm] = to
    cur_num = start_nums[0]
    for i in range(10_000_000):
        #three_vals = cur_cup.next_3()
        a = nums[cur_num]
        b = nums[a]
        c = nums[b]
        d = nums[c]
        three_vals = a,b,c

        dest_num = next_num[cur_num]
        while dest_num in three_vals:
            dest_num = next_num[dest_num]
        #if 437_490 <= i <= 437_500 and i % 1 == 0:
            #print(f"{i:_}", a,b,c,d, '---', dest_num)
        #dest_cup = nums[dest_num]

        #cur_cup.next.next.next.next, dest_cup.next, cur_cup.next = dest_cup.next, cur_cup.next, cur_cup.next.next.next.next
        #fourth_cup = cur_cup.next.next.next.next
        #cur_cup.next.next.next.next = dest_cup.next
        nums[c] = nums[dest_num]
        #dest_cup.next = cur_cup.next
        nums[dest_num] = a
        #cur_cup.next = fourth_cup
        nums[cur_num] = d
        #cur_cup = cur_cup.next
        cur_num = d

    #print(inp, nums[1], nums[nums[1]])
    p2 = nums[1] * nums[nums[1]]

    return p1, p2

def run_tests():
    cases = [
        #(p1, p2, inp),
        (67384529, 149245887792, "389125467"),
        (25368479, 44541319250, "326519478"),
    ]

    for i, (want_p1, want_p2, inp) in enumerate(cases):
        p1, p2 = d23(inp)
        if want_p1 is not None:
            assert want_p1 == p1, {"want": want_p1, "got": p1, "inp": inp, "idx": i}
        if want_p2 is not None:
            assert want_p2 == p2

def main():
    with open('../inputs/d23.txt') as f:
        inp = f.read().strip()
    p1, p2 = d23(inp)
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    #main()
