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
    ]

    for want_p1, want_p2, inp in cases:
        p1, p2 = d22(inp)
        if want_p1 is not None:
            assert want_p1 == p1
        if want_p2 is not None:
            assert want_p2 == p2
            #exit()

def main():
    with open('../inputs/d22.txt') as f:
        inp = f.read().strip()
    p1, p2 = d22(inp)
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()
