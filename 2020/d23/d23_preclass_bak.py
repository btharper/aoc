from collections import Counter, deque, defaultdict
import re

def advance_to(deq, num):
    #count = 0
    #while deq[0] != num:
    #    deq.rotate(-1)
    #    count += 1
    count = deq.index(num)
    #count = min(count, count - len(deq), key=abs)
    deq.rotate(-count)
    #assert deq[0] == num, {"count": count, "target":num, "landed": deq[0], "near": tuple([deq[i] for i in range(-10, 11)])}
    #print(f"Advanced {count} places")
    return count

def take_3(deq):
    return deq.popleft(), deq.popleft(), deq.popleft()

def put_3(deq, three):
    for num in three:
        deq.append(num)

def print_head(deq, n=25):
    for i in range(n):
        print(deq[0], end = ', ')
        deq.rotate(-1)
    deq.rotate(n)
    print()

def maybe_predict(nums, last_advance, dest_num):
    #advance_to(nums, dest_num)
    #return
    best_step = None
    best_step_cost = 100
    for step in range(1, 10):
        if len(last_advance) <= step * 3:
            last_advance.append(advance_to(nums, dest_num))
            return
        la_t = (*last_advance,)
        step_cost = max(abs(a - 2*b + c) for a,b,c in zip(la_t, la_t[step:], la_t[2*step:]))
        if step_cost < best_step_cost:
            best_step = step
            best_step_cost = step_cost
        #if all(a-b == c for a, b in zip(last_advance, tuple(last_advance)[step:])):
        #    think_rotate = last_advance[~0] * 2 - last_advance[~step]
        #    nums.rotate(-1 * think_rotate)
        #    if nums[0] == dest_num:
        #        last_advance.append(think_rotate)
        #    else:
        #        #nums.rotate(think_rotate)
        #        nums.rotate(100)
        #        last_advance.append(advance_to(nums, dest_num))
    if best_step is not None:
        think_rotate = last_advance[~0] * 2 - last_advance[~best_step] - (2 * best_step_cost)
        nums.rotate(-1 * think_rotate)
        assert numx.index(dest_num) < 200
    else:
        last_advance.append(advance_to(nums, dest_num))

def d23(inp):
    p1, p2 = None, None

    nums = deque(map(int, inp))
    #print(f"Starting with {' '.join(map(str, nums))}")
    snums = list(sorted(nums, reverse=True))
    next_num = dict(zip(snums, snums[1:] + snums[:1]))
    assert all(k-v == 1 or k == 1 for k,v in next_num.items())

    cur_num = nums[0]
    for i in range(100):
        advance_to(nums, cur_num)
        #print(f"cups: {' '.join(map(str, nums))}")
        nums.rotate(-1)
        three = take_3(nums)
        #print(f"pick up: {', '.join(map(str, three))}")
        n_num = nums[0]
        #print(f"\tnext start is {n_num} : {' '.join(map(str, nums))}")
        dest_num = next_num[cur_num]
        while dest_num in three:
            dest_num = next_num[dest_num]
        #print(f"destination: {dest_num}\n")
        advance_to(nums, dest_num)
        nums.rotate(-1)
        put_3(nums, three)
        cur_num = n_num
    advance_to(nums, 1)
    nums.popleft()
    p1 = int(''.join(map(str, nums)))

    next_num = dict(zip(range(2, 1_000_001), range(1, 1_000_001)))
    next_num[1] = 1_000_000
    assert len(next_num.values()) == len(next_num.keys())
    assert len(next_num.keys()) == 1_000_000
    assert all(k-v == 1 or k == 1 for k,v in next_num.items())

    nums = deque(tuple(map(int, inp)))
    nums.extend(range(snums[0] + 1, 1_000_000+1))
    #print("Starting with: ", end='')
    #print_head(nums, 10)

    last_cur_nums = deque(maxlen=5)
    last_dest_nums = deque(maxlen=5)
    last_three = [deque((-1, -1), maxlen=5) for _ in range(3)]

    last_advance = [deque((-1, -1), maxlen=20) for _ in range(4)]

    cur_num = nums[0]

    print(f"{len(nums):_}")
    for i in range(10_000_000):
        #print(i)
        #if i >= 100:
        #    break
        if (i+0) % 1_000 == 0:
            print(i)
        #if nums[i+4] == cur_num:
        #    nums.rotate(-i-4)
        #else:
        maybe_predict(nums, last_advance[0], cur_num)
        ##last_advance[0].append(advance_to(nums, cur_num))
        #print(f"cups: {' '.join(map(str, nums))}")
        #print_head(nums)
        nums.rotate(-1)
        three = take_3(nums)
        #print(f"pick up: {', '.join(map(str, three))}")
        n_num = nums[0]
        #print(f"\tnext start is {n_num} : {' '.join(map(str, nums))}")
        dest_num = next_num[cur_num]
        while dest_num in three:
            dest_num = next_num[dest_num]
        #print(f"destination: {dest_num}\n")
        #nums.rotate(6+i)
        #if nums[0] != dest_num:
        #    print('pattern break')
        #    advance_to(nums, dest_num)
        maybe_predict(nums, last_advance[1], dest_num)

        #print_head(nums)
        nums.rotate(-1)
        put_3(nums, three)
        #print_head(nums)
        cur_num = n_num
        #last_cur_nums.append(cur_num)
        #last_dest_nums.append(dest_num)
        #print("last_cur_nums =", last_cur_nums)
        #print("last_dest_nums =", last_dest_nums)
        #for i in range(3):
        #    last_three[i].append(three[i])
        #    print(f"last_three[{i}] = {last_three[i]}")
        #for i in range(4):
        #    if last_advance[i]:
        #        print(f"last_advance[{i}] = {last_advance[i]}")
    advance_to(nums, 1)
    nums.rotate(-1)
    assert nums[-1] == 1
    one, two = nums[0], nums[1]
    print(f"{one}, {two}, {one*two}")
    p2 = one * two
    return p1, p2

def run_tests():
    cases = [
        #(p1, p2, inp),
        (67384529, 149245887792, "389125467"),
        (25368479, None, "326519478"),
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
    main()
