import textwrap as tw
from collections import Counter, deque, defaultdict
import re
from itertools import product

def d24(inp):
    p1, p2 = 0, 0

    directions = [(1,0),(1,-1), (0,-1),(-1,0), (-1,1), (0,1)]
    assert len(directions) == len({*directions,})
    inp = inp.replace('ne','0').replace('se','2').replace('sw','3').replace('nw','5').replace('e','1').replace('w','4')

    black = set()
    for line in inp.split('\n'):
        cx, cy = 0, 0
        for dir in map(int, line):
            dx, dy = directions[dir]
            cx += dx
            cy += dy
        coord = cx, cy
        if coord in black:
            black.remove(coord)
        else:
            black.add(coord)
    p1 = len(black)

    for day in range(1, 101):
        nbrs = defaultdict(int)
        for cx, cy in black:
            nbrs[cx, cy] += 0
            for dir in range(6):
                dx, dy = directions[dir]
                nbrs[cx+dx,cy+dy] += 1
        for k,v in nbrs.items():
            if k in black and (v == 0 or v > 2):
                black.remove(k)
            elif k not in black and (v == 2):
                black.add(k)
    p2 = len(black)

    return p1, p2

def run_tests():
    cases = [
        #(p1, p2, inp),
        (10, 2208, """
        sesenwnenenewseeswwswswwnenewsewsw
        neeenesenwnwwswnenewnwwsewnenwseswesw
        seswneswswsenwwnwse
        nwnwneseeswswnenewneswwnewseswneseene
        swweswneswnenwsewnwneneseenw
        eesenwseswswnenwswnwnwsewwnwsene
        sewnenenenesenwsewnenwwwse
        wenwwweseeeweswwwnwwe
        wsweesenenewnwwnwsenewsenwwsesesenwne
        neeswseenwwswnwswswnw
        nenwswwsewswnenenewsenwsenwnesesenew
        enewnwewneswsewnwswenweswnenwsenwsw
        sweneswneswneneenwnewenewwneswswnese
        swwesenesewenwneswnwwneseswwne
        enesenwswwswneneswsenwnewswseenwsese
        wnwnesenesenenwwnenwsewesewsesesew
        nenewswnwewswnenesenwnesewesw
        eneswnwswnwsenenwnwnwwseeswneewsenese
        neswnwewnwnwseenwseesewsenwsweewe
        wseweeenwnesenwwwswnew
        """),
    ]

    for i, (want_p1, want_p2, inp) in enumerate(cases):
        inp = tw.dedent(inp).strip()
        p1, p2 = d24(inp)
        if want_p1 is not None:
            assert want_p1 == p1, f"Test{i:02d}-p1 {dict(want=want_p1, got=p1, i=i)}"
        if want_p2 is not None:
            assert want_p2 == p2, f"Test{i:02d}-p2 {dict(want=want_p2, got=p2, i=i)}"

def main():
    with open('../inputs/d24.txt') as f:
        inp = f.read().strip()
    p1, p2 = d24(inp)
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()
