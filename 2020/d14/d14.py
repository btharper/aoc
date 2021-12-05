from collections import Counter, defaultdict, deque

def p2_write(mask, addr, mem, val):
    idx = mask.find('X')
    if idx < 0:
        mem[addr] = val
    else:
        new_mask = mask.replace('X', '0', 1)
        shift = 35 - idx
        addr |= 1<<shift
        p2_write(new_mask, addr, mem, val)
        addr ^= 1<<shift
        p2_write(new_mask, addr, mem, val)

def d14(inp):
    lines = inp.split('\n')
    mem = defaultdict(int)
    mem2 = defaultdict(int)
    #print(bin(and_mask))
    #print(bin(or_mask))
    and_mask = int('1' * 36, 2)
    or_mask = 0
    p2 = 0
    writes = []
    for line in lines:
        op, val = line.split(' = ')
        if op[:3] == 'mem':
            addr, val = line.split('] =')
            addr = int(addr.split('[')[-1])
            #print(f"starting {val} into {addr}")
            val = int(val)
            val2 = val
            val &= and_mask
            val |= or_mask
            mem[addr] = val
            #print(f"storing {val} in {addr}")
            for i, char in enumerate(reversed(mask)):
                if char == '1':
                    addr |= 1<<i
            p2_write(mask, addr, mem2, val2)
        elif op[:3] == 'mas':
            mask = line.split('=')[-1].strip()
            and_mask = int(mask.replace('X', '1'), 2)
            or_mask = int(mask.replace('X', '0'), 2)
            #print(mask.count('X'))
        else:
            print(f"bad op = '{op}'")
    p1 = sum(mem.values())
    p2 = sum(mem2.values())
    return p1, p2

def run_tests():
    cases = [
        #(p1, p2, inp),
        #(165, None,
#        """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
#mem[8] = 11
#mem[7] = 101
#mem[8] = 0"""),
        (None, 208,
        """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""),
    ]

    for want_p1, want_p2, inp in cases:
        p1, p2 = d14(inp)
        if want_p1 is not None:
            assert want_p1 == p1, (want_p1, p1)
        if want_p2 is not None:
            assert want_p2 == p2, (want_p2, p2)

def main():
    with open('../inputs/d14.txt') as f:
        inp = f.read().strip()
    p1, p2 = d14(inp)
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()
