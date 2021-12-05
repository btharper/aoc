with open('../inputs/d10.txt') as f:
    inp = f.read()

inp2 = """16
10
15
5
1
11
7
19
6
12
4"""

inp3 = """3
6
9"""

inp4 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

#inp = inp4
#inp = inp3

jolts = list(map(int, inp.split()))

#print(len(jolts), len(set(jolts)))
jolts.append(0)
jolts.sort()
jolts.append(jolts[-1] + 3)
print(jolts[:10], "")
#assert 0 in jolts
sj = set(jolts)
sj |= {jolts[-1] + 3, }

chg = 0
n1 = 0
n3 = 0
for i, j in enumerate(jolts):
 #   print("Jo", i, j)
    if all(j-k not in jolts for k in range(1,4)):
        continue
    if j + 1 in sj:
        sj.add(j + 1)
  #      print(j, j+1)
        n1 += 1
    if j + 3 in sj:
        sj.add(j + 3)
   #     print(j, j+3)
        n3 += 1

n1 = 0
n3 = 0
for i, j in zip(jolts, jolts[1:]):
    if j-i == 1:
        n1 += 1
    if j-i == 3:
        n3 += 1

from collections import defaultdict

#jolts.sort(reverse=True)
memo = {0:1} #list([1] * len(jolts))
#memo = defaultdict(lambda:1)
combo = 0
ways = 0

for ii, j in enumerate(jolts):
    combo = 0
    for i in range(1, 4):
        if j == i: #memo[j-i] > 0:
            combo += 1
        elif j-i in memo:
            combo += memo[j-i]
        else:
            #print("no find", j-i, "for", j)
            pass
    memo[j] = combo
    ways += combo


p1 = n1 * n3





print(f"p1 = {p1}, {n1}, {n3}")
print(f"p2 = {memo[jolts[-1]]}")
for a,b in zip(memo,jolts):
    print(f"memo[{b}] = {memo[b]}")
