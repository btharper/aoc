from typing import List, Dict
from collections import Counter, deque, defaultdict
from itertools import product
import re

class Tile:
    id: int
    grid: List[List[str]]
    edges: List[int]
    xdim: int
    ydim: int

    def _line_to_ints(self, line):
        line = list(line)
        ret = 0
        rev = 0
        for i, char in enumerate(reversed(line)):
            if char == '#':
                ret += 2**i
        for i, char in enumerate(line):
            if char == '#':
                rev += 2**i
        return ret, rev

    def __init__(self, tile_str):
        title_line, grid_lines = tile_str.split('\n', 1)
        self.id = int(title_line.split(':')[0].split()[-1])
        self.grid = [list(line) for line in grid_lines.split('\n')]
        n_edge = self._line_to_ints(self.grid[0])
        s_edge = self._line_to_ints(self.grid[-1][::-1])
        e_edge = self._line_to_ints([line[-1] for line in self.grid])
        w_edge = self._line_to_ints([line[0] for line in reversed(self.grid)])
        self.edges = [n_edge[0], e_edge[0], s_edge[0], w_edge[0], w_edge[1], s_edge[1], e_edge[1], n_edge[1]]
        self.ydim = len(self.grid)
        self.xdim = len(self.grid[0])
        #print(*[''.join(line) for line in self.grid], sep='\n')
        #print(self.edges)

    def has_edge(self, edge):
        if edge in self.edges:
            return True

    def set_edge_dir(self, edge, dir):
        idx = self.edges.index(edge)
        if idx >= 4:
            self.flip_nsew()
            idx = self.edges.index(edge)
        self.set_edge_north(edge)
        for _ in range(dir):
            self.rotate(1)

    def set_edge_north(self, edge):
        idx = self.edges.index(edge)
        if idx < 4:
            for _ in range(idx):
                self.rotate(-1)
        elif idx >= 4:
            for _ in range(7 - idx, 4):
                self.rotate(-1)
            self.flip_ew()

    def flip_ew(self):
        new_grid = [list([None] * self.xdim) for _ in range(self.ydim)]
        for x, y in product(range(self.xdim), range(self.ydim)):
            new_grid[y][self.xdim-1-x] = self.grid[y][x]
        self.grid = new_grid
        n,e,s,w,wr,sr,er,nr = self.edges
        self.edges = [nr, wr, sr, er, e, s, w, n]

    def flip_ns(self):
        new_grid = [list([None] * self.xdim) for _ in range(self.ydim)]
        for x, y in product(range(self.xdim), range(self.ydim)):
            new_grid[self.ydim-1-y][x] = self.grid[y][x]
        self.grid = new_grid
        n,e,s,w,wr,sr,er,nr = self.edges
        self.edges = [sr, er, nr, wr, w, n, e, s]

    def flip_nsew(self):
        new_grid = [list([None] * self.ydim) for _ in range(self.xdim)]
        for x, y in product(range(self.xdim),range(self.ydim)):
            new_grid[x][y] = self.grid[y][x]
        self.grid = new_grid
        self.xdim, self.ydim = self.ydim, self.xdim
        n,e,s,w,wr,sr,er,nr = self.edges
        self.edges = [wr, sr, er, nr, n, e, s, w]

    def get_opposite_edge(self, edge):
        idx = self.edges.index(edge) - 8
        return self.edges[~idx]

    def get_matching_edge(self, edge):
        idx = self.edges.index(edge)
        return self.edges[~idx]

    def get_edge(self, idx):
        return self.edges[idx]

    def rotate(self, dir):
        new_grid = [list([None] * self.ydim) for _ in range(self.xdim)]
        if dir == -1:
            for x, y in product(range(self.xdim), range(self.ydim)):
                new_grid[self.xdim-1-x][y] = self.grid[y][x]
            self.grid = new_grid
            self.xdim, self.ydim = self.ydim, self.xdim
            n,e,s,w,wr,sr,er,nr = self.edges
            self.edges = [e, s, w, n, nr, wr, sr, er]
        elif dir == 1:
            for x, y in product(range(self.xdim), range(self.ydim)):
                new_grid[x][self.ydim-1-y] = self.grid[y][x]
            self.grid = new_grid
            self.xdim, self.ydim = self.ydim, self.xdim
            n,e,s,w,wr,sr,er,nr = self.edges
            self.edges = [w, n, e, s, sr, er, nr, wr]

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

    print(f"{sides=}")
    print(f"total_sides={sum(sides.values())}")
    single_sides = +Counter({k:v % 2 for k,v in sides.items()})
    print(f"{len(single_sides)=}")
    print(f"{single_sides=}")
    print(f"num_tiles =", len(inp.split('\n\n')))

    singles = {*single_sides.keys(),}
    #print(singles)

    p1 = 1
    for tile in tiles.values():
        if len(singles & set(tile.edges)) == 4:
            p1 *= tile.id
            corner_tile = tile
    needs_pair = set(corner_tile.edges) - singles
    right_edge = needs_pair.pop()
    needs_pair.add(right_edge)

    corner_tile.set_edge_dir(right_edge, 0)
    assert corner_tile.get_edge(2) not in needs_pair
    if corner_tile.get_edge(1) in needs_pair:
        assert corner_tile.get_edge(3) not in needs_pair
        right_edge = corner_tile.get_edge(0)
        bottom_edge = corner_tile.get_edge(1)
    elif corner_tile.get_edge(3) in needs_pair:
        assert corner_tile.get_edge(1) not in needs_pair
        right_edge = corner_tile.get_edge(3)
        bottom_edge = corner_tile.get_edge(0)
    corner_tile.set_edge_dir(right_edge, 1)
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

    grid_dim = len(single_sides) // 8
    tile_grid = [list([None] * grid_dim) for _ in range(grid_dim)]
    tile_grid[0][0] = corner_tile
    unused_tiles = set(tiles.values())
    unused_tiles.remove(corner_tile)
    """
    for xy in range(1, grid_dim):
        print(f"Scanning {xy=}")
        for tile in unused_tiles:
            if tile.has_edge(right_edge):
                tile.set_edge_dir(tile.get_matching_edge(right_edge), 3)
                tile_grid[0][xy] = tile
                right_edge = tile.get_edge(1)
                assert tile.get_edge(0) in singles
                left_edge_match = tile.get_matching_edge(tile.get_edge(3))
                lefts_right_edge = tile_grid[0][xy-1].get_edge(1)
                assert left_edge_match == lefts_right_edge
            elif tile.has_edge(bottom_edge):
                tile.set_edge_dir(tile.get_matching_edge(bottom_edge), 0)
                tile_grid[xy][0] = tile
                bottom_edge = tile.get_edge(2)
        assert tile_grid[0][xy] is not None
        assert tile_grid[xy][0] is not None
        unused_tiles.remove(tile_grid[0][xy])
        unused_tiles.remove(tile_grid[xy][0])
    """
    for y in range(1, grid_dim):
        print(f"Scanning first col {y=}")
        for tile in unused_tiles:
            if tile.has_edge(bottom_edge):
                tile.set_edge_dir(tile.get_matching_edge(bottom_edge), 0)
                tile_grid[y][0] = tile
                assert tile.get_edge(3) in singles
                bottom_edge = tile.get_edge(2)
                bottom_matching_edge = tile_grid[y-1][0].get_edge(2)
                top_matching_edge = tile.get_matching_edge(tile.get_edge(0))
                assert bottom_matching_edge == top_matching_edge
                break
        assert tile_grid[y][0] is not None
        unused_tiles.remove(tile_grid[y][0])


    for y in range(grid_dim):
        for x in range(1, grid_dim):
    #for x, y in product(range(1, grid_dim), repeat=2):
            print("scanning", x, y)
            lefts_right_edge = tile_grid[y][x-1].get_edge(1)
            for tile in unused_tiles:
                if tile.has_edge(lefts_right_edge):
                    tile.set_edge_dir(tile.get_matching_edge(lefts_right_edge), 3)
                    tile_grid[y][x] = tile
                    left_edge_match = tile.get_matching_edge(tile.get_edge(3))
                    lefts_right_edge = tile_grid[y][x-1].get_edge(1)
                    assert left_edge_match == lefts_right_edge
                    if y > 0:
                        ups_bottom_edge = tile_grid[y-1][x].get_edge(2)
                        top_edge = tile.get_matching_edge(tile.get_edge(0))
                        assert ups_bottom_edge == top_edge
                    break
            assert tile_grid[y][x] is not None
            unused_tiles.remove(tile_grid[y][x])

    for y in range(grid_dim):
        for line in range(10):
            for x in range(grid_dim):
                print(''.join(tile_grid[y][x].get_line(line)), end=' ')
            print()
        print()
    print()
    print()

    edge_view = format_grid(tile_grid)
    print(pic_str := format_grid_small(tile_grid))
    tile_str = "Tile 0:\n" + pic_str
    pic = Tile(tile_str)
    print('\n')
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
    pic.flip_nsew()
    pic.flip_nsew()
    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str
    pic.flip_ns()
    pic.flip_nsew()
    pic.flip_ew()
    pic.flip_ew()
    pic.flip_nsew()
    pic.flip_ns()
    assert '\n'.join([''.join(grid_row) for grid_row in pic.grid]) == pic_str

    #print()
    #print()
    #for i in range(len(pic.grid)):
    #    print(''.join(pic.get_line(i)))

    for _ in range(2):
        for _ in range(4):
            if n_mons := has_monster(pic.grid):
                print('\n'*5, '*'*50)
                #print('\n'.join([''.join(grid_row) for grid_row in pic.grid]))
                for grid_row in pic.grid:
                    print(''.join(grid_row))
                print(f"Spotted {n_mons} loch ness monsters")
                p2 = sum(1 for x, y in product(range(len(pic.grid[0])), range(len(pic.grid))) if pic.grid[y][x] == '#')
                print(f"Found {p2} total '#'s, {p2 - (n_mons * 15)} after subtracting {n_mons} mons")
                p2 -= n_mons * 15
                break
            else:
                pic.rotate(-1)
        else:
            pic.flip_nsew()
            continue
        break
    else:
        print("Something went horribly wrong")

    print('\n\n')
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
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()

