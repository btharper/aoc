from enum import Enum, auto
from collections import Counter, deque, ChainMap, defaultdict

class Status(Enum):
    RUNNING = auto()
    LOOP = auto()
    CYCLE = auto()
    BAD_PC = auto()
    HIT_TARGET = auto()
    NEED_INPUT = auto()
    NEED_OUTPUT = auto()

def input_prog(day):
    prog = []

    with open(f'../inputs/d{day:02d}.txt') as f:
        #inp = f.read()
        for line in f.readlines():
            if len(line) < 3:
                continue
            op, num = line.split()
            prog.append((op, int(num)))
    return prog

def clean_state(**kwargs):
    kwargs.setdefault('acc', 0)
    kwargs.setdefault('pc', 0)
    kwargs.setdefault('seen', set())
    kwargs.setdefault('status', Status.RUNNING)
    return kwargs

def run_prog(prog, state, *, target = None, num_loops = 0):
    if 'target' not in state:
        state['target'] = len(prog)
    last_seen = {-1,-1,-1}
    seen_match = 0
    rc = -999
    while 0 <= state['pc'] < state['target']:
        if state['pc'] in state['seen']:
            if num_loops == -1:
                rc = -1
                break
            elif seen == last_seen:
                seen_match += 1
                if seen_match > num_loops:
                    rc = -2
                    break
            last_seen = seen
            seen = set()
        seen.add(pc)
        op, num = prog[pc]
        if op == "acc":
            acc += num
            pc += 1
        elif op == "nop":
            pc += 1
        elif op == "jmp":
            pc = pc + num
    if pc == target:
        rc = 0
    else:
        rc = -3
    return (rc, pc, acc)

if __name__ == "__main__":
    prog = input_prog(8)
    #print(inp)
    #print(repr(inp[:20]))
    #print(inp.split('\n')[:4])

    state = clean_state()
    run_prog(prog, state)
