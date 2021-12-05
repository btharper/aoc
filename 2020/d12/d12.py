from typing import List, Tuple
from fractions import Fraction
import re
from collections import Counter, deque, defaultdict
from itertools import product


with open('../inputs/d12.txt') as f:
    inp = f.read().strip()

inp2 = """F10
N3
F7
R90
F11"""

#inp = inp2

rot = {}

def d12(inp: str) -> Tuple[int, int]:
    dir = complex(1, 0)
    way = complex(10, -1)
    pos1 = complex(0, 0)
    pos2 = complex(0, 0)
    for line in inp.strip().split():
        go, num = line[0], int(line[1:])
        delta1 = complex(0, 0)
        delta2 = complex(0, 0)
        if go == 'L':
            dir *= complex(0, -1) ** (num // 90)
            way *= complex(0, -1) ** (num // 90)
        elif go == 'R':
            dir *= complex(0, 1) ** (num // 90)
            way *= complex(0, 1) ** (num // 90)
        elif go == 'F':
            delta1 = dir * num
            delta2 = way * num
        elif go == 'N':
            delta1 = complex(0, -num)
            way -= complex(0, num)
        elif go == 'S':
            delta1 = complex(0, num)
            way += complex(0, num)
        elif go == 'E':
            delta1 = complex(num, 0)
            way += complex(num, 0)
        elif go == 'W':
            delta1 = complex(-num, 0)
            way -= complex(num, 0)
        pos1 += delta1
        pos2 += delta2
    return (int(abs(pos1.real) + abs(pos1.imag)), int(abs(pos2.real) + abs(pos2.imag)))

if __name__ == '__main__':
    #assert d12(inp2) == (25, 286), d12(inp2)
    p1, p2 = d12(inp)
    print(f"p1 = {p1}\np2 = {p2}")
