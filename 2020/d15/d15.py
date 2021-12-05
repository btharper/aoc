from collections import Counter, defaultdict, deque

def d15(inp):
    turn_spoken = {}
    #turn_spoken = [-1] * 30000000
    #turn_spoken = [-1] * 29600000
    last_spoken = None
    num_spoken = None
    turn = 0
    #max_spoken = 0
    for line in inp.split(','):
        last_spoken = num_spoken
        num_spoken = int(line)
        if last_spoken is not None:
            #max_spoken = max(max_spoken, last_spoken)
            turn_spoken[last_spoken] = turn
        turn += 1
    #print(turn_spoken)

    while True:
        last_spoken = num_spoken
        #max_spoken = max(max_spoken, last_spoken)
        if last_spoken in turn_spoken:
        #if turn_spoken[last_spoken] >= 0:
            num_spoken = turn - turn_spoken[last_spoken]
        else:
            num_spoken = 0
        turn_spoken[last_spoken] = turn
        turn += 1
        #max_spoken = max(max_spoken, num_spoken)
        if turn == 2020:
            p1 = num_spoken
        elif turn == 30000000:
            p2 = num_spoken
            break
        #if 6000 <= turn <= 6025:
        #if turn < 100:
        #    print(f"{turn=} {num_spoken=}")

    #p1 = num_spoken
    #print(f"{inp}, {(p1,p2)}, {len(turn_spoken)}, {max_spoken}")
    print(f"{inp}, {(p1,p2)}, {len(turn_spoken)}")
    return p1, p2

def run_tests():
    cases = [
        #(p1, p2, inp),
        (436, 175594, "0,3,6"),
        (1, 2578, "1,3,2"),
        (10, 3544142, "2,1,3"),
        (27, 261214, "1,2,3"),
        (78, 6895259, "2,3,1"),
        (438, 18, "3,2,1"),
        (1836, 362, "3,1,2"),
    ]

    for want_p1, want_p2, inp in cases:
        p1, p2 = d15(inp)
        if want_p1 is not None:
            assert want_p1 == p1
        if want_p2 is not None:
            assert want_p2 == p2

def main():
    with open('../inputs/d15.txt') as f:
        inp = f.read().strip()
    p1, p2 = d15(inp)
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()
