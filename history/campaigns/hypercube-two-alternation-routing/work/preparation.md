# Testing foundation

Prepared before the executable candidate. The independent source oracle is Z3
Boolean dominating-set feasibility. The target oracle uses bit vectors for cube
vertices and an uninterpreted mate function. Selected dynamic edges impose both
mate(a)=b and mate(b)=a with a!=b. This enforces matching consistency among all
selected edges without enumerating the exponentially represented cube.

A route is either all-static, static–dynamic–static (possibly empty static
segments), or dynamic–static–dynamic. Their doubled lengths are respectively
2h(u,v), 1+2h(u,a)+2h(b,v), and 2+2h(a,b), with appropriate endpoint matching
constraints. A simple route with <=2 alternations has one of these shapes,
since distinct dynamic edges cannot be consecutive in a matching. Conversely
these expressions specify walks; deleting a cycle never increases cost or the
number of alternations. Thus existence of these walks has exactly the same
threshold meaning. A model's actual matching is checked separately by evaluating
the minimum over every matching edge and the two endpoint mates.

Generic preprocessing forces a demand edge only when its absence alone is
impossible: every distinct-endpoint demand has cost >=1 in doubled units.
Without the direct dynamic edge its cost is >=min(2h(u,v),3). If the sum of
baseline weighted costs plus this demand's weighted gap exceeds the budget,
the edge is mandatory. Conflicting mandatory edges imply NO. This rule uses
only the target definition, not source vertices, slots, guard balls, or the
candidate's characterization. Z3 still ranges over arbitrary matchings.
SAT models are validated exactly; UNSAT is NO; unknown is an explicit failure.
There are no solver timeouts or heuristic approximations.

`python3 work/check.py --self-test` (from campaign root) passed 18 target
comparisons with exhaustive partial-matching enumeration on Q1 and Q2,
9 hand-classified source cases, and malformed-target/invalid-witness checks.
See [actual output](evidence/preparation/self-test.json) for the solver version.
Coverage is deliberately finite. Crosschecking formulas on small cubes does
not prove the reduction. Actual large-output decision checks follow construction.

The initial mixed integer/bit-vector encoding was manually interrupted during
an unresolved solver call, three times while refining its symbolic formulation.
None of these calls is recorded as UNSAT. Snapshots under rounds/001 preserve
the earlier checkers, and prepared-checks-interrupted.jsonl records completed
cases before interruption. These are oracle implementation repairs in round 1,
not new construction attempts or imposed campaign timeouts.

The current solver uses QF_UFBV throughout: route lengths and weighted totals
have width one bit beyond the bit length of max(K,(4*ell+2)*sum(weights))+1.
Every selected route expression is at most 4*ell+1, so every intermediate length
and weighted sum is below the signed-positive range. Arithmetic cannot wrap.
Generic nearest-free-vertex shells provide redundant route restrictions. A
route using a forced edge can be replaced by the best route in the forced
matching, so the variable one-edge route may use free endpoints only. Its
endpoint distance is at least the nearest free shell; at that distance and
the next distance the endpoint must belong to the enumerated free shell.
The constraints need not exclude more distant forced vertices: allowing them
only adds already legal routes. If a two-edge route begins at a free vertex,
its partner must also be free; this gives the corresponding nearest-free lower
bound when the other route endpoint is already forced. These facts are generic
matching facts, independent of source labels and the guard construction.

The revised self-tests and deliberately incorrect subprocess fixtures passed:
[self-tests](evidence/preparation/self-test-bitvector.json),
[negative fixtures and independent enumerator crosschecks](evidence/preparation/negative-and-enumerator-checks.json).
The actual-output prepared suite now passes 9 sources and 10 recovery calls;
see [raw results](../rounds/001/prepared-checks.jsonl).
