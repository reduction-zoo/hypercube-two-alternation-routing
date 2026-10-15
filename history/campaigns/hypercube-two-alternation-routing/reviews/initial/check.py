"""Reviewer-owned structural and arbitrary-witness extension check; no candidate imports."""
import json
import subprocess
import sys
from pathlib import Path

candidate = Path(__file__).resolve().parents[2] / 'work' / 'algorithm.py'

def run(value, extract=False):
    return json.loads(subprocess.check_output([sys.executable, str(candidate)] + (['--extract'] if extract else []), input=json.dumps(value).encode()))

def ball(center, radius, dim):
    reached = {center}
    frontier = reached
    for _ in range(radius):
        frontier = {v ^ (1 << i) for v in frontier for i in range(dim)} - reached
        reached |= frontier
    return reached

def distance(u, v, mate):
    best = 2*(u ^ v).bit_count()
    if mate.get(u) == v:
        return 1
    for a, b in mate.items():
        best = min(best, 1 + 2*(u ^ a).bit_count() + 2*(b ^ v).bit_count())
    if u in mate and v in mate:
        best = min(best, 2 + 2*(mate[u] ^ mate[v]).bit_count())
    return best

# Extend beyond the recorded d<=2 tests; Q3's even-parity set dominates Q3.
d = 3
source = {'dimension': d, 'active': [1]*8, 'k': 4}
out = run(source)
dim = len(out['cube'])
assert dim == 39
b = 2*d+3
o, s, g, h = [((1 << b)-1) << (d+j*b) for j in range(4)]
T = set(range(8))
slots = sorted(ball(o, d, dim)-ball(o, d-1, dim))[:4]
near = T | {v ^ (1 << i) for v in T for i in range(dim)}
F = (near | ball(o, d+1, dim))-T-set(slots)
expected = {frozenset((v, v ^ h)) for v in F-{o}}
expected |= {frozenset((o,s))}
expected |= {frozenset((v,v ^ g)) for v in ball(s,d,dim)-{s}}
alpha = 8*(d+2)+1
actual = {frozenset((u,v)) for u,v,w in out['demands'] if w == alpha}
assert actual == expected
mate = {}
for edge in actual:
    a,b = sorted(edge)
    assert a not in mate and b not in mate and (a^b).bit_count() >= 9
    mate[a],mate[b] = b,a
assert len(mate) == 2*len(actual)
assert all(v in mate and mate[v] not in T for v in ball(s,d,dim))
assert all(v in mate for v in near-T)
assert all(v in mate for v in ball(o,d+1,dim)-set(slots))
X = sorted(v for v in T if v.bit_count()%2 == 0)
for a,b in zip(X, slots):
    assert a not in mate and b not in mate
    mate[a],mate[b] = b,a
base = sum(w*distance(u,v,mate) for u,v,w in out['demands'])
assert base == out['bound']
# A feasible witness may contain unrelated extra edges, reversed and unordered.
free = [v for v in range(1 << 16) if v not in mate][:2]
assert len(free) == 2
mate[free[0]],mate[free[1]] = free[1],free[0]
edges = [[b,a] for a,b in mate.items() if a < b][::-1]
assert sum(w*distance(u,v,mate) for u,v,w in out['demands']) <= out['bound']
recovered = run({'source':source,'target_solution':edges}, True)
assert recovered == X
assert all(any((u^v).bit_count() <= 1 for v in recovered) for u in T)
print(json.dumps({'dimension':d,'cube_dimension':dim,'forced_edges':len(actual),'canonical_cost':base,'bound':out['bound'],'extra_edge':free,'recovered':recovered,'passed':True}))
