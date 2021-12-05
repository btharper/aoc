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

print(inp.split()[:10])

def dir_mul(dir, mul):
    return (dir[0] * mul, dir[1] * mul)

x, y = 0, 0
dir = (1, 0)
for line in inp.split():
    num = int(line[1:])
    go = line[0]
    dx, dy = 0, 0
    if go == 'F':
        dx, dy = dir_mul(dir, num)
    elif go == 'R' or go == 'L':
        if num % 90 != 0:
            print(go, num)
        if num == 180:
            dir = dir_mul(dir, -1)
            continue
        elif num == 270:
            if go == 'R':
                go = 'L'
            elif go == 'L':
                go = 'R'
        if dir == (1, 0):
            dir = (0, 1)
        elif dir == (0, 1):
            dir = (-1, 0)
        elif dir == (-1, 0):
            dir = (0, -1)
        elif dir == (0 , -1):
            dir = (1, 0)
        if go == 'L':
            dir = (dir[0] * -1, dir[1] * -1)
    elif go == 'N':
        dx, dy = 0, -1 * num
    elif go == 'E':
        dx, dy = num, 0
    elif go == 'S':
        dx, dy = 0, num
    elif go == 'W':
        dx, dy = -1 * num, 0
    x += dx
    y += dy

print(f"p1 = {abs(x) + abs(y)}")

x, y = 0, 0
sx, sy = 10, -1

for line in inp.split():
    go, num = line[0], int(line[1:])
    dx, dy = 0, 0
    if go == 'N':
        sy -= num
    elif go == 'E':
        sx += num
    elif go == 'S':
        sy += num
    elif go == 'W':
        sx -= num
    elif go == 'F':
        dx, dy = sx * num, sy * num
    else: # L or R
        if num == 270 and go == 'R':
            go = 'L'
        elif num == 270 and go == 'L':
            go = 'R'
        elif num == 180:
            sx, sy = sx * -1, sy * -1
            continue
        if go == 'R':
            sx, sy = -1 * sy, sx
        elif go == 'L':
            sx, sy = sy, -1 * sx
        continue
    x += dx
    y += dy
print(f"p2 = {abs(x) + abs(y)}")
