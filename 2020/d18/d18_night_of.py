from collections import defaultdict, Counter, deque
from itertools import product
from multiprocessing import Pool
import re

def paren(inp):
    return calc(inp[1:-1].split())

def calc(*inp):
    q = deque(inp)
    a = int(q.popleft())
    while len(q) > 0:
        op, b = q.popleft(), int(q.popleft())
        if op == '*':
            a = a * b
        elif op == '+':
            a = a + b
        elif op == '-':
            a = a - b
        else:
            print(f"unknown op {a=}; {op=}; {b=}; {inp}")
    return a

def calc_stack2(inp):
    #print(inp)
    vals = inp.replace('(', '( ').replace(')', ' )').split()
    stack = deque()
    for val in vals:
        if val in ('(', '*', '+', '-'):
            #print(f"op {val}")
            stack.append(val)
            continue
        if val == ')':
            #print(f"close paren")
            a = stack.pop()
            op = stack.pop()
            assert op == '('
            assert a == int(a)
            stack.append(a)
        #print(f"work {val}")
        a = int(val)
        while stack:
            print(f"working {stack[-2]}, {stack[-1]} --- {val}")
            op = stack[-1]
            if op == '(':
                continue
            stack.pop()
            b = stack.pop()
            print(f"calc: {b} {op} {a}")
            if op == '*':
                #stack.append(a * b)
                a = b * a
            elif op == '+':
                #stack.append(a + b)
                a = b + a
            elif op == '-':
                #stack.append(b - a)
                a = b - a
            else:
                print(f"bad op: {op=}; {a=}; {b=}")
    return a

def calc_stack_p1(inp):
    #print(inp)
    vals = inp.replace('(', '( ').replace(')', ' )').split()
    stack = deque()
    math = deque(vals)
    parens = 0

    while len(math) + len(stack) > 2:
        #print(f"working {' '.join(map(str, stack))} & {' '.join(map(str, math))}")
        if math[0] == '(':
            if math[2] == ')':
                #print(f"condensing paren {math}")
                math.popleft()
                math.rotate(-1)
                math.popleft()
                math.rotate(1)
                #print(f"done {math}")
                while stack and stack[-1] != '(':
                    math.appendleft(stack.pop())
                    math.appendleft(stack.pop())
            else:
                stack.append(math.popleft())
        elif (len(math) == 1 and len(stack) > 0) or math[1] == ')':
            #stack.append(math.popleft()) # num
            #stack.append(math.popleft()) # )
            while stack and math[0] != '(':
                math.appendleft(stack.pop())
        elif math[1] in ('*', '+', '-'):
            if math[2] == '(':
                stack.append(math.popleft()) # num
                stack.append(math.popleft()) # op
                stack.append(math.popleft()) # (
            else:
                a = int(math.popleft())
                op = math.popleft()
                b = int(math.popleft())
                if op == '*':
                    math.appendleft(a * b)
                elif op == '+':
                    math.appendleft(a + b)
                elif op == '-':
                    math.appendleft(a - b)
                else:
                    assert False, f"math {a} {op} {b} = {math[0]}"
                while stack and stack[-1] != '(':
                    math.appendleft(stack.pop())
                    math.appendleft(stack.pop())
                #print(f"math {a} {op} {b} = {math[0]}")
        else:
            print(f"panic {stack} --- {math}")
            return -1
    return math.pop()

