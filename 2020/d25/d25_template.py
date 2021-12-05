import textwrap as tw
from collections import Counter, deque, defaultdict
import re
from itertools import product

def d25(inp):
    p1, p2 = 0, 0

    

    return p1, p2

def run_tests():
    cases = [
        #(p1, p2, inp),
    ]

    for want_p1, want_p2, inp in cases:
        p1, p2 = d25(inp)
        if want_p1 is not None:
            assert want_p1 == p1
        if want_p2 is not None:
            assert want_p2 == p2

def main():
    with open('../inputs/d25.txt') as f:
        inp = f.read().strip()
    p1, p2 = d25(inp)
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()
