from collections import *

with open('../inputs/d09.txt') as f:
    inp = f.read()

nums = [int(n) for n in inp.split()]

window = deque(nums[:25], 25)
assert len(window) == 25, "Wrong window len"

for num in nums[25:]:
    next_num = False
    for i, ival in enumerate(window):
        for j, jval in enumerate(window):
            if i == j:
                continue
            if ival + jval == num:
                next_num = True
                window.append(num)
                break
        else:
            continue
        break
    else:
        p1 = num
        break

i, j = 0, 1
total = nums[0]
rng = deque(nums[:1])

while total != p1:
    if total < p1:
        total += nums[j]
        rng.append(nums[j])
        j += 1
    elif total > p1:
        total -= nums[i]
        rng.popleft()
        i += 1

#assert sum(rng) == p1
p2 = min(rng) + max(rng)

print(f"p1 = {p1}")
print(f"p2 = {p2}")
