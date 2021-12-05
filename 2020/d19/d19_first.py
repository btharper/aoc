import re

def d19(inp):
    p1, p2 = 0, 0

    rules, messages = inp.split('\n\n')
    p1_rdict = {}
    p2_rdict = {}
    unmatched = True
    while unmatched:
        unmatched = False
        for rule in rules.split('\n'):
            rule_num, rulestr = rule.split(':')
            rule_num, rulestr = rule_num.strip(), rulestr.strip()
            if rule_num in p1_rdict:
                continue
            if len(rulestr) >= 3 and rulestr[0] == '"' and rulestr[-1] == '"':
                # got literal
                parsed_rule = rulestr.strip('"')
                p1_rdict[rule_num] = parsed_rule
                p2_rdict[rule_num] = parsed_rule
                continue
            rulesplit = rulestr.split()
            if all(point in p1_rdict for point in rulesplit):
                assert all(point in p2_rdict for point in rulesplit)
                # no concat
                parsed_rule = ''.join(p1_rdict[n] for n in rulesplit)
                p1_rdict[rule_num] = parsed_rule
                #if rule_num == '8' and rulestr == '42':
                    #p2_rdict['8'] = '(?:' + p2_rdict['42'] + ')+'
                    #print(f"rdict['8'] = {p2_rdict['8']}")
                #el
                if rule_num == '0' and rulestr == '8 11':
                    """
                    When 0: 8 11 and 8: 42 | 42 8 and 11: 42 31 | 42 11 31
                    Then 0: 42{n} 42{k} 31{k} for any k >= 1 and n >=1
                    or   0: 42 42{n} 31{m} where m > 1 and n >= m
                    """
                    p2_rdict['0'] = p2_rdict['42'] + p2_rdict['11']
                elif rule_num == '0':
                    p2_rdict['0'] = '(' + parsed_rule + ')(z?)'
                elif rule_num == '11' and rulestr == '42 31':
                    #print(f"{rulesplit}")
                    #print(f"rdict['11'] =\n{p2_rdict['42']}\n(11)\n{p2_rdict['31']}")
                    p42 = p2_rdict['42']
                    p31 = p2_rdict['31']
                    """
                    11: 42 31 | 42 11 31 means we need at least one '42 31' pair, then more flanking
                    RE's can't count, so that's done later with the captured groups
                    """
                    #p2_rdict['11'] = '((?:' + p42 + ')+)' + p42 + p31  + '((?:' + p31 + ')+)'
                    p2_rdict['11'] = f'((?:{p42})*){p42}{p31}((?:{p31})*)'
                else:
                    p2_rdict[rule_num] = parsed_rule
            elif all(point == '|' or point in p1_rdict for point in rulesplit):
                assert all(point == '|' or point in p2_rdict for point in rulesplit)
                chunks = rulestr.split(' | ')
                chunk_patterns = [''.join(p1_rdict[n] for n in chunk.split()) for chunk in chunks]

                parsed_rule = '(?:' + '|'.join(chunk_patterns) + ')'
                p1_rdict[rule_num] = parsed_rule
                p2_rdict[rule_num] = parsed_rule
            else:
                unmatched = True
    assert '0' in p1_rdict

    p1_pattern = re.compile(p1_rdict['0'])
    p2_pattern = re.compile(p2_rdict['0'])
    if do_p2 := '42' in p2_rdict and '31' in p2_rdict and '11' in p2_rdict and p2_rdict['11'] in p2_rdict['0']:
        a_pattern = re.compile(p2_rdict['42'])
        b_pattern = re.compile(p2_rdict['31'])
    for line in messages.split('\n'):
        if p1_pattern.fullmatch(line):
            #print(len(line))
            p1 += 1
        if do_p2 and (m := p2_pattern.fullmatch(line)):
            #print(f"\n{p2_rdict['0']}\n\n{m}")
            #part_a = m.group(1)
            #part_b = m.group(2)
            part_a, part_b = m.groups()
            a_cnt = len(list(a_pattern.finditer(part_a)))
            b_cnt = len(list(b_pattern.finditer(part_b)))
            #if len(re.split(p2_rdict['42'], part_a)) >= len(re.split(p2_rdict['31'], part_b)):
            #print(f"{a_cnt} {b_cnt}")
            if a_cnt >= b_cnt:
                p2 += 1

    return p1, p2

def run_tests():
    cases = [
        #(p1, p2, inp),
        (2, None, """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""),
        (3, 12, """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""),
    ]

    for want_p1, want_p2, inp in cases:
        p1, p2 = d19(inp)
        if want_p1 is not None:
            assert want_p1 == p1, (want_p1, p1)
        if want_p2 is not None:
            assert want_p2 == p2, (want_p2, p2)

def main():
    with open('../inputs/d19.txt') as f:
        inp = f.read().strip()
    p1, p2 = d19(inp)
    assert (p1, p2) == (144, 260), f"{(p1, p2)} != (144, 260)"
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()
