"""Independent exact Z3 oracles derived from the two decision definitions."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import z3

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parent


def source_valid(x):
    return (isinstance(x, dict) and set(x) == {'dimension', 'active', 'k'}
            and type(x['dimension']) is int and x['dimension'] >= 1
            and isinstance(x['active'], list) and len(x['active']) > 0
            and len(x['active']).bit_length()-1 == x['dimension']
            and len(x['active']) & (len(x['active'])-1) == 0
            and all(type(v) is int and v in (0, 1) for v in x['active'])
            and type(x['k']) is int and x['k'] >= 0)


def source_witness(x, selected):
    if not source_valid(x) or not isinstance(selected, list):
        return False
    if any(type(v) is not int for v in selected):
        return False
    targets = {i for i, bit in enumerate(x['active']) if bit}
    return (len(selected) == len(set(selected)) and len(selected) <= x['k']
            and set(selected) <= targets
            and all(any((u ^ v).bit_count() <= 1 for v in selected) for u in targets))


def source_solve(x):
    if not source_valid(x):
        return None
    targets = [i for i, bit in enumerate(x['active']) if bit]
    choose = {v: z3.Bool(f'choose_{v}') for v in targets}
    solver = z3.Solver()
    solver.add(z3.Sum([z3.If(choose[v], 1, 0) for v in targets]) <= x['k'])
    for u in targets:
        solver.add(z3.Or([choose[v] for v in targets if (u ^ v).bit_count() <= 1]))
    result = solver.check()
    assert result != z3.unknown, solver.reason_unknown()
    if result == z3.unsat:
        return None
    witness = [v for v in targets if z3.is_true(solver.model().eval(choose[v]))]
    assert source_witness(x, witness)
    return witness


def target_valid(x):
    if not isinstance(x, dict) or set(x) != {'cube', 'demands', 'bound'}:
        return False
    if not isinstance(x['cube'], str) or not x['cube'] or set(x['cube']) != {'1'}:
        return False
    if type(x['bound']) is not int or x['bound'] < 0 or not isinstance(x['demands'], list):
        return False
    limit = 1 << len(x['cube'])
    return all(isinstance(e, list) and len(e) == 3
               and all(type(v) is int for v in e)
               and 0 <= e[0] < limit and 0 <= e[1] < limit and e[0] != e[1]
               and e[2] > 0 for e in x['demands'])


def distance(u, v, edges):
    result = 2 * (u ^ v).bit_count()
    mate = dict(edges + [(b, a) for a, b in edges])
    for a, b in edges:
        result = min(result, 1 + 2*((u ^ a).bit_count() + (b ^ v).bit_count()),
                     1 + 2*((u ^ b).bit_count() + (a ^ v).bit_count()))
    if u in mate and v in mate:
        result = min(result, 2 + 2*(mate[u] ^ mate[v]).bit_count())
    return result


def target_witness(x, edges):
    if not target_valid(x) or not isinstance(edges, list):
        return False
    seen = set()
    for e in edges:
        if not isinstance(e, (tuple, list)) or len(e) != 2:
            return False
        if any(type(v) is not int or not 0 <= v < 1 << len(x['cube']) for v in e):
            return False
        if e[0] == e[1] or seen.intersection(e):
            return False
        seen.update(e)
    edges = [tuple(e) for e in edges]
    return sum(w * distance(u, v, edges) for u, v, w in x['demands']) <= x['bound']


def target_solve(x):
    assert target_valid(x), x
    dim = len(x['cube'])
    baseline = sum(w for _, _, w in x['demands'])
    if baseline > x['bound']:
        return None
    forced = {}
    for u, v, w in x['demands']:
        gap = min(2*(u ^ v).bit_count(), 3)-1
        if baseline + gap*w > x['bound']:
            if (u in forced and forced[u] != v) or (v in forced and forced[v] != u):
                return None
            forced[u] = v
            forced[v] = u
    solver = z3.Solver()
    mate = z3.Function('mate', z3.BitVecSort(dim), z3.BitVecSort(dim))
    for u, v in forced.items():
        solver.add(mate(z3.BitVecVal(u, dim)) == v)

    def hamming(a, b):
        bits = a ^ b
        return z3.Sum([z3.If(z3.Extract(i, i, bits) == 1, 1, 0) for i in range(dim)])

    def free_shell(center):
        for radius in range(dim+1):
            shell = [center ^ sum(1 << j for j in bits)
                     for bits in combinations(range(dim), radius)]
            free = [v for v in shell if v not in forced]
            if free:
                return radius, free
        return dim+1, []

    terms, records = [], []
    for i, (u, v, w) in enumerate(x['demands']):
        if forced.get(u) == v:
            terms.append(w)
            continue
        a, b = z3.BitVecs(f'a_{i} b_{i}', dim)
        kind, cost = z3.Ints(f'kind_{i} cost_{i}')
        U, V = z3.BitVecVal(u, dim), z3.BitVecVal(v, dim)
        fixed_edges = [(a, b) for a, b in forced.items() if a < b]
        known_cost = distance(u, v, fixed_edges)
        ru, free_u = free_shell(u)
        rv, free_v = free_shell(v)
        # Any useful new edge has free endpoints; known edges are covered by kind 0.
        free_constraints = []
        for vertex, center, radius, nearest in ((a, U, ru, free_u), (b, V, rv, free_v)):
            center_value = center.as_long()
            next_free = [center_value ^ sum(1 << j for j in bits)
                         for bits in combinations(range(dim), radius+1)
                         if center_value ^ sum(1 << j for j in bits) not in forced]
            free_constraints.append(z3.Implies(hamming(vertex, center) == radius+1,
                                               z3.Or([vertex == x for x in next_free])))
            free_constraints += [hamming(vertex, center) >= radius,
                                 z3.Implies(hamming(vertex, center) == radius,
                                            z3.Or([vertex == x for x in nearest]))]
        two_constraints = []
        if u in forced:
            two_constraints.append(a == forced[u])
        if v in forced:
            two_constraints.append(b == forced[v])
        if u not in forced and v in forced:
            radius, _ = free_shell(forced[v])
            two_constraints.append(hamming(a, b) >= radius)
        if v not in forced and u in forced:
            radius, _ = free_shell(forced[u])
            two_constraints.append(hamming(a, b) >= radius)
        solver.add(z3.Or(
            z3.And(kind == 0, cost == known_cost),
            z3.And(kind == 1, *free_constraints, a != b, mate(a) == b, mate(b) == a,
                   cost == 1 + 2*(hamming(U, a) + hamming(b, V))),
            z3.And(kind == 2, *two_constraints, a != U, b != V, mate(U) == a, mate(a) == U,
                   mate(V) == b, mate(b) == V, cost == 2 + 2*hamming(a, b))))
        terms.append(w*cost)
        records.append((u, v, a, b, kind))
    solver.add(z3.Sum(terms) <= x['bound'])
    result = solver.check()
    assert result != z3.unknown, solver.reason_unknown()
    if result == z3.unsat:
        return None
    model = solver.model()
    edges = {tuple(sorted((u, v))) for u, v in forced.items()}
    for u, v, a, b, kind in records:
        route = model.eval(kind).as_long()
        if route:
            A, B = model.eval(a).as_long(), model.eval(b).as_long()
            additions = [(A, B)] if route == 1 else [(u, A), (v, B)]
            edges.update(tuple(sorted(e)) for e in additions)
    witness = [list(e) for e in sorted(edges)]
    assert target_witness(x, witness), (x, witness)
    return witness


def matchings(vertices):
    if not vertices:
        yield []
        return
    u, *rest = vertices
    yield from matchings(rest)
    for v in rest:
        for tail in matchings([w for w in rest if w != v]):
            yield [(u, v)] + tail


def invoke(candidate, value, extract=False):
    result = subprocess.run([sys.executable, str(candidate)] + (['--extract'] if extract else []),
                            input=json.dumps(value), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def self_test():
    count = 0
    for dim in (1, 2):
        for bound in range(9):
            demands = [[0, (1 << dim)-1, 2], [1, 0, 1]]
            target = {'cube': '1'*dim, 'demands': demands, 'bound': bound}
            expected = any(target_witness(target, m) for m in matchings(list(range(1 << dim))))
            assert (target_solve(target) is not None) == expected
            count += 1
    assert not target_valid({'cube': '10', 'demands': [], 'bound': 0})
    toy = {'cube': '11', 'demands': [[0, 3, 1]], 'bound': 1}
    assert target_witness(toy, [[0, 3]])
    assert not target_witness(toy, [[0, 3], [0, 2]])
    assert not target_witness(toy, [])
    cases = json.loads((ROOT/'cases.json').read_text())
    for case in cases:
        assert (source_solve(case['source']) is not None) == case['yes']
    assert not source_witness({'dimension': 2, 'active': [1, 0, 0, 1], 'k': 1}, [0])
    print(json.dumps({'z3': z3.get_version_string(), 'target_exhaustive_crosschecks': count,
                      'source_cases': len(cases), 'malformed_target_and_wrong_witnesses_rejected': True}))


def run(candidate):
    count = recoveries = 0
    for case in json.loads((ROOT/'cases.json').read_text()):
        source = case['source']
        target = invoke(candidate, source)
        assert target_valid(target)
        witness = target_solve(target)
        assert (witness is not None) == (source_solve(source) is not None), (source, target)
        if witness is not None:
            for edges in (witness, [e[::-1] for e in witness[::-1]]):
                recovered = invoke(candidate, {'source': source, 'target_solution': edges}, True)
                assert source_witness(source, recovered), (source, recovered)
                recoveries += 1
        count += 1
        print(json.dumps({'case': count, 'source': source, 'yes': witness is not None,
                          'demands': len(target['demands']), 'recoveries_so_far': recoveries}), flush=True)
    print(json.dumps({'passed_sources': count, 'recoveries': recoveries}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--candidate', type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        run(args.candidate)
