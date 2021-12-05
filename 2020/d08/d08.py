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


def run_prog(prog, *, target = None, num_loops = 0):
    if target == None:
        target = len(prog)
    acc = 0
    pc = 0
    seen = set()
    last_seen = {-1,-1,-1}
    seen_match = 0
    rc = -999
    while 0 <= pc < target:
        if pc in seen:
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

    pr2 = prog[:]
    p1 = run_prog(pr2, num_loops = -1)[2]
    print(f"p1 = {p1}")
    for i, line in enumerate(prog):
        old_op, num = line
        if old_op == 'acc':
            continue
        elif old_op == 'jmp':
            new_op = 'nop'
        elif old_op == 'nop':
            new_op = 'jmp'
        pr2[i] = (new_op, num)
        res = run_prog(pr2)
        if res[0] == 0:
            print(f"p2 = {res[2]}")
            break
        else:
            pr2[i] = (old_op, num)
    else:
        print("nothing found")
    #print(acc, i, prog[i], pr2[i], (op, num), res, len(prog))
