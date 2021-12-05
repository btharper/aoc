from collections import Counter, deque

with open('../inputs/d07.txt') as f:
    inp = f.read()

bags = {}
max_fan = 0
max_num = 0
for line in inp.split('\n'):
    try:
        inside, others = line.split(' bags contain ')
    except:
        print(line)
    these = Counter()
    for tup in others.split(', '):
        num, typ = tup.strip('.').split(' ', 1)
        if num == 'no' or int(num) == 0:
            continue
        typ = typ.rsplit(' bag', 1)[0]
        these[typ] = int(num)
        max_num = max(max_num, int(num))
    max_fan = max(max_fan, len(these))
    assert inside not in bags or bags[inside] == these, f"{inside}, {bags[inside]}, {these}"
    bags[inside] = these

print(f"{len(bags)=}; {max_num=}; {max_fan=}")

has_shiny_gold = set()
no_gold = set()
for bag in bags:
    if bag in has_shiny_gold or bag in no_gold:
        continue
    seen = set()
    travel = {bag,}
    while travel:
        check = travel.pop()
        seen.add(check)
        if 'shiny gold' in bags[check]:
            has_shiny_gold.add(bag)
            has_shiny_gold.add(check)
            break
        travel.update(set(bags[check]) - seen - no_gold)
    if bag not in has_shiny_gold:
        no_gold |= seen

print(f"p1 {len(has_shiny_gold)}")

within = 0

que = deque()
que.append(('shiny gold', 1))

while que:
    bag, mul = que.popleft()
    for bag_type, bag_count in bags[bag].items():
        que.append((bag_type, mul * bag_count))
        within += bag_count * mul
print(f"p2 {within}")
