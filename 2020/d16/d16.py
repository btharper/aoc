def d16(inp):
    str_valid_fields, str_my_ticket, str_nearby_tickets = inp.split('\n\n')

    valid_fields = {}
    ranges = []
    num_fields = str_my_ticket.count(',') + 1
    for i, line in enumerate(str_valid_fields.strip().split('\n')):
        field_name, str_values = line.split(':')
        str_1, str_2 = str_values.strip().split(' or ')
        slow1, shi1 = str_1.strip().split('-')
        slow2, shi2 = str_2.strip().split('-')
        low1, hi1, low2, hi2 = int(slow1), int(shi1), int(slow2), int(shi2)
        valid_fields[field_name.strip()] = [i, low1, hi1, low2, hi2, {*range(num_fields),}]
        ranges.append([low1, hi1])
        ranges.append([low2, hi2])
    #for rng in ranges:
        #print(rng)

    #for line in str_my_ticket.strip().split('\n')[1].strip().split(','):
    #    pass
    my_ticket = list(map(int, str_my_ticket.strip().split('\n')[1].strip().split(',')))

    invalid_sum = 0
    all_idxs = {*range(num_fields)}
    all_fnames = {*valid_fields.keys()}
    for line in str_nearby_tickets.strip().split('\n')[1:]:
        #print(f"line = {line.strip()}")
        nums = map(int, line.strip().split(','))
        for i, num in enumerate(nums):
            ever_valid = set()
            for fname, (j, l1, h1, l2, h2, si) in valid_fields.items():
                if l1 <= num <= h1 or l2 <= num <= h2:
                    ever_valid.add(fname)
            #for rlow, rhi in ranges:
            #    #print(f"{rlow}, {rhi}, {rlow <= num}, {num <= rhi}")
            #    if rlow <= num <= rhi:
            #        ever_valid = True
            #        break
            #else:
                #print(f"\tnever valid = {num}")
            if not ever_valid:
                invalid_sum += num
            else:
                for fname in all_fnames - ever_valid:
                    #print(f"dbg {fname=}, {i=}")
                    valid_fields[fname][5].discard(i)

    
    any_mult = True
    wide_fnames = all_fnames.copy()
    while any_mult:
        any_mult = False
        for fname in wide_fnames:
            if len(valid_fields[fname][5]) == 1:
                num = valid_fields[fname][5].copy().pop()
                for other_fname in wide_fnames:
                    if fname == other_fname:
                        continue
                    if num in valid_fields[other_fname][5]:
                        valid_fields[other_fname][5].discard(num)
                        any_mult = True
    prod = 1
    for fname in valid_fields:
        valid = valid_fields[fname][5]
        print(f"{fname=} {valid=}")
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
    print(f"p1 = {p1}\np2 = {p2}")

if __name__ == '__main__':
    run_tests()
    main()
