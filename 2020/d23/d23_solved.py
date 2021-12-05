from collections import Counter, deque, defaultdict
import re
from dataclasses import dataclass

@dataclass
class Cup:
    num: int
    next: "Cup"

    def next_3(self):
        return (self.next.num, self.next.next.num, self.next.next.next.num)

    def cut_3(self):
        ret_a = self.next
        ret_b = ret_a.next
        ret_c = ret_b.next
        link = self.next.next.next.next
        self.next.next.next.next = None
        self.next = link
        return ret_a, (ret_a.num, ret_b.num, ret_c.num)

    def paste_3(self, node):
        target = self.next
        self.next = node
        assert node is not None
        assert node.next is not None
        assert node.next.next is not None, node
        node.next.next.next = target

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
        three_vals = cur_cup.next_3()
        dest_num = next_num[cur_cup.num]
        while dest_num in three_vals:
            dest_num = next_num[dest_num]
        dest_cup = nums[dest_num]

        fourth_cup = cur_cup.next.next.next.next
        cur_cup.next.next.next.next = dest_cup.next
        dest_cup.next = cur_cup.next
        cur_cup.next = fourth_cup
        cur_cup = fourth_cup

    p1 = 0
    cup = nums[1].next
    while cup.num != 1:
        p1 *= 10
        p1 += cup.num
        cup = cup.next

    next_num[1] = 1_000_000
    nums = [Cup(n, None) for n in range(1_000_001)]
    for frm, to in zip(start_nums + (*range(max_num + 1, 1_000_001),), start_nums[1:] + (*range(max_num + 1, 1_000_001),) + start_nums[:1]):
        nums[frm].next = nums[to]
    cur_cup = nums[start_nums[0]]
    for i in range(10_000_000):
        three_vals = cur_cup.next_3()
        dest_num = next_num[cur_cup.num]
        while dest_num in three_vals:
            dest_num = next_num[dest_num]
        dest_cup = nums[dest_num]

        #cur_cup.next.next.next.next, dest_cup.next, cur_cup.next = dest_cup.next, cur_cup.next, cur_cup.next.next.next.next
        fourth_cup = cur_cup.next.next.next.next
        cur_cup.next.next.next.next = dest_cup.next
        dest_cup.next = cur_cup.next
        cur_cup.next = fourth_cup
        cur_cup = cur_cup.next

    p2 = nums[1].next.num * nums[1].next.next.num

    return p1, p2

def run_tests():
    cases = [
        #(p1, p2, inp),
        (67384529, 149245887792, "389125467"),
        (25368479, 44541319250, "326519478"),
    ]

    for want_p1, want_p2, inp in cases:
        p1, p2 = d23(inp)
        if want_p1 is not None:
            assert want_p1 == p1
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
