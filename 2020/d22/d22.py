from collections import Counter, deque, defaultdict
from itertools import product

def score_deque(deck):
    #print("Scoring deck\n", deck)
    total = 0
    mul = 1
    while deck:
        total += mul * deck.pop()
        #print(deck)
        mul += 1
    #print("returning deck", total)
    return total

game_num = 1
def recursive_combat(d1, d2, score=False):
    global game_num
    game = game_num
    game_num += 1
    history = set()
    #print(f"=== Game {game} ===\n")
    round = 0
    while d1 and d2:
        round += 1
        #print(f"-- Round {round} (Game {game}) --")
        #print(f"Player 1's deck: {', '.join(map(str, d1))}")
        #print(f"Player 2's deck: {', '.join(map(str, d2))}")
        round_state = (*d1, -1, *d2)
        if round_state in history:
            #print(f"Player 1 wins the game: Loop!")
            if score:
                return score_deque(d1)
            return 1
        else:
            history.add(round_state)
            c1, c2 = d1.popleft(), d2.popleft()
            #print(f"Player 1 plays: {c1}")
            #print(f"Player 2 plays: {c2}")
            if c1 <= len(d1) and c2 <= len(d2):
                rd1 = deque((*d1,)[:c1])
                rd2 = deque((*d2,)[:c2])
                #print(f"Playing a sub-game to determine the winner...\n")
                round_result = recursive_combat(rd1, rd2)
                #print(f"...anyway, back to game <num>")
            elif c1 > c2:
                round_result = 1
            elif c2 > c1:
                round_result = 2
            else:
                #print(f"{c1=} {c2=} {d1=} {d2=}")
                raise Exception('Bad state')
        if round_result == -1:
            if score:
                return score_deque(d1)
            return -1
        elif round_result == 1:
            #print(f"Player 1 wins round {round} of game {game}!\n")
            d1.append(c1)
            d1.append(c2)
        elif round_result == 2:
            #print(f"Player 1 wins round {round} of game {game}!\n")
            d2.append(c2)
            d2.append(c1)
        else:
            raise Exception("Bad state 2")
    if score:
        #print(f"returning score")
        return score_deque(d1) + score_deque(d2)
    return round_result

def d22(inp):
    #print("running input", inp, sep='\n\n')
    p1, p2 = 0, 0

    pys = inp.split('Player')[1:]
    d1, d2 = deque(map(int, pys[0].strip(':\n').split('\n')[1:])), deque(map(int, pys[1].strip(':\n').split('\n')[1:]))

    p2_copy = d1.copy(), d2.copy()

    ### Part 1
    #print("Starting part 1")
    history = set()
    while d1 and d2:
        history_entry = (*d1, -1, *d2)
        #print(history_entry)
        if history_entry in history:
            p1 = score_deque(d1)
            break
        history.add(history_entry)
        p1c, p2c = d1.popleft(), d2.popleft()
        if p1c > p2c:
            d1.extend((p1c, p2c))
        else:
            d2.extend((p2c, p1c))
    p1 = score_deque(d1) + score_deque(d2)
    #print("finished part 1", p1)
    ### Part 2
    d1, d2 = p2_copy

    p2 = recursive_combat(d1, d2, score=True)
    #print(f"returned from rec combt")

    return p1, p2

