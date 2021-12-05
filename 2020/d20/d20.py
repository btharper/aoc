from typing import List, Dict
from collections import Counter
from itertools import product

do_asserts = True

class Tile:
    id: int
    grid: List[List[str]]
    edges: List[int]
    dim: int
    renders: List[List[List[str]]]

    def _line_to_ints(self, line, llen):
        line = list(line)
        ret = 0
        rev = 0
        for i, char in enumerate(line):
            if char == '#':
                rev += 2**i
                ret += 2**(llen + (~i))
        return ret, rev

    def _empty_grid(self):
        self._empty_line = [None] * self.dim
        return [self._empty_line.copy() for _ in range(self.dim)]

    def __init__(self, tile_str):
        title_line, grid_lines = tile_str.split('\n', 1)
        self.id = int(title_line.split(':')[0].split()[-1])
        self.grid = [list(line) for line in grid_lines.split('\n')]
        self.dim = len(self.grid)
        self._empty_line = [None] * self.dim
        n, nr = self._line_to_ints(self.grid[0], self.dim)
        s, sr = self._line_to_ints(self.grid[-1][::-1], self.dim)
        e, er = self._line_to_ints([line[-1] for line in self.grid], self.dim)
        w, wr = self._line_to_ints([line[0] for line in self.grid[::-1]], self.dim)
        self.renders = {n:grid}
        self.edges = [n, e, s, w, wr, sr, er, nr]
        self.edge_set = {n, e, s, w, wr, sr, er, nr}
        #print(*[''.join(line) for line in self.grid], sep='\n')
        #print(self.edges)

    def has_edge(self, edge):
        return edge in self.edge_set

    def set_edge_dir(self, edge, dir):
        other_offsets = {(5,0): 2, (6,0):1, (6,1):2}
        idx = self.edges.index(edge)
        if idx < 4:
            self.rotate(dir - idx)
        else:
            offset = (7 - idx + dir) % 4
            if (idx,dir) in other_offsets:
                assert other_offsets[idx,dir] == offset
            #print(f"\tset_edge_dir({idx=}, {dir=}, {offset=})")
            #  5  0  2
            #  6  0  1
            #  6  1  2
            #  4  1  
            if offset == 0:
                self.flip_ew()
                #print('ew')
            elif offset == 1:
                self.flip_mEqPos1()
                #print('pos1')
            elif offset == 2:
                self.flip_ns()
                #print('ns')
            elif offset == 3:
                self.flip_mEqNeg1()
                #print('neg1')
            else:
                print(f"{'*' * 50}\noops {idx} {dir} {offset}")
        #elif idx == 6:
        #    if 3 == 10 - idx - dir:
        #        ew()
        #    elif 2 == 10 - idx - dir:
        #        Pos1()
        #    elif dir == 3:
        #        ns()
        #    elif dir == 0:
        #        Neg1()
        #if idx >= 4:
        #    self.flip_mEqNeg1()
        #    idx = self.edges.index(edge)
        #self.set_edge_north(edge)
        #self.rotate(dir)

    def set_edge_north(self, edge):
        idx = self.edges.index(edge)
        if idx < 4:
            self.rotate(-idx)
        elif idx >= 4:
            self.rotate(7 - idx)
            self.flip_ew()

    def flip_ew(self):
        #new_grid = [list([None] * self.dim) for _ in range(self.dim)]
        new_grid = self._empty_grid()
        for x, y in product(range(self.dim), repeat=2):
            new_grid[y][self.dim-1-x] = self.grid[y][x]
        self.grid = new_grid
        n,e,s,w,wr,sr,er,nr = self.edges
        self.edges = [nr, wr, sr, er, e, s, w, n]

    def flip_ns(self):
        #new_grid = [list([None] * self.dim) for _ in range(self.dim)]
        new_grid = self._empty_grid()

        for x, y in product(range(self.dim), repeat=2):
            new_grid[self.dim-1-y][x] = self.grid[y][x]
        self.grid = new_grid
        n,e,s,w,wr,sr,er,nr = self.edges
        self.edges = [sr, er, nr, wr, w, n, e, s]

    def flip_mEqNeg1(self):
        new_grid = self._empty_grid()
        #new_grid = [list([None] * self.dim) for _ in range(self.dim)]
        for x, y in product(range(self.dim),range(self.dim)):
            new_grid[x][y] = self.grid[y][x]
        self.grid = new_grid
        n,e,s,w,wr,sr,er,nr = self.edges
        self.edges = [wr, sr, er, nr, n, e, s, w]

    def flip_mEqPos1(self):
        new_grid = self._empty_grid()
        #new_grid = [list([None] * self.dim) for _ in range(self.dim)]
        for x, y in product(range(self.dim),range(self.dim)):
            new_grid[self.dim-1-x][self.dim-1-y] = self.grid[y][x]
        self.grid = new_grid
        n,e,s,w,wr,sr,er,nr = self.edges
        self.edges = [er, nr, wr, sr, s, w, n, e]

    def get_opposite_edge(self, edge):
        idx = self.edges.index(edge) - 8
        return self.edges[~idx]

    def get_matching_edge(self, edge):
        idx = self.edges.index(edge)
        return self.edges[~idx]

    def get_edge(self, idx):
        return self.edges[idx]

    def rotate(self, dir):
        new_grid = self._empty_grid()
        #new_grid = [list([None] * self.dim) for _ in range(self.dim)]
        dir %= 4
        if dir == -1 or dir == 3:
            for x, y in product(range(self.dim), repeat=2):
                new_grid[self.dim-1-x][y] = self.grid[y][x]
            self.grid = new_grid
            n,e,s,w,wr,sr,er,nr = self.edges
            self.edges = [e, s, w, n, nr, wr, sr, er]
        elif dir == 1 or dir == -3:
            for x, y in product(range(self.dim), repeat=2):
                new_grid[x][self.dim-1-y] = self.grid[y][x]
            self.grid = new_grid
            n,e,s,w,wr,sr,er,nr = self.edges
            self.edges = [w, n, e, s, sr, er, nr, wr]
        elif dir == 2 or dir == -2:
            for x, y in product(range(self.dim), repeat=2):
                new_grid[self.dim-1-y][self.dim-1-x] = self.grid[y][x]
            self.grid = new_grid
            n,e,s,w,wr,sr,er,nr = self.edges
            self.edges = [s, w, n, e, er, nr, wr, sr]

    def get_line(self, idx):
        return self.grid[idx].copy()

    def get_line_compact(self, idx):
        return self.grid[idx][1:-1].copy()

