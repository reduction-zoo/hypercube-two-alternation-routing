"""Independent finite route enumeration and Boolean matching checks."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import z3

sys.set_int_max_str_digits(0)


def call(path, value, extract=False):
    p = subprocess.run([sys.executable, str(path)] + (['--extract'] if extract else []),
                       input=json.dumps(value), text=True, capture_output=True, check=True)
    return json.loads(p.stdout)


def ball(c, r, dim):
    for j in range(min(r, dim)+1):
        for bits in combinations(range(dim), j):
            yield c ^ sum(1 << i for i in bits)


def cost(u, v, matching):
    mate = {a: b for x, y in matching for a, b in ((x, y), (y, x))}
    value = 2*(u ^ v).bit_count()
    for a, b in mate.items():
        value = min(value, 1+2*((u ^ a).bit_count()+(b ^ v).bit_count()))
    if u in mate and v in mate:
        value = min(value, 2+2*(mate[u] ^ mate[v]).bit_count())
    return value


def solve(target):
    dim, demands, bound = len(target['cube']), target['demands'], target['bound']
    baseline = sum(w for _, _, w in demands)
    if baseline > bound:
        return None, 0
    forced = {}
    for u, v, w in demands:
        if baseline+w*(min(2*(u ^ v).bit_count(), 3)-1) > bound:
            for a, b in ((u, v), (v, u)):
                if a in forced and forced[a] != b:
                    return None, 0
                forced[a] = b
    fixed = {tuple(sorted((u, v))) for u, v in forced.items()}
    low = [(u, v, w) for u, v, w in demands if forced.get(u) != v]
    residual = bound-sum(w for u, v, w in demands if forced.get(u) == v)
    if not low:
        return sorted(fixed), 0
    queries = 0
    # Exact routes up to cutoff, with an optimistic unconstrained overflow option.
    # UNSAT excludes all routes; a model without overflow supplies an exact witness.
    for cutoff in range(1, residual+1):
        solver = z3.Solver()
        edge_vars = {}
        def available(edges):
            literals = []
            vertices = {}
            for a, b in edges:
                if a == b:
                    return z3.BoolVal(False)
                for x, y in ((a, b), (b, a)):
                    if (x in forced and forced[x] != y) or (x in vertices and vertices[x] != y):
                        return z3.BoolVal(False)
                    vertices[x] = y
                edge = tuple(sorted((a, b)))
                if edge not in fixed:
                    if edge not in edge_vars:
                        edge_vars[edge] = z3.Bool(f'edge_{a}_{b}')
                    literals.append(edge_vars[edge])
            return z3.And(literals)
        records = []
        total = []
        for index, (u, v, weight) in enumerate(low):
            length = z3.Int(f'length_{index}')
            overflow = z3.Bool(f'overflow_{index}')
            options = [z3.And(overflow, length == cutoff+1)]
            known = cost(u, v, fixed)
            if known <= cutoff:
                options.append(z3.And(z3.Not(overflow), length == known))
            radius = (cutoff-1)//2
            for b in ball(v, radius, dim):
                if b in forced:
                    continue
                rem = radius-(b ^ v).bit_count()
                for a in ball(u, rem, dim):
                    if a in forced or a == b:
                        continue
                    value = 1+2*((u ^ a).bit_count()+(v ^ b).bit_count())
                    options.append(z3.And(z3.Not(overflow), length == value, available([(a,b)])))
            radius = (cutoff-2)//2
            if radius >= 0:
                if v in forced:
                    pairs = ((a, forced[v]) for a in ball(forced[v], radius, dim))
                elif u in forced:
                    pairs = ((forced[u], b) for b in ball(forced[u], radius, dim))
                else:
                    pairs = ((a, b) for a in range(1 << dim) for b in ball(a, radius, dim))
                for a, b in pairs:
                    if a == u or b == v:
                        continue
                    if (u in forced and forced[u] != a) or (v in forced and forced[v] != b):
                        continue
                    if (a in forced and forced[a] != u) or (b in forced and forced[b] != v):
                        continue
                    value = 2+2*(a ^ b).bit_count()
                    options.append(z3.And(z3.Not(overflow), length == value, available([(u,a),(v,b)])))
            solver.add(z3.Or(options))
            total.append(weight*length)
            records.append(overflow)
        incident = {}
        for (a, b), variable in edge_vars.items():
            incident.setdefault(a, []).append(variable)
            incident.setdefault(b, []).append(variable)
        for variables in incident.values():
            solver.add(z3.AtMost(*variables, 1))
        solver.add(z3.Sum(total) <= residual)
        result = solver.check()
        queries += 1
        assert result != z3.unknown, solver.reason_unknown()
        if result == z3.unsat:
            return None, queries
        model = solver.model()
        if not any(z3.is_true(model.eval(o)) for o in records):
            matching = sorted(fixed | {e for e, flag in edge_vars.items() if z3.is_true(model.eval(flag))})
            endpoints = [v for e in matching for v in e]
            assert len(endpoints) == len(set(endpoints))
            assert sum(w*cost(u, v, matching) for u, v, w in demands) <= bound
            return matching, queries
    raise AssertionError('Complete bounded route enumeration must decide')


def main(candidate):
    instances = recoveries = queries = 0
    for d in (1, 2):
        for bits in range(1, 1 << (1 << d)):
            active = [(bits >> v) & 1 for v in range(1 << d)]
            targets = [v for v, bit in enumerate(active) if bit]
            for k in range(1, len(targets)+1):
                source = {'dimension': d, 'active': active, 'k': k}
                expected = any(all(any((u ^ v).bit_count() <= 1 for v in X) for u in targets)
                               for X in combinations(targets, k))
                target = call(candidate, source)
                witness, calls = solve(target)
                queries += calls
                assert (witness is not None) == expected, source
                if witness is not None:
                    # Add an unrelated edge if two unused vertices exist.
                    used = {v for edge in witness for v in edge}
                    free = [v for v in range(min(1 << len(target['cube']), 20000)) if v not in used][:2]
                    variants = [witness]
                    if len(free) == 2:
                        variants.append(witness+[tuple(free)])
                    for edges in variants:
                        assert sum(w*cost(u, v, edges) for u, v, w in target['demands']) <= target['bound']
                        recovered = call(candidate, {'source': source, 'target_solution': edges}, True)
                        assert len(set(recovered)) == len(recovered) <= k
                        assert set(recovered) <= set(targets)
                        assert all(any((u ^ v).bit_count() <= 1 for v in recovered) for u in targets)
                        recoveries += 1
                instances += 1
                print(json.dumps({'case': instances, 'source': source, 'yes': expected,
                                  'solver_queries': calls}), flush=True)
    print(json.dumps({'sources': instances, 'recoveries': recoveries, 'solver_queries': queries}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', type=Path, required=True)
    main(parser.parse_args().candidate)
