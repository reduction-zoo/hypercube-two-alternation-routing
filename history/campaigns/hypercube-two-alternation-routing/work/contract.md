# JSON contract

Source: exactly `dimension`, `active`, `k`. Dimension is an integer >=1,
active is a list of exactly 2^dimension integers in {0,1}, k is a nonnegative
integer. Booleans are not integers here. Malformed source objects and malformed
JSON are outside the source language and map to the fixed NO target. Source
witness: a duplicate-free list of active vertex indices, length <=k, dominating
all active vertices by Hamming distance <=1.

Target: exactly `cube`, `demands`, `bound`. Cube is a nonempty unary dimension
string consisting of ones. Each demand is [u,v,w], distinct legal vertex indices
and positive integer weight. Bound is a nonnegative integer in doubled cost
units: static edges cost 2 and matching edges cost 1. Repeated demand pairs are
allowed and their weights contribute separately. Target witness: a list of
pairwise vertex-disjoint unordered pairs of distinct legal vertex indices.
Its weighted sum of shortest route costs with <=2 medium alternations must
not exceed bound. Empty matching and unused vertices are permitted.

`python3 algorithm.py` reads a source JSON value and writes the target JSON.
`python3 algorithm.py --extract` reads {source: ..., target_solution: ...} and
writes a source witness. Recovery guarantees apply only to valid target witnesses
of the constructed target. Infeasible recovery witnesses have no correctness guarantee;
malformed JSON raises an explicit parser error in recovery mode.
Both maps work in fresh processes. No solvers are used by either map.

Fixed YES: Q1, empty demands, bound 0. Fixed NO: Q1, demand [0,1,1], bound 0.
An empty source active set returns YES and recovers []; k=0 with a nonempty set
returns NO. For k>=|T| the forward map may return YES and recovery returns T.