def run_tests():
    cases = [
        #(p1, p2, inp),
        (306, 291, """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""),
    (None, None, """Player 1:
43
19

Player 2:
2
29
14"""),
    (None, 34700, """Player 1:
22
41
30
6
9
1
50
4
40
33
12
19
15
24
7
2
11
5
48
20
34
35
31
16
17

Player 2:
27
25
46
29
28
23
36
32
13
8
45
42
10
26
39
43
3
44
47
21
18
49
37
14
38

"""),
    (None, 34361, """Player 1:
42
19
8
46
26
16
27
43
14
38
41
5
20
49
39
10
29
21
22
6
36
44
34
3
2

Player 2:
48
25
45
4
33
40
32
18
50
31
13
37
47
24
30
23
1
15
12
35
7
17
11
9
28

"""),
    (None, 33719, """Player 1:
19
44
1
38
6
11
46
45
41
20
25
4
3
43
36
23
17
10
5
37
35
13
18
9
34

Player 2:
12
7
31
28
14
26
30
27
29
8
40
15
39
47
50
21
16
22
48
49
32
33
2
42
24

"""),
    (None, 32509, """Player 1:
18
43
32
25
29
13
36
4
46
1
34
10
49
39
48
7
37
42
45
9
20
3
26
17
40

Player 2:
22
5
47
31
33
16
24
50
15
38
2
11
6
41
35
27
44
14
12
28
19
21
30
8
23

"""),
    (None, 34101, """Player 1:
30
16
12
39
29
20
27
31
32
9
22
40
4
25
47
50
24
42
48
1
6
28
37
45
7

Player 2:
26
41
11
2
19
34
13
10
18
15
8
44
35
33
17
43
21
14
49
46
3
5
38
36
23

"""),
    (None, 33007, """Player 1:
40
34
4
19
43
32
35
16
13
8
10
41
5
22
48
30
15
21
37
49
45
25
11
20
24

Player 2:
46
1
6
2
17
12
33
42
23
36
38
26
18
3
50
28
9
47
27
29
44
39
31
7
14

"""),
    (None, 32327, """Player 1:
13
36
43
47
12
14
27
22
5
3
19
32
42
6
15
39
26
49
7
45
46
38
25
28
30

Player 2:
40
18
41
10
4
20
24
33
31
29
34
23
37
16
1
9
50
48
11
44
2
21
35
8
17

"""),
    (None, 32686, """Player 1:
44
9
7
16
22
20
37
23
26
17
4
5
6
41
30
27
43
48
25
12
28
36
8
35
2

Player 2:
33
40
42
24
31
49
34
32
18
10
1
19
15
38
21
39
50
46
11
3
14
45
29
13
47

"""),
    (None, 31397, """Player 1:
44
1
17
13
11
50
26
49
8
42
46
25
29
48
34
36
4
7
14
32
43
38
19
28
20

Player 2:
30
5
33
31
40
18
24
22
6
41
37
21
3
35
10
16
23
15
12
9
47
39
27
45
2

"""),
    (None, 34962, """Player 1:
15
2
37
26
50
7
41
42
47
5
48
20
36
11
6
33
39
28
8
17
3
44
14
43
12

Player 2:
19
16
30
32
22
21
9
40
1
35
23
25
34
13
49
38
24
10
29
27
18
46
4
45
31

"""),
    (None, 31783, """Player 1:
1
26
43
42
14
16
47
33
50
40
4
8
7
18
25
39
27
21
32
36
28
24
46
31
30

Player 2:
15
10
11
35
34
20
48
49
23
6
19
5
44
22
45
41
2
12
17
9
37
13
29
3
38

"""),
    (None, 32716, """Player 1:
19
22
21
38
14
25
2
8
4
23
40
17
20
47
11
10
29
49
13
48
9
39
45
1
12

Player 2:
28
6
42
50
44
33
30
31
46
27
36
24
3
15
5
41
34
43
18
32
37
26
16
35
7

"""),
    (None, 33403, """Player 1:
27
32
42
45
25
8
36
1
5
46
43
10
19
38
16
17
33
44
26
37
41
30
29
14
47

Player 2:
9
6
39
34
21
31
20
7
40
11
49
2
24
48
12
50
4
35
3
23
28
13
18
22
15

"""),
    (None, 30782, """Player 1:
13
5
31
45
22
30
29
3
27
24
35
7
20
4
49
44
32
17
18
42
39
14
46
25
34

Player 2:
2
37
23
1
33
43
8
40
19
36
26
28
48
6
15
41
21
38
11
12
9
10
16
47
50

"""),
    (None, 33201, """Player 1:
9
11
44
27
6
10
28
49
17
20
39
24
1
26
47
40
34
33
45
29
46
5
50
8
23

Player 2:
25
16
48
21
2
35
13
42
31
36
18
14
30
4
3
12
41
19
15
37
7
22
32
38
43"""),
    ]

    for want_p1, want_p2, inp in cases:
        p1, p2 = d22(inp)
        if want_p1 is not None:
            assert want_p1 == p1
        if want_p2 is not None:
            assert want_p2 == p2, f"want={(want_p1, want_p2)} got={(p1, p2)}"
            #exit()

def main():
    with open('../inputs/d22.txt') as f:
        inp = f.read().strip()
    p1, p2 = d22(inp)
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()
