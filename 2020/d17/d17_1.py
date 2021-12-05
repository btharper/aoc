from collections import defaultdict
from itertools import product

def count_neighbors_3(cube, x, y, z):
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                count += cube[x+dx,y+dy,z+dz]
    return count

def count_neighbors_4(cube, x, y, z, w):
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                for dw in range(-1, 2):
                    if dx == 0 and dy == 0 and dz == 0 and dw == 0:
                        continue
                    count += cube[x+dx, y+dy, z+dz, w+dw]
    return count

def d17(inp):
    cube = None
    next_cube = defaultdict(bool)
    four_cube = defaultdict(bool)

    transition = [defaultdict(bool),defaultdict(bool)]
    transition[False][3] = True
    transition[True][2] = True
    transition[True][3] = True

    ix, ax = 0, 0
    iy, ay = 0, 0
    iz, az = 0, 0

    for y, line in enumerate(inp.split('\n')):
        for x, char in enumerate(line):
            if char == '#':
                next_cube[x,y,0] = True
                four_cube[x,y,0,0] = True
    iax = ax = max(ax, x)
    iay = ay = max(ay, y)

    for i in range(6):
        cube = next_cube.copy()
        next_cube.clear()
        for x in range(ix-1, ax+2):
            for y in range(iy-1, ay+2):
                for z in range(iz-1, az+2):
                    nbrs = count_neighbors_3(cube, x, y, z)
                    if transition[cube[x,y,z]][nbrs]:
                        next_cube[x,y,z] = True
                        ix, ax = min(ix, x), max(ax, x)
                        iy, ay = min(iy, y), max(ay, y)
                        iz, az = min(iz, z), max(az, z)

    p1 = sum(next_cube.values())


    ix, ax = 0, iax
    iy, ay = 0, iay
    iz, az = 0, 0
    iw, aw = 0, 0
    next_cube = four_cube

    for i in range(6):
        cube = next_cube.copy()
        next_cube.clear()
        for x in range(ix-1, ax+2):
            for y in range(iy-1, ay+2):
                for z in range(iz-1, az+2):
                    for w in range(iw-1, aw+2):
                        nbrs = count_neighbors_4(cube, x, y, z, w)
                        if transition[cube[x,y,z,w]][nbrs]:
                            next_cube[x,y,z,w] = True
                            ix, ax = min(ix, x), max(ax, x)
                            iy, ay = min(iy, y), max(ay, y)
                            iz, az = min(iz, z), max(az, z)
                            iw, aw = min(iw, w), max(aw, w)
    p2 = sum(next_cube.values())
    return p1, p2

def run_tests():
    cases = [
        #(p1, p2, inp),
        (112, 848, """.#.\n..#\n###"""),
    ]

    for want_p1, want_p2, inp in cases:
        p1, p2 = d17(inp)
        if want_p1 is not None:
            assert want_p1 == p1, f"want = {want_p1}; got = {p1}"
        if want_p2 is not None:
            assert want_p2 == p2

def main():
    with open('../inputs/d17.txt') as f:
        inp = f.read().strip()
    p1, p2 = d17(inp)
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()
