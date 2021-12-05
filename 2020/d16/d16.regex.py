import re

field_pattern = re.compile(r'([^:]+): (\d+)-(\d+) or (\d+)-(\d+)')

def d16(inp):
    str_valid_fields, str_my_ticket, str_nearby_tickets = inp.split('\n\n')

    valid_fields = {}
    valid_locs = {}
    all_fnames = set()
    all_fields = {*range(str_my_ticket.count(',') + 1)}
    for i, line in enumerate(str_valid_fields.strip().split('\n')):
        fname, slow1, shi1, slow2, shi2 = field_pattern.fullmatch(line.strip()).groups()
        valid_fields[fname] = [i, int(slow1), int(shi1), int(slow2), int(shi2)]
        valid_locs[fname] = all_fields.copy()
        all_fnames.add(fname)

    my_ticket = [int(num) for num in str_my_ticket.strip().split('\n')[1].strip().split(',')]

    invalid_sum = 0
    for line in str_nearby_tickets.strip().split('\n')[1:]:
        nums = map(int, line.strip().split(','))
        for i, num in enumerate(nums):
            ever_valid = set()
            for fname, (j, l1, h1, l2, h2) in valid_fields.items():
                if l1 <= num <= h1 or l2 <= num <= h2:
                    ever_valid.add(fname)
            if ever_valid:
                for fname in all_fnames - ever_valid:
                    valid_locs[fname].discard(i)
            else:
                invalid_sum += num

    any_mult = {"",}
    wide_fnames = all_fnames.copy()
    while any_mult:
        wide_fnames -= any_mult
        any_mult.clear()
        for fname in wide_fnames:
            if len(valid_locs[fname]) == 1:
                num = valid_locs[fname].copy().pop()
                for other_fname in wide_fnames:
                    if fname == other_fname:
                        continue
                    if num in valid_locs[other_fname]:
                        valid_locs[other_fname].discard(num)
                        any_mult.add(fname)
    prod = 1
    for fname in valid_fields:
        valid = valid_locs[fname]
        if fname.startswith('departure') and len(valid) == 1:
            prod *= my_ticket[valid.pop()]
    return invalid_sum, prod

def run_tests():
    cases = [
        #(p1, p2, inp),
        (71 , None, """class: 1-3 or 5-7
        row: 6-11 or 33-44
        seat: 13-40 or 45-50

        your ticket:
        7,1,14

        nearby tickets:
        7,3,47
        40,4,50
        55,2,20
        38,6,12"""),
    ]

    for want_p1, want_p2, inp in cases:
        p1, p2 = d16(inp)
        if want_p1 is not None:
            assert want_p1 == p1, f"expected = {want_p1}, got = {p1}"
        if want_p2 is not None:
            assert want_p2 == p2

def main():
    with open('../inputs/d16.txt') as f:
        inp = f.read().strip()
    p1, p2 = d16(inp)
    assert (p1, p2) == (21081, 314360510573), "input incorrect or changed"
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()
