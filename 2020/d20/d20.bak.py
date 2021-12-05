from typing import List, Dict
from collections import Counter, deque, defaultdict
from itertools import product
import re

class Tile:
    id: int
    grid: List[List[str]]
    edges: List[int]
    dim: int

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
        self.dim = len(self.grid)
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
        new_grid = [list([None] * self.dim) for _ in range(self.dim)]
        for x, y in product(range(self.dim), repeat=2):
            new_grid[y][self.dim-x] = self.grid[y][x]
        self.grid = new_grid
        n,e,s,w,wr,sr,er,nr = self.edges
        self.edges = [nr, wr, sr, er, e, s, w, n]

    def flip_ns(self):
        new_grid = [list([None] * self.dim) for _ in range(self.dim)]
        for x, y in product(range(self.dim), repeat=2):
            new_grid[self.dim-y][x] = self.grid[y][x]
        self.grid = new_grid
        n,e,s,w,wr,sr,er,nr = self.edges
        self.edges = [sr, er, nr, wr, w, n, e, s]

    def flip_nsew(self):
        new_grid = [list([None] * self.dim) for _ in range(self.dim)]
        for x, y in product(range(self.dim), repeat=2):
            new_grid[x][y] = self.grid[y][x]
        self.grid = new_grid
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
        new_grid = [list([None] * self.dim) for _ in range(self.dim)]
        if dir == -1:
            for x, y in product(range(self.dim), repeat=2):
                new_grid[self.dim-1-x][y] = self.grid[y][x]
            self.grid = new_grid
            n,e,s,w,wr,sr,er,nr = self.edges
            self.edges = [e, s, w, n, nr, wr, sr, er]
        elif dir == 1:
            for x, y in product(range(self.dim), repeat=2):
                new_grid[x][self.dim-1-y] = self.grid[y][x]
            self.grid = new_grid
            n,e,s,w,wr,sr,er,nr = self.edges
            self.edges = [w, n, e, s, sr, er, nr, wr]

    def get_line(self, idx, trim=False):
        if trim:
            return self.grid[idx][1:-1]
        return self.grid[idx]

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
            edge = tile
            needs_pair = set(tile.edges) - singles
            right_edge = needs_pair.pop()
            needs_pair.add(right_edge)

            tile.set_edge_dir(right_edge, 0)
            assert tile.get_edge(2) not in needs_pair
            if tile.get_edge(1) in needs_pair:
                assert tile.get_edge(3) not in needs_pair
                right_edge = tile.get_edge(0)
                bottom_edge = tile.get_edge(1)
            elif tile.get_edge(3) in needs_pair:
                assert tile.get_edge(1) not in needs_pair
                right_edge = tile.get_edge(3)
                bottom_edge = tile.get_edge(0)
            tile.set_edge_dir(right_edge, 1)
            assert right_edge == tile.get_edge(1)
            assert bottom_edge == tile.get_edge(2)

    grid_dim = len(single_sides) // 8
    tile_grid = [list([None] * grid_dim) for _ in range(grid_dim)]
    tile_grid[0][0] = edge
    unused_tiles = {*tiles.values(),} - {edge,}
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
        unused_tiles.discard(tile_grid[0][xy])
        unused_tiles.discard(tile_grid[xy][0])

    for x, y in product(range(1, grid_dim), repeat=2):
        print("scanning", x, y)
        bottom_above = tile_grid[y-1][x].get_edge(2)
        for tile in unused_tiles:
            if tile.has_edge(bottom_above):
                tile.set_edge_dir(tile.get_matching_edge(bottom_above), 0)
                tile_grid[y][x] = tile
                left_edge_match = tile.get_matching_edge(tile.get_edge(3))
                lefts_right_edge = tile_grid[y][x-1].get_edge(1)
                assert left_edge_match == lefts_right_edge
                break

    for y in range(grid_dim):
        for line in range(10):
            for x in range(grid_dim):
                print(''.join(tile_grid[y][x].get_line(line)), end=' ')
            print()
        print()
    print()
    print()

    pic = list([None] * 8 * grid_dim)
    for y in range(grid_dim):
        for line in range(1, 9):
            line_str = ''.join(''.join(tile_grid[y][x].get_line(line, True) for x in range(grid_dim)))
            pic[y*8 + line - 1] = line_str
            print(line_str)
            #for x in range(grid_dim):
            #    print(''.join(tile_grid[y][x].get_line(line, True)), end='')
            #print()
    print()
    print()

    print('\n\n')
    return p1, p2

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
            assert want_p2 == p2

def main():
    with open('../inputs/d20.txt') as f:
        inp = f.read().strip()
    p1, p2 = d20(inp)
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()

