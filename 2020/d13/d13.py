from math import gcd

def d13(inp):
    inpl = inp.split()
    start = int(inpl[0])
    sline = inpl[1].split(',')
    busses = [(i, int(b)) for i, b in enumerate(sline) if b != 'x']

    delay = max(start, busses[0][1])
    quick_bus = None
    step = 1
    p2 = 0
    for x, bus in busses:
        if delay > (bus - (start % bus)):
            quick_bus = bus
            delay = min(delay, bus - (start % bus))
        while (p2 + x) % bus != 0:
            p2 += step
        step = step * bus // gcd(step, bus)
        assert step % bus == 0
    p1 = delay * quick_bus
    return p1, p2

if __name__ == '__main__':
    with open('../inputs/d13.txt') as f:
        inp = f.read().strip()

    inp2 = """939\n7,13,x,x,59,x,31,19"""

    tests = [
        (3417, "0\n17,x,13,19"),
        (754018, "0\n67,7,59,61"),
        (779210, "0\n67,x,7,59,61"),
        (1261476, "0\n67,7,x,59,61"),
        (1202161486, "0\n1789,37,47,1889"),
    ]

    for want, case in tests:
        _, got = d13(case)
        assert want == got, f"test {want=}, {got=}"

    assert d13(inp2) == (295, 1068781), d13(inp2)

    p1, p2 = d13(inp)
    print(f"p1 = {p1}\np2 = {p2}")
