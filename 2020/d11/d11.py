from collections import defaultdict
from typing import List
from itertools import product

with open('../inputs/d11.txt') as f:
    inp = f.read()

inp2 = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

#inp = inp2

adjacent = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def num_filled(xy_grid: List[List[str]], max_neighbors: int, vision_range=1) -> int:
    height = len(xy_grid)
    width = len(xy_grid[0])
    if vision_range < 0:
        vision_range = max(height, width)
    ng = {}
    around = defaultdict(int)
    nbrs = defaultdict(set)
    delta = set()
    for y, x in product(range(height), range(width)):
        if grid[y][x] == '.':
            continue
        point = (y,x)
        ng[point] = True
        delta.add(point)
        for dy, dx in adjacent:
            for i in range(1, vision_range+1):
                oy = y + dy * i
                ox = x + dx * i
                if oy < 0 or oy >= height or ox < 0 or ox >= width:
                    break
                if grid[oy][ox] == 'L':
                    around[point] += 1
                    nbrs[point].add((oy,ox))
                    break

    asquare = around.copy()

    while delta:
        changed = delta.copy()
        cg = ng.copy()
        around = asquare.copy()
        delta.clear()
        for point in changed:
            if around[point] == 0 and not cg[point]:
                plus = 1
            elif around[point] >= max_neighbors and cg[point]:
                plus = -1
            else:
                continue
            ng[point] = not cg[point]
            for nbr in nbrs[point]:
                nbr_asquare = asquare[nbr] + plus
                asquare[nbr] = nbr_asquare
                if nbr_asquare >= max_neighbors or nbr_asquare == 0:
                    delta.add(nbr)

    return sum(ng.values())

grid = [list(line) for line in inp.strip().split()]

p1 = num_filled(grid, 4, 1)
p2 = num_filled(grid, 5, -1)
print(f"p1 = {p1}\np2 = {p2}")
