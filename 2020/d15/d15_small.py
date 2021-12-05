import time
from collections import defaultdict, Counter, deque, ChainMap
from itertools import product
from multiprocessing import Pool

def d15(inp):
    p1, p2 = None, None

    turn_spoken = ChainMap()
    num_hidden = 0
    maps_hidden = 0
    low_len = 1024
    max_sz = 1024 * 4
    low_nums = [0] * low_len
    cnt = Counter()
    big = {}
    mx = 0
    #turn_spoken = [-1] * 30_000_000
    #turn_spoken = [-1] * 29_600_000
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

    #zero_next = set()
    while turn <= 30_000_000:
        if turn % 1_000_000 == 0:
            print(f"{turn=:_}")
        last_spoken = num_spoken
        #max_spoken = max(max_spoken, last_spoken)
        if last_spoken < low_len:
            num_spoken = turn - low_nums[last_spoken]
        elif last_spoken in turn_spoken:
        #if turn_spoken[last_spoken] >= 0:
            num_spoken = turn - turn_spoken[last_spoken]
            #zero_next.discard(last_spoken)
        else:
            #zero_next.add(last_spoken)
            num_spoken = 0
        cnt[num_spoken] += 1
        #mx = max(mx, num_spoken)
        if num_spoken > mx:
            mx = num_spoken
            #print(f"{mx}")
        if last_spoken < low_len:
            low_nums[last_spoken] = turn
        else:
            if len(turn_spoken.maps[0]) >= max_sz:
                while len(turn_spoken.maps) > 1:
                    mrg = turn_spoken.maps.pop(0)
                    hidden = len(mrg) + len(turn_spoken.maps[0])
                    turn_spoken.maps[0].update(mrg)
                    hidden -= len(turn_spoken.maps[0])
                    num_hidden += hidden
                    maps_hidden += 1
                turn_spoken = turn_spoken.new_child()
            turn_spoken[last_spoken] = turn
        turn += 1
        #max_spoken = max(max_spoken, num_spoken)
        if turn == 2020:
            p1 = num_spoken
        elif turn == 30_000_000:
            p2 = num_spoken
            break
        #if 6000 <= turn <= 6025:
        #if turn < 100:
        #    print(f"{turn=} {num_spoken=}")

    #p1 = num_spoken
    #print(f"{inp}, {(p1,p2)}, {len(turn_spoken)}, {max_spoken}")
    print(f"{inp}, {(p1,p2)}, {len(turn_spoken):_}")
    prev = 0
    for i in (4, 16, 64, 124, 252):
        curr = sum(v for k,v in cnt.items() if k < (i // 4 * 1024 ))
        print(f"{i: 4d} {curr - prev:8d} {curr:8d} {(curr - prev) / 300000: 3.2f} {(30_000_000 - curr) / 300_000: 3.2f}")
        time.sleep(0.001)
        prev = curr

    prev = 0
    total_space = 0
    for i in range(7, 32,7):
        curr = sum(v for k, v in cnt.items() if k < (2**i))
        total_space += (i // 7) * (curr - prev)
        print(f"{i: 4d} {curr - prev:8d} {curr:8d} {(curr - prev) / 300000: 3.2f} {(30_000_000 - curr) / 300_000: 3.2f} space_k={total_space/1024}")
        time.sleep(0.001)
        prev = curr

    prev = 0
    total_space=0
    for i in range(15, 32,15):
        curr = sum(v for k, v in cnt.items() if k < (2**i))
        total_space += (i // 15 * 2) * (curr - prev)
        print(f"{i: 4d} {curr - prev:8d} {curr:8d} {(curr - prev) / 300000: 3.2f} {(30_000_000 - curr) / 300_000: 3.2f} space_k={total_space/1024}")
        time.sleep(0.01)
        prev = curr

    print(f"num maps: len(turn_spoken.maps)={len(turn_spoken.maps)+maps_hidden:_}")
    print(f"mem_MB = {(sum(len(m) for m in turn_spoken.maps) + num_hidden)* 8 // 1024 // 32 / 32:_}")
    print(f"num slots = {(sum(len(m) for m in turn_spoken.maps) + num_hidden):_}")

    #print(cnt.most_common()[:-21:-1])
    #print({k:v for k,v in cnt.items() if v == 1})
    print(  f"cnt v=1 {len([1 for k,v in cnt.items() if v==1]):_}",
            f"min v=1 {min(k for k,v in cnt.items() if v == 1):_}",
            #f"cnt[min v=1] {cnt[min(k for k,v in cnt.items() if v == 1)]:_}",
            #f"min v=1 {min(v for k,v in cnt.items() if v == 1):_}",
            #f"max v>1 {max(k for k,v in cnt.items() if v > 1):_}",
            #f"cnt[max v>1] {cnt[max(k for k,v in cnt.items() if v > 1)]:_}",
            #f"cnt[mx] {cnt[mx]:_}, {mx=}",
            #f"{len(zero_next)=:_} / {len(turn_spoken):_} {100 * len(zero_next) / len(turn_spoken): 3.2f}% min_skip={min(zero_next):_}",
            "", "", sep='\n')
    #print("big =\n", big, mx)
    #exit()
    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d15(inp)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
    return True

def main(inp):
    return d15(inp)

if __name__ == '__main__':
    with open('../inputs/d15.txt') as f:
        inp = f.read().strip()

    cases = [
        #(id, inp, p1, p2),
        (0, "0,3,6", 436, 175594),
        (1, "1,3,2", 1, 2578),
        (2, "2,1,3", 10, 3544142),
        (3, "1,2,3", 27, 261214),
        (4, "2,3,1", 78, 6895259),
        (5, "3,2,1", 438, 18),
        (6, "3,1,2", 1836, 362),
        ('inp', inp, 421, 436),
    ]

    # Non multiprocessing version
    for case in cases:
        validate_test(*case)
    p1, p2 = main(inp)
    print(f"p1 = {p1}\np2 = {p2}")