def calc_stack_p2(inp):
    #print(inp)
    ops = ('*', '+', '-')
    symbols = ('(', ')', '*', '+', '-')
    vals = inp.replace('(', '( ').replace(')', ' )').split()
    stack = deque()
    math = deque(map(lambda x: x if x in symbols else int(x), vals))

    #print(inp)
    while stack or len(math) > 1:
        #print(f"working {' '.join(map(str, stack))} & {' '.join(map(str, math))}")
        has_parens = False
        for char in list(math):
            if char == ')':
                break
            elif char == '(':
                while math:
                    char = math.popleft()
                    if char == ')':
                        math.appendleft(char)
                        break
                    stack.append(char)
                while stack[-1] != '(':
                    math.appendleft(stack.pop())
                if stack[-1] == '(' and math[1] == ')':
                    stack.pop()
                    math.rotate(-1)
                    math.popleft()
                    math.rotate(1)
                    stack.reverse()
                    math.extendleft(stack)
                    stack.clear()
        if len(math) < 3:
            stack.reverse()
            math.extendleft(stack)
            stack.clear()
        elif math[0] not in symbols and math[2] not in symbols:
            if math[1] == '+':
                a = math.popleft()
                math.popleft()
                math.appendleft(a + math.popleft())
                stack.reverse()
                math.extendleft(stack)
                stack.clear()
            elif math[1] == '*':
                for char in math:
                    if char == '+' or char == '(':
                        stack.append(math.popleft())
                        stack.append(math.popleft())
                        break
                    elif char == ')':
                        a = math.popleft()
                        math.popleft()
                        math.appendleft(a * math.popleft())
                        break
                    elif char == '*' or isinstance(char, int):
                        pass
                    else:
                        print(f"*****\nunk {char=}\n*****")
                else:
                    a = math.popleft()
                    math.popleft()
                    math.appendleft(a * math.popleft())
        elif math[1] in ops and math[2] == '(':
            stack.append(math.popleft())
            stack.append(math.popleft())
        elif math[0] == '(' and math[2] == ')' and isinstance(math[1], int):
            math.popleft()
            math.rotate(-1)
            math.popleft()
            math.rotate(1)
        elif math[0] == ')' or math[1] == ')':
            stack.reverse()
            math.extendleft(stack)
            stack.clear()
        elif math[0] == '(':
            stack.append(math.popleft())
        else:
            print(f"What do?\n{math[0]} {math[1]} {math[2]}\n{stack} && {math}\n\n")
            break
    #print(f"finished {math[0]}\n")
    return math.pop()

def calc_p2(inp):
    # p2, but no parens
    while m := re.search(r'(?:\d+\s*\+\s*)+\d+', inp):
        val = sum(map(int, m.group().split('+')))
        #   print(f"{m.group()} = {val}")
        inp = inp.replace(m.group(0), str(val))
    prod = 1
    vals = map(int, inp.split('*'))
    for val in vals:
        prod *= val
    return prod

def recur_stack_p2(inp):
    while m := re.search(r'\(([^()]+)\)', inp):
        inp = inp.replace(m.group(0), str(calc_p2(m.group(1))))
    return calc_p2(inp)

def calc_p1(inp):
    #print(f"\t{inp}")
    while m := re.search(r'^\s*(\d+)\s*(\+|\*)\s*(\d+)', inp):
        if m.group(2) == '*':
            val = int(m.group(1)) * int(m.group(3))
        else:
            val = int(m.group(1)) + int(m.group(3))
        #print(f"\t\t{m.group(0)} = {val}")
        inp = inp.replace(m.group(0), str(val), 1)
    #print(f"\t= {inp}")
    return inp

def recur_stack_p1(inp):
    #print(inp)
    while m := re.search(r'\(([^()]+)\)', inp):
        val = calc_p1(m.group(1))
        #print(f"{m.group(0)} = {val}")
        inp = inp.replace(m.group(0), str(val), 1)
    val = int(calc_p1(inp))
    #print("=", val)
    return val

def d18(inp):
    p1, p2 = 0, 0

    for line in inp.split('\n'):
        #assert recur_stack_p1(line) == calc_stack_p1(line), f"{recur_stack_p1(line)} // {calc_stack_p1(line)}\n{line}\n\n"
        p1 += recur_stack_p1(line)
        #assert recur_stack_p2(line) == calc_stack_p2(line)
        p2 += recur_stack_p2(line)

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d18(inp)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
    return True

def main():
    with open('../inputs/d18.txt') as f:
        inp = f.read().strip()
    return d18(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        ('1', '1 + 2 * 3 + 4 * 5 + 6', 71, 231),
        ('2', '1 + (2 * 3) + (4 * (5 + 6))', 51, 51),
        ('3', '2 * 3 + (4 * 5)', 26, 46),
        ('4', '5 + (8 * 3 + 9 + 3 * 4 * 3)', 437, 1445),
        ('5', '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))' , 12240, 669060),
        ('6', '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632, 23340),
    ]

    #"""
    # Non multiprocessing version
    for case in cases:
        validate_test(*case)
    p1, p2 = main()
    #assert p2 > 213702899691555
    assert p1 == 45283905029161, "p1 broke"
    assert p2 == 216975281211165, "p2 broke"
    print(f"p1 = {p1}\np2 = {p2}")
    exit(0)
    #"""


    #with Pool(processes=min(8, len(cases) + 1)) as pool:
    with Pool(processes=1) as pool:
        main_res = pool.apply_async(main)
        test_res = [pool.apply_async(validate_test, case) for case in cases]
        if all(test.get(30) for test in test_res):
            p1, p2 = main_res.get(60)
            assert p1 == 45283905029161, "p1 broke"
            assert p2 == 216975281211165, "p2 broke"
            print(f"p1 = {p1}\np2 = {p2}")