def d20(inp):
    p1, p2 = 0, 0

    tiles = {}
    sides = Counter()
    for tile_str in inp.split('\n\n'):
        tile = Tile(tile_str)
        tiles[tile.id] = tile
        sides.update(tile.edges)

    #print(f"{sides=}")
    #print(f"total_sides={sum(sides.values())}")
    #single_sides = +Counter({k:v % 2 for k,v in sides.items()})
    #print(f"{len(single_sides)=}")
    #print(f"{single_sides=}")
    #print(f"num_tiles =", len(inp.split('\n\n')))

    singles = {k for k,v in sides.items() if v == 1}
    #print(singles)

    p1 = 1
    for tile in tiles.values():
        if len(singles & set(tile.edges)) == 4:
            p1 *= tile.id
            corner_tile = tile
    needs_pair = set(corner_tile.edges) - singles
    right_edge = needs_pair.copy().pop()

    if do_asserts:
        #print(f"{corner_tile.edges.index(right_edge)}, 0")
        for i in range(4, 10):
            if i == 1:
                pic = tile
            else:
                pic = Tile(' 3:\n.#\n.#')
                pic.id = 666666
                pic.edges = ['n', 'e', 's', 'w', 'wr', 'sr', 'er', 'nr']
                pic.dim = i
                pic.grid = pic._empty_grid()
                for x, y in product(range(pic.dim), repeat=2):
                    pic.grid[y][x] = '#' if x*x+y % 4 == 0 else '.'
                pic.grid[0][1] = 'a'
                pic.grid[1][pic.dim-1] = 'b'
                pic.grid[pic.dim-1][pic.dim-2] = 'c'
                pic.grid[pic.dim-2][0] = 'd'
                pic.grid[0][0] = 'A'
                pic.grid[0][pic.dim-1] = 'B'
                pic.grid[pic.dim-1][pic.dim-1] = 'C'
                pic.grid[pic.dim-1][0] = 'D'
            #print(*pic.grid, sep='\n')
            saved_edges = tuple(pic.get_edge(i) for i in range(8))
            pic_str = '\n'.join([''.join(grid_row) for grid_row in pic.grid])
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            for e in range(4):
                for i in range(10):
                    pic.rotate(i)
                    pic.set_edge_dir(saved_edges[e], e)
                    assert tuple(pic.edges) == saved_edges
                    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                for i in range(4):
                    pic.rotate(i)
                    pic.rotate(4-i)
                    assert tuple(pic.edges) == saved_edges
                    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                for i in range(4):
                    pic.rotate(i)
                    pic.rotate(-i)
                    assert tuple(pic.edges) == saved_edges
                    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                pic.flip_ns()
                pic.flip_ns()
                assert tuple(pic.edges) == saved_edges
                assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
                pic.set_edge_dir(saved_edges[e], e)
                assert tuple(pic.edges) == saved_edges
                assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                pic.flip_ew()
                pic.flip_ew()
                assert tuple(pic.edges) == saved_edges
                assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
                pic.set_edge_dir(saved_edges[e], e)
                assert tuple(pic.edges) == saved_edges
                assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                pic.flip_mEqNeg1()
                pic.flip_mEqNeg1()
                assert tuple(pic.edges) == saved_edges
                assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
                pic.set_edge_dir(saved_edges[e], e)
                assert tuple(pic.edges) == saved_edges
                assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                pic.flip_mEqPos1()
                pic.flip_mEqPos1()
                assert tuple(pic.edges) == saved_edges
                assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
                pic.set_edge_dir(saved_edges[e], e)
                assert tuple(pic.edges) == saved_edges
                assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                for i in range(10):
                    pic.rotate(i)
                    pic.rotate(i)
                    pic.rotate(i)
                    pic.rotate(i)
                    assert tuple(pic.edges) == saved_edges
                    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                for i in range(100):
                    pic.rotate(i)
                    pic.set_edge_dir(saved_edges[e], e)
                    assert tuple(pic.edges) == saved_edges
                    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                for i in range(10):
                    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str, f"{e=} {i=} flip_ns()"
                    #print(f"{'*'*60}\nHere be dragons")
                    #print("Starting")
                    #print('\n'.join([''.join(grid_row) for grid_row in pic.grid]), "\n\n")
                    #print(pic.edges)
                    pic.rotate(i)
                    #print("Post rotate(i)")
                    #print('\n'.join([''.join(grid_row) for grid_row in pic.grid]), "\n\n")
                    #print(pic.edges)
                    pic.flip_ns()
                    #print("Post flip_ns()")
                    #print('\n'.join([''.join(grid_row) for grid_row in pic.grid]), "\n\n")
                    #print(pic.edges)
                    #print(f"rotate({i}), flip_ns(), {e=}, {saved_edges[e]}")
                    pic.set_edge_dir(saved_edges[e], e)
                    #print("Post set_edge")
                    #print('\n'.join([''.join(grid_row) for grid_row in pic.grid]), "\n\n")
                    #print(pic.edges)
                    assert tuple(pic.edges) == saved_edges
                    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str, f"{e=} {i=} flip_ns()"
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                for i in range(10):
                    pic.rotate(i)
                    pic.flip_ew()
                    pic.set_edge_dir(saved_edges[e], e)
                    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                for i in range(10):
                    pic.rotate(i)
                    pic.flip_mEqNeg1()
                    pic.set_edge_dir(saved_edges[e], e)
                    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            for e in range(4):
                for i in range(10):
                    pic.rotate(i)
                    pic.flip_mEqPos1()
                    pic.set_edge_dir(saved_edges[e], e)
                    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
            assert tuple(pic.edges) == saved_edges
            assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
    corner_tile.set_edge_dir(right_edge, 0)
    if corner_tile.get_edge(1) in needs_pair:
        if do_asserts:
            assert corner_tile.get_edge(2) not in needs_pair
            assert corner_tile.get_edge(3) not in needs_pair
        right_edge = corner_tile.get_edge(0)
        bottom_edge = corner_tile.get_edge(1)
    elif corner_tile.get_edge(3) in needs_pair:
        if do_asserts:
            assert corner_tile.get_edge(1) not in needs_pair
            assert corner_tile.get_edge(2) not in needs_pair
        right_edge = corner_tile.get_edge(3)
        bottom_edge = corner_tile.get_edge(0)
    corner_tile.set_edge_dir(right_edge, 1)
    if do_asserts:
        assert right_edge == corner_tile.get_edge(1)
        assert bottom_edge == corner_tile.get_edge(2)

        saved_edges = corner_tile.edges.copy()
        saved_north = corner_tile.get_edge(0)
        for i in range(10):
            for _ in range(i):
                corner_tile.rotate(1)
            corner_tile.set_edge_dir(saved_north, 0)
        assert saved_edges == corner_tile.edges.copy()
        for i in range(10):
            for _ in range(i):
                corner_tile.rotate(-1)
            corner_tile.set_edge_dir(saved_north, 0)
        assert saved_edges == corner_tile.edges.copy()

    grid_dim = len(singles) // 8
    tile_grid = [list([None] * grid_dim) for _ in range(grid_dim)]
    tile_grid[0][0] = corner_tile
    unused_tiles = set(tiles.values())
    unused_tiles.remove(corner_tile)
    for y in range(1, grid_dim):
        #print(f"Scanning first col {y=}")
        for tile in unused_tiles:
            if tile.has_edge(bottom_edge):
                tile.set_edge_dir(tile.get_matching_edge(bottom_edge), 0)
                tile_grid[y][0] = tile
                if do_asserts:assert tile.get_edge(3) in singles
                bottom_edge = tile.get_edge(2)
                bottom_matching_edge = tile_grid[y-1][0].get_edge(2)
                top_matching_edge = tile.get_matching_edge(tile.get_edge(0))
                if do_asserts:assert bottom_matching_edge == top_matching_edge
                break
        if do_asserts:assert tile_grid[y][0] is not None
        unused_tiles.remove(tile_grid[y][0])

    for y, x in product(range(grid_dim), range(1, grid_dim)):
        #print("scanning", x, y)
        lefts_right_edge = tile_grid[y][x-1].get_edge(1)
        for tile in unused_tiles:
            if tile.has_edge(lefts_right_edge):
                tile.set_edge_dir(tile.get_matching_edge(lefts_right_edge), 3)
                tile_grid[y][x] = tile
                left_edge_match = tile.get_matching_edge(tile.get_edge(3))
                lefts_right_edge = tile_grid[y][x-1].get_edge(1)
                if do_asserts:
                    assert left_edge_match == lefts_right_edge
                    if y > 0:
                        ups_bottom_edge = tile_grid[y-1][x].get_edge(2)
                        top_edge = tile.get_matching_edge(tile.get_edge(0))
                        assert ups_bottom_edge == top_edge
                break
        if do_asserts:assert tile_grid[y][x] is not None
        unused_tiles.remove(tile_grid[y][x])

    #for y in range(grid_dim):
    #    for line in range(10):
    #        for x in range(grid_dim):
    #            print(''.join(tile_grid[y][x].get_line(line)), end=' ')
    #        print()
    #    print()
    #print()
    #print()

    edge_view = format_grid(tile_grid)
    pic_str = format_grid_small(tile_grid)
    tile_str = "Tile 0:\n" + pic_str
    pic = Tile(tile_str)
    #print(f"big tile dims are {(pic.xdim, pic.ydim)}")
    #print('\n')
    if do_asserts:
        assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
        pic.rotate(1)
        pic.rotate(1)
        pic.rotate(1)
        pic.rotate(1)
        assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
        pic.flip_ns()
        pic.flip_ns()
        assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
        pic.flip_ew()
        pic.flip_ew()
        assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
        pic.flip_mEqNeg1()
        pic.flip_mEqNeg1()
        assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
        pic.flip_ns()
        pic.flip_mEqNeg1()
        pic.flip_ew()
        pic.flip_ew()
        pic.flip_mEqNeg1()
        pic.flip_ns()
        assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
        pic.rotate(2)
        pic.rotate(1)
        pic.rotate(-3)
        assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
        pic.rotate(10)
        pic.rotate(-5)
        pic.rotate(19)
        assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
        pic.flip_ns()
        pic.rotate(3)
        pic.flip_mEqNeg1()
        pic.rotate(-2)
        pic.flip_ew()
        pic.rotate(-1)
        pic.flip_ns()
        pic.rotate(1)
        assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
        pic.flip_mEqNeg1()
        pic.flip_mEqPos1()
        pic.rotate(2)
        assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
        pic.flip_ns()
        pic.rotate(3)
        pic.flip_mEqPos1()
        pic.rotate(-2)
        pic.flip_ew()
        pic.rotate(-1)
        pic.flip_ns()
        pic.rotate(-1)
        assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
        

    #print()
    #print()
    #for i in range(len(pic.grid)):
    #    print(''.join(pic.get_line(i)))

    for _ in range(2):
        for _ in range(4):
            if n_mons := has_monster(pic.grid):
                #print('\n'*5, '*'*50)
                #print('\n'.join([''.join(grid_row) for grid_row in pic.grid]))
                #for grid_row in pic.grid:
                #    print(''.join(grid_row))
                #print(f"Spotted {n_mons} loch ness monsters")
                p2 = sum(1 for x, y in product(range(len(pic.grid[0])), range(len(pic.grid))) if pic.grid[y][x] == '#')
                #print(f"Found {p2} total '#'s, {p2 - (n_mons * 15)} after subtracting {n_mons} mons")
                p2 -= n_mons * 15
                break
            else:
                pic.rotate(-1)
        else:
            pic.flip_mEqNeg1()
            continue
        break
    else:
        print("Something went horribly wrong")

    #print('\n\n')
    return p1, p2

