from collections import defaultdict
from itertools import product
from multiprocessing import Pool

def count_neighbors_3(cube, x, y, z):
    count = 0
    for dx, dy, dz in product(range(-1, 2), repeat=3):
        if dx == 0 and dy == 0 and dz == 0:
            continue
        count += cube[x+dx,y+dy,z+dz]
    return count

def count_neighbors_4(cube, x, y, z, w):
    count = 0
    root = (x, y, z, w)
    for d in product(range(x-1,x+2), range(y-1,y+2),range(z-1,z+2),range(w-1,w+2)):
        count += d != root and cube[d]
    return count

def d17(inp):
    cube = None
    next_cube = defaultdict(bool)
    four_cube = defaultdict(bool)

    transition = [defaultdict(bool), defaultdict(bool)]
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
    iax = ax = x
    iay = ay = y

    for i in range(6):
        cube = next_cube.copy()
        next_cube.clear()
        for x, y, z in product(range(ix-1, ax+2), range(iy-1, ay+2), range(iz-1, az+2)):
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

    for i in range(5):
        cube = next_cube.copy()
        next_cube.clear()
        for x, y, z, w in product(range(ix-1, ax+2), range(iy-1, ay+2), range(iz-1, az+2), range(iw-1, aw+2)):
            nbrs = count_neighbors_4(cube, x, y, z, w)
            if transition[cube[x,y,z,w]][nbrs]:
                next_cube[x,y,z,w] = True
                ix, ax = min(ix, x), max(ax, x)
                iy, ay = min(iy, y), max(ay, y)
                iz, az = min(iz, z), max(az, z)
                iw, aw = min(iw, w), max(aw, w)

    p2 = 0
    for x, y, z, w in product(range(ix-1, ax+2), range(iy-1, ay+2), range(iz-1, az+2), range(iw-1, aw+2)):
        nbrs = count_neighbors_4(next_cube, x, y, z, w)
        if transition[next_cube[x,y,z,w]][nbrs]:
            p2 += 1
    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d17(inp)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
    return True

def main():
    with open('../inputs/d17.txt') as f:
        inp = f.read().strip()
    return d17(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        ('sample', '.#.\n..#\n###', 112, 848),
    ]
    """
    for case in cases:
        validate_test(*case)
    p1, p2 = main()
    print(f"p1 = {p1}\np2 = {p2}")
    """


    with Pool(processes=min(8, len(cases) + 1)) as pool:
        #import time
        main_res = pool.apply_async(main)
        #p1, p2 = main_res.get(60)
        test_res = [pool.apply_async(validate_test, case) for case in cases]
        #time.sleep(3)
        #assert main_res.ready()
        if all(test.get(30) for test in test_res):
            p1, p2 = main_res.get(60)
            print(f"p1 = {p1}\np2 = {p2}")
