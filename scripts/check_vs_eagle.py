"""Compare the KiCad netlist with the Eagle board netlist (eagle_nets.py output), using the ref mapping below.
Two-terminal non-polar parts (R, film C) are compared without pin order."""
import re, sys
M = {'IC1': 'U1', 'IC2': 'U2', 'RATE': 'RV1', 'DEPTH': 'RV2', 'TRIM': 'RV3', 'TREM': 'SW1', 'RLED': 'R15', 'IN': 'J1', 'IG': 'J2', 'OUT': 'J3', 'OG': 'J4', 'V+': 'J5', 'V-': 'J6', 'LS': 'J7', 'LG': 'J8'}
PAD = {'+': '1', '-': '2', 'A': '2', 'C': '1', 'ANODE': '2', 'P$1': '1'}
NONPOL = lambda r: re.match(r'^(R\d+|C[3-7])$', r)
def mp(ref, pad):
    r = M.get(ref, ref)
    if ref.startswith('D') or ref in ('C1', 'C2'): pad = PAD.get(pad, pad)
    return (r, '*' if NONPOL(r) else pad)
def norm(nets):
    return sorted(sorted(n) for n in nets if len(n) > 1)
truth = []
for l in open(sys.argv[1]):
    p = l.split()
    if len(p) < 2 or "('" in l: continue
    truth.append(frozenset(mp(*x.rsplit('.', 1)) for x in p[1:]))
got = []
for blk in re.split(r'\(net\s*\(code', open(sys.argv[2]).read())[1:]:
    got.append(frozenset((r, '*' if NONPOL(r) else p) for r, p in re.findall(r'\(ref "([^"]+)"\)\s*\(pin "([^"]+)"', blk)))
# with pin order ignored, each non-polar part must still have one pin in each of two different nets
T, G = norm(truth), norm(got)
print('matches Eagle board:', T == G)
for x in T:
    if x not in G: print(' eagle only:', x)
for x in G:
    if x not in T: print(' kicad only:', x)
