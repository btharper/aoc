from dataclasses import dataclass
from collections import defaultdict, Counter, deque
from functools import cache
from itertools import product, pairwise
from multiprocessing import Pool
import math
import re
from typing import Any, List

def get_bits(data, start, read_len, data_len):
    val = data >> (data_len - read_len - start)
    val &= (1<<read_len)-1
    return start + read_len, val

def read_header(data, start, data_len):
    start, ver = get_bits(data, start, 3, data_len)
    start, typ = get_bits(data, start, 3, data_len)
    return start, ver, typ

def read_literal(data, start, data_len=None):
    val = 0
    itr = start
    quad = 0x10
    while quad & 0x10:
        itr, quad = get_bits(data, itr, 5, data_len)
        val = (val << 4) + (quad & 0xf)
    return itr, val

def read_packet(data, start, data_len=None):
    itr = start
    itr, p_ver, p_typ = read_header(data, itr, data_len)
    pkt = packet(p_ver, p_typ)
    if pkt.typ == 4: # Literal value
        itr, val = read_literal(data, itr, data_len)
        pkt.data = val
    else:
        itr, val = get_bits(data, itr, 1, data_len)
        pkt.len_type = val
        if val == 0: # 15 bit total sub_pkt len
            itr, val = get_bits(data, itr, 15, data_len)
            pkt.sub_bitlen = val
            sub_data_len = val
            itr, sub_data = get_bits(data, itr, val, data_len)
            sub_itr = 0
            sub_pkts = []
            while sub_itr < sub_data_len:
                sub_itr, sub_pkt = read_packet(sub_data, sub_itr, sub_data_len)
                sub_pkts.append(sub_pkt)
            pkt.sub_pkts = sub_pkts
        elif val == 1: # 11 bit num sub_pkts
            itr, num_sub_pkts = get_bits(data, itr, 11, data_len)
            pkt.sub_numpkts = num_sub_pkts
            sub_pkts = []
            for _ in range(num_sub_pkts):
                itr, sub_pkt = read_packet(data, itr, data_len)
                sub_pkts.append(sub_pkt)
            pkt.sub_pkts = sub_pkts
    return itr, pkt

@dataclass
class packet:
    ver: int
    typ: int
    len_type: int = None
    sub_bitlen: int = None
    sub_numpkts: int = None
    sub_pkts: List[packet] = None
    data: Any = None

def sum_all_versions(main_pkt):
    total = 0
    check = deque()
    check.append(main_pkt)
    while check:
        pkt = check.pop()
        total += pkt.ver
        if pkt.typ != 4:
            check.extend(pkt.sub_pkts)
    return total

def evaluate(pkt):
    typ = pkt.typ
    if typ == 4:
        return pkt.data
    if typ == 0: # sum(...)
        total = 0
        for sub_pkt in pkt.sub_pkts:
            total += evaluate(sub_pkt)
        return total
    elif typ == 1: # product(...)
        total = 1
        for sub_pkt in pkt.sub_pkts:
            total *= evaluate(sub_pkt)
        return total
    elif typ == 2: # min(...)
        ret = evaluate(pkt.sub_pkts[0])
        for sub_pkt in pkt.sub_pkts[1:]:
            ret = min(ret, evaluate(sub_pkt))
        return ret
    elif typ == 3: # max(...)
        ret = evaluate(pkt.sub_pkts[0])
        for sub_pkt in pkt.sub_pkts[1:]:
            ret = max(ret, evaluate(sub_pkt))
        return ret
    elif typ == 5: # sub[0] > sub[1]
        a, b = pkt.sub_pkts
        return int(evaluate(a) > evaluate(b))
    elif typ == 6: # sub[0] < sub[1]
        a, b = pkt.sub_pkts
        return int(evaluate(a) < evaluate(b))
    elif typ == 7: # sub[0] == sub[1]
        a, b = pkt.sub_pkts
        return int(evaluate(a) == evaluate(b))

def d16(inp, sample=False):
    p1, p2 = 0, None

    # Round up just in case
    #ba = bytearray.fromhex(inp.strip())
    data = int(inp.strip(), 16)
    #data_len = math.ceil(data.bit_length()/4)*4
    data_len = len(inp.strip()) * 4

    _, pkt_data = read_packet(data, 0, data_len)
    p1 = sum_all_versions(pkt_data)
    p2 = evaluate(pkt_data)

    return p1, p2

def validate_test(case_id, inp=None, want_p1=None, want_p2=None):
    do_p1, do_p2 = False, False
    newline = '\n'
    #print(f"validate_test({case_id}, {inp}, {want_p1}, {want_p2})")
    got_p1, got_p2 = d16(inp, sample=True)
    if want_p1 is not None:
        assert want_p1 == got_p1, f"{case_id=} p1:\n\t{want_p1=}\n\t{got_p1=}"
        do_p1 = True
    if want_p2 is not None:
        assert want_p2 == got_p2, f"{case_id=} p2:\n\t{want_p2=}\n\t{got_p2=}"
        do_p2 = True
    return True, do_p1, do_p2

def main():
    with open('../inputs/d16.txt') as f:
        inp = f.read().strip()
    return d16(inp)

if __name__ == '__main__':
    cases = [
        #(id, inp, p1, p2),
        (0, "8A004A801A8002F478", 16, None),
        (1, "620080001611562C8802118E34", 12, None),
        (2, "C0015000016115A2E0802F182340", 23, None),
        (3, "A0016C880162017C3686B18A3D4780", 31, None),
        (21, "C200B40A82", None, 3),
        (22, "04005AC33890", None, 54),
        (23, "880086C3E88112", None, 7),
        (24, "CE00C43D881120", None, 9),
        (25, "D8005AC2A8F0", None, 1),
        (26, "F600BC2D8F", None, 0),
        (27, "9C005AC2F8F0", None, 0),
        (28, "9C0141080250320F1802104A08", None, 1),
    ]

    assert read_header(int('6200', 16), 0, 16)[1] == 3, f"{read_header(int('6200', 16), 0)}"

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
            assert p1 == 940
            assert p2 == 13476220616073
            print(f"p1 = {p1}\np2 = {p2}")
