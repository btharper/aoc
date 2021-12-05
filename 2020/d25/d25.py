import textwrap as tw
from collections import Counter, deque, defaultdict
import re
from itertools import product

def d25(inp):
    p1, p2 = 0, 0

    key1, key2 = map(int, inp.split())
    n = 7
    p1 = key2
    while n != key1:
        n = (n * 7) % 20201227
        p1 = (p1 * key2) % 20201227
#        print(f"{p1:_}")
    return p1, p2

def run_tests():
    cases = [
        #(p1, p2, inp),
        (14897079, None, """
        5764801
        17807724
        """),
    ]

    for i, (want_p1, want_p2, inp) in enumerate(cases):
        inp = tw.dedent(inp).strip()
        p1, p2 = d25(inp)
        if want_p1 is not None:
            assert want_p1 == p1, f"Test{i:02d}-p1 {dict(want=want_p1, got=p1, i=i)}"
        if want_p2 is not None:
            assert want_p2 == p2, f"Test{i:02d}-p2 {dict(want=want_p2, got=p2, i=i)}"

def main():
    with open('../inputs/d25.txt') as f:
        inp = f.read().strip()
    p1, p2 = d25(inp)
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()