def format_grid(grid):
    rows = []
    for y, grid_row in enumerate(grid):
        for line in range(10):
            rows.append(' '.join([''.join(tile.get_line(line)) for x, tile in enumerate(grid_row)]))
    return '\n\n'.join(rows)

def format_grid_small(grid):
    rows = []
    for grid_row in grid:
        for line in range(1, 9):
            rows.append(''.join([''.join(tile.get_line_compact(line)) for tile in grid_row]))
    return '\n'.join(rows)

def has_monster(grid):
    #                   8
    # 0    56    12    789
    #  1  4  7  0  3  6
    sea_monster = ((18,), (0, 5,6,11,12,17,18,19), (1,4,7,10,13,16))
    num_monsters = 0

    for y, grid_row in enumerate(grid[:-2]):
        for x, char in enumerate(grid_row[:-20]):
            for my, monster_row in enumerate(sea_monster):
                for mx in monster_row:
                    if grid[y+my][x+mx] != '#':
                        break
                else:
                    continue
                break
            else:
                num_monsters += 1
    return num_monsters

def run_tests():
    cases = [
        #(p1, p2, inp),
        (20899048083289, 273,
        """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""),
    ]

    for want_p1, want_p2, inp in cases:
        p1, p2 = d20(inp)
        if want_p1 is not None:
            assert want_p1 == p1
        if want_p2 is not None:
            assert want_p2 == p2, (want_p2, p2)

def main():
    with open('../inputs/d20.txt') as f:
        inp = f.read().strip()
    p1, p2 = d20(inp)
    assert (p1, p2) == (15670959891893, 1964)
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()

