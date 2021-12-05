from collections import ChainMap, Counter, defaultdict, deque

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

def print_grid(grid, neighbors, changed):
    if len(grid) > 20:
        return
    for i in range(len(grid)):
        print(''.join(grid[i]), "  ", ''.join(map(str, neighbors[i])), " ")
    print('\n')

#inp = inp2

sgrid = [list(line) for line in inp.strip().split()]
sheight = len(sgrid)
height = sheight + 2
swidth = len(sgrid[0])
width = swidth + 2

grid = [['.'] + list(row) + ['.'] for row in sgrid]
grid = [['.'] * width] + grid + [['.'] * width]
changed = list([list([True] * width) for row in grid])
neighbors = list([list([0] * width) for row in grid])

clean_grid = [list(row) for row in grid]
clean_changed = [list(row) for row in changed]
clean_neighbors = [list(row) for row in neighbors]

any_changed = True
min_y, max_y = 1, height-1
min_x, max_x = 1, width -1
while any_changed:
    any_changed = False
    ngrid = [list(row) for row in grid]
    nneighbors = [list(row) for row in neighbors]
    nchanged = [list([False] * width) for row in grid]
    nmax_x, nmin_x = 0, width
    nmax_y, nmin_y = 0, height

    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            #print(f"{y=}, {x=}")
            if grid[y][x] == '.' or changed[y][x] == False:
                continue
            adj = neighbors[y][x]
            """
            for dy in range(-1,2):
                for dx in range(-1,2):
                    if grid[y+dy][x+dx] == '#' and (dx != 0 or dy != 0):
                        adj += 1
            """
            if grid[y][x] == 'L' and adj == 0:
                any_changed = True
                ngrid[y][x] = '#'
                nmin_y, nmin_x = min(nmin_y, y), min(nmin_x, x)
                nmax_y, nmax_x = max(nmax_y, y), max(nmax_x, x)
                for dy in range(-1,2):
                    for dx in range(-1,2):
                        if dx != 0 or dy != 0:
                            nchanged[y+dy][x+dx] = True
                            nneighbors[y+dy][x+dx] += 1
            elif grid[y][x] == '#' and adj >= 4:
                any_changed = True
                ngrid[y][x] = 'L'
                nmin_y, nmin_x = min(nmin_y, y), min(nmin_x, x)
                nmax_y, nmax_x = max(nmax_y, y), max(nmax_x, x)
                for dy in range(-1,2):
                    for dx in range(-1,2):
                        if dx != 0 or dy != 0:
                            nchanged[y+dy][x+dx] = True
                            nneighbors[y+dy][x+dx] -= 1
    grid = ngrid
    neighbors = nneighbors
    changed = nchanged
    min_y, max_y = max(nmin_y-1, 1), min(nmax_y, height-1)
    min_x, max_x = max(nmin_x-1, 1), min(nmax_x, width-1)

    min_y, max_y = 1, height - 1
    min_x, max_x = 1, width - 1

    print_grid(grid, neighbors, changed)

"""
### Part 1 to part 2
"""

p1 = sum(sum(seat == '#' for seat in row) for row in grid)
print(f"p1 = {p1}")

grid = clean_grid
changed = clean_changed
#neighbors = clean_neighbors
any_changed = True

visible = {}
tgrid = {}
tneighbors = {}
tchanged = set()

for y in range(height):
    for x in range(width):
        if grid[y][x] == '.':
            continue
        point = (y,x)
        tgrid[point] = '#'
        tchanged.add(point)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                for i in range(1, max(width, height)):
                    oy, ox = y + dy * i, x + dx * i
                    if 0 <= oy < height and 0 <= ox < width:
                        if grid[oy][ox] == 'L':
                            if point not in tneighbors:
                                tneighbors[point] = 0
                                visible[point] = []
                            tneighbors[point] += 1
                            visible[point].append((oy,ox))
                            break
                    else: # Outside bounds
                        break

def print_tgrid(grid, neighbors, changed):
    if len(grid) > 100:
        return
    print(f"len(changed) = {len(changed)}")
    for y in range(height):
        for x in range(width):
            point = (y,x)
            print(grid.get(point, '.'), end='')
        print()
    print('\n')

grid = tgrid.copy()
any_changed = True
changed = tchanged.copy()
tchanged.clear()
neighbors = tneighbors.copy()

while any_changed:
    any_changed = False
    for point in changed:
        delta = 0
        if neighbors[point] == 0 and grid[point] == 'L':
            tgrid[point] = '#'
            delta = 1
        elif neighbors[point] >= 5 and grid[point] == '#':
            tgrid[point] = 'L'
            delta = -1

        if delta != 0:
            any_changed = True
            for npoint in visible[point]:
                tchanged.add(npoint)
                tneighbors[npoint] += delta

    grid = tgrid.copy()
    changed = tchanged.copy()
    tchanged.clear()
    neighbors = tneighbors.copy()
    print_tgrid(grid, neighbors, changed)

p2 = sum(v == '#' for k,v in grid.items())
print(f"p2 = {p2}")
