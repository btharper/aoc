from collections import defaultdict, Counter, deque
from itertools import product
from multiprocessing import Pool
import math
import re

non_digits = re.compile('[^0-9]+')
def sign(a, b, step=1):
    return int(math.copysign(step, b-a))
def autorange(a,b, step=1):
    if a == b:return (a,)
    s = sign(a, b, step)
    return range(a, b+s, s)
def get_ints(line, strip_line=False):
    if strip_line:
        line = line.strip()
    return [*map(int, non_digits.split(line))]

letter_map = {
        '.####.': {'#....#': {
                '#..#.#': {'.#.###': {'......': 'G',},},
                '#....#': {'.#..#.': {'......': 'C',},},
            },},
        '.#####': {'#..#..': {'#..#..': {'.#####': {'......': 'A',},},},},
        '#####.': {
                '.....#': {'.....#': {'#####.': {'......': 'U',},},},
                '#...#.': {'#...#.': {'#...#.': {'#####.': '{square}',},},},
            },
        '######': {
                '..#...': {'..#...': {'######': {'......': 'H',},},},
                '#..#..': {'#..#..': {'.##...': {'......': 'P',},},},
            },
    }

def read_font(img):
    ret = []
    for left in range(0, len(img[0]), 5):
        letter = [list('?' * 6) for _ in range(5)]
        for y in range(6):
            for x in range(5):
                letter[x][y] = img[y][left+x]
        #print(*map(lambda x:''.join(x), letter), sep='\n', end='\n\n')
        ret.append(read_letter(letter))
    return ''.join(ret)

def read_letter(img):
    lttr = letter_map
    for line in img:
        lkup = ''.join(line)
        if lkup not in lttr:
            break
        lttr = lttr[lkup]
    else: #nobreak
        return lttr
    print('Letter Not found:')
    for x in range(6):
        for y in range(5):
            print(img[y][x], end='')
        print()
    print('-'*10)

def d13(inp, sample=False):
    p1, p2 = None, None

    xy_pos_list, instructions = inp.strip().split('\n\n')
    max_x, max_y = 0,0
    grid = {}
    inst = []
    for line in xy_pos_list.split():
        x,y = get_ints(line)
        grid[x,y] = '#'
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    for line in instructions.strip().split('\n'):
        last = line.split()[-1]
        axis, num = last.split('=')
        num = int(num)
        inst.append((axis, num))

    for axis, num in inst:
        ngrid = {}
        if axis == 'x':
            max_x = num
            for (x,y),v in grid.items():
                if x > num:
                    nx = 2 * num - x
                    ngrid[nx,y] = v
                else:
                    ngrid[x,y] = v
        elif axis == 'y':
            max_y = num
            for (x,y),v in grid.items():
                if y < num:
                    ngrid[x,y] = v
                else:
                    ngrid[x,2*num-y] = v
        grid = ngrid
        if p1 is None:
            p1 = len(grid)

    img = [list('?' * max_x) for _ in range(max_y)]
    for y in range(max_y):
        for x in range(max_x):
            img[y][x] = grid.get((x,y), '.')

    #print(*map(lambda x:''.join(x), img), sep='\n', end='\n\n')
    p2 = read_font(img)

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d13(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d13.txt') as f:
        inp = f.read().strip()
    return d13(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""", 17, '{square}'),
    ]

    """
    # Non multiprocessing version
    for case in cases:
        validate_test(*case)
    p1, p2 = main()
    print(f"p1 = {p1}\np2 = {p2}")
    """


    with Pool(processes=min(8, len(cases) + 1)) as pool:
        main_res = pool.apply_async(main)
        test_res = [pool.apply_async(validate_test, case) for case in cases]
        test_pass, do_p1, do_p2 = True, False, False
        for test in test_res:
            tp, dp1, dp2 = test.get(30)
            test_pass &= tp
            do_p1 |= dp1
            do_p2 |= dp2
        if test_pass:
            p1, p2 = main_res.get(60)
            assert do_p1 or do_p2, "Didn't run any tets"
            assert p1 is None or do_p1 == True, "Got P1 value without 'do_p1' set"
            assert p2 is None or do_p2 == True, "Got P2 value without 'do_p2' set"
            print(f"p1 = {p1}\np2 = {p2}")
