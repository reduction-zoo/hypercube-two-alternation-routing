"""Partial hypercube domination to two-alternation reconfigurable routing."""
from itertools import combinations
import json
import sys

sys.set_int_max_str_digits(0)


def valid(x):
    return (isinstance(x, dict) and set(x) == {'dimension', 'active', 'k'}
            and type(x['dimension']) is int and x['dimension'] >= 1
            and isinstance(x['active'], list) and len(x['active']) > 0
            and len(x['active']).bit_length()-1 == x['dimension']
            and len(x['active']) & (len(x['active'])-1) == 0
            and all(type(v) is int and v in (0, 1) for v in x['active'])
            and type(x['k']) is int and x['k'] >= 0)


def ball(center, radius, dimension):
    return {center ^ sum(1 << i for i in bits)
            for size in range(radius+1) for bits in combinations(range(dimension), size)}


def geometry(d, k):
    block = 2*d+3
    dim = 4*block+d
    o, s, g, h = [((1 << block)-1) << (d+i*block) for i in range(4)]
    slots = sorted(ball(o, d, dim)-ball(o, d-1, dim))[:k]
    return dim, o, s, g, h, slots


def forward(x):
    no = {'cube': '1', 'demands': [[0, 1, 1]], 'bound': 0}
    yes = {'cube': '1', 'demands': [], 'bound': 0}
    if not valid(x):
        return no
    targets = {i for i, bit in enumerate(x['active']) if bit}
    if not targets or x['k'] >= len(targets):
        return yes
    if x['k'] == 0:
        return no
    d, k = x['dimension'], x['k']
    dim, o, s, g, h, slots = geometry(d, k)
    moon = range(1 << d)
    near = set(moon) | {v ^ (1 << i) for v in moon for i in range(dim)}
    occupied = (near | ball(o, d+1, dim))-targets-set(slots)
    edges = [(v, v ^ h) for v in sorted(occupied-{o})] + [(o, s)]
    edges += [(v, v ^ g) for v in sorted(ball(s, d, dim)-{s})]
    weight = len(targets)*(d+2)+1
    demands = [[u, v, weight] for u, v in edges] + [[t, o, 1] for t in sorted(targets)]
    return {'cube': '1'*dim, 'demands': demands,
            'bound': weight*len(edges)+len(targets)*(2*d+3)-2*k}


def extract(source, edges):
    if not valid(source):
        raise ValueError('Recovery requires a valid source and feasible target witness')
    targets = {i for i, bit in enumerate(source['active']) if bit}
    if not targets or source['k'] >= len(targets):
        return sorted(targets)
    if source['k'] == 0:
        raise ValueError('A nonempty zero-budget source has no feasible target witness')
    slots = set(geometry(source['dimension'], source['k'])[-1])
    return sorted({u for a, b in edges for u, v in ((a, b), (b, a))
                   if u in targets and v in slots})


if __name__ == '__main__':
    if sys.argv[1:] == ['--extract']:
        request = json.load(sys.stdin)
        result = extract(request['source'], request['target_solution'])
    elif not sys.argv[1:]:
        try:
            source = json.load(sys.stdin)
        except json.JSONDecodeError:
            source = None
        result = forward(source)
    else:
        raise ValueError('Expected no arguments or --extract')
    print(json.dumps(result))
