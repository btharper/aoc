from collections import defaultdict, Counter, deque
from itertools import product
from multiprocessing import Pool
import re

do_p2 = False

def check_board(board):
    for x in range(5):
        row = col = 0
        for y in range(5):
            if (x,y) in board['marked']:
                row += 1
            if (y,x) in board['marked']:
                col += 1
        if col == 5 or row == 5:
            return True
    return False

def d04(inp, sample=False):
    p1, p2 = None, None
    #verbose = sample
    verbose = False

    groups = list(map(lambda x:x.strip(), inp.split('\n\n')))
    nums = groups[0]
    boards_str = groups[1:]
    num_boards = len(boards_str)

    nums = list(map(int, nums.split(',')))
    boards = []
    for board_str in boards_str:
        b = {'total':0, 'marked': {}, 'done':False}
        for y, row in enumerate(board_str.split('\n')):
            for x, n in enumerate(row.strip().split()):
                if verbose:
                    print(f"@{(x,y)=} = {int(n)}")
                b[x,y] = int(n)
                b[int(n)] = (x,y)
                b['total'] += int(n)
        verbose = False
        boards.append(b)
    #print(*boards, sep='\n\n')

    for num in nums:
        for board in boards:
            if board['done']:
                continue
            if num in board:
                board['total'] -= num
                board['marked'][board[num]] = True
                if check_board(board):
                    #print(board)
                    if p1 is None:
                        p1 = board['total'] * num
                    board['done'] = True
                    num_boards -= 1
                    if num_boards == 0:
                        p2 = board['total'] * num
                        break
        if p2 is not None:
            break

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d04(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d04.txt') as f:
        inp = f.read().strip()
    return d04(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

        22 13 17 11  0
         8  2 23  4 24
         21  9 14 16  7
          6 10  3 18  5
           1 12 20 15 19

            3 15  0  2 22
             9 18 13 17  5
             19  8  7 25 23
             20 11 10 24  4
             14 21 16 12  6

             14 21 17 24  4
             10 16 15  9 19
             18  8 23 26 20
             22 11 13  6  5
              2  0 12  3  7""", 4512,1924),
    ]

    """
    # Non multiprocessing version
    for case in cases:
        validate_test(*case)
    p1, p2 = main()
    print(f"p1 = {p1}\np2 = {p2}")
    """


    with Pool(processes=min(8, len(cases) + 1)) as pool:
        main_res = pool.apply_async(main)
        test_res = [pool.apply_async(validate_test, case) for case in cases]
        test_pass, do_p1, do_p2 = True, False, False
        for test in test_res:
            tp, dp1, dp2 = test.get(30)
            test_pass &= tp
            do_p1 |= dp1
            do_p2 |= dp2
        if test_pass:
            p1, p2 = main_res.get(60)
            assert do_p1 or do_p2, "Didn't run any tets"
            assert p1 is None or do_p1 == True, "Got P1 value without 'do_p1' set"
            assert p2 is None or do_p2 == True, "Got P2 value without 'do_p2' set"
            print(f"p1 = {p1}\np2 = {p2}")
