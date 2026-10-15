# Independent review

Decision: **advance**. Date: 2026-09-16.

The complete forward map and recovery meet the fixed mathematical question. The
proof supports correctness for all source dimensions and every feasible target
matching, and the construction contributes a new boundary relative to the primary
results inspected. This is eligibility for manuscript preparation and expert
review, not human verification or publication acceptance. There is one minor
bit-complexity wording correction below; it does not change the stated final bound.

## Scope and independence

Read README.md, AGENTS.md, research-review/SKILL.md, the fixed question, contract,
algorithm, proof, preparation, verification, and round record. I did not import
the candidate or either existing checker. The round reports no applicable shared
experience entry; none is used as a proof premise. I reused the recorded passing
9-source/10-recovery prepared suite and the 36-source/66-recovery/124-query second
suite, and inspected their raw logs and negative-fixture evidence. I did not
repeat either full suite.

My `check.py` invokes the candidate as fresh subprocesses and independently
constructs Hamming balls by breadth-first shells. It checks a new dimension-3
instance, exact forced-demand endpoints, matching disjointness, guard occupancy,
canonical cost, and recovery from an extended matching with reordered and reversed
edges. `check-output.json` records 102374 forced edges, doubled cost 4197398 equal
to the bound, and recovered dominating set [0,3,5,6]. The extra edge [1,2] is
between unselected source vertices, so this also exercises an arbitrary free
source-to-source edge, not merely unused remote vertices. These are finite checks,
not the basis of the universal proof.

A separately raised parser concern was checked with 2000 nested arrays containing
zero. On the actual Python 3.14.7 runtime, this valid JSON outside the source
schema returns the fixed NO instance with exit code zero; see
`deep-json-output.json`. It is not a reproduced defect. This observation does not
assert behavior of other Python versions.

## Correctness

The route formula is exact. With one port, two distinct dynamic edges cannot be
consecutive on a simple path. At most two alternations therefore permits only
S, SDS, and DSD, allowing empty static segments. The formula minimizes over their
possible matching endpoints and Hamming geodesics. A constructed walk can be
shortened to a path: removing a cycle deletes a substring of the binary medium
word and cannot increase its transitions. Reusing the same dynamic edge does
not invalidate the formula because such walks are removable or dominated.

The six region centers are separated by at least 2d+3, whereas the sum of any
two radii is at most 2d+2. The regions are disjoint. The exclusions of o and s
avoid conflict with {o,s}; translations are injective. Thus the mandatory
matching actually exists and is disjoint from source vertices and slots. All
vertices in the partner ball B(s,d) have mates outside T. This last property,
not simply distance between the source and destination, is the crucial premise.

For completeness, a dominating set may be padded within T to exactly k because
1<=k<|T|. Its bijection to the slots coexists with all forced edges. Selected
vertices cost d+1/2 and every other demand costs at most d+3/2, giving the exact
advertised budget. Trivial YES and NO cases and their recovery behavior agree
with the contract.

For soundness, every distinct-endpoint demand costs at least 1/2. Removing a
forced direct edge raises its minimum cost to at least 3/2; the endpoints are
not adjacent. Its added weighted cost alpha exceeds the entire low-demand
allowance. This reasoning needs no optimality assumption and forces all edges
simultaneously in every feasible matching.

For a low demand with cost at most d+3/2, a one-dynamic route must arrive from
B(o,d+1). A forced vertex there has its mate too far from the source. Hence the
arrival endpoint is a slot, at distance d from o, and the departure endpoint is
within distance one of the source. In a two-dynamic route the final edge is
{s,o}. The first mate cannot belong to B(s,d), since every vertex of that ball
is already matched outside T. Therefore its cost is at least d+2. All-static
routes are also too expensive. These inequalities hold for arbitrary extra
matching edges and arbitrary source labels.

The sum bound is tight: if a source vertices are matched to slots, low demands
cost at least |T|(d+3/2)-a, with a<=k. Feasibility implies a=k. Every other demand
must achieve d+3/2. Since all k slots are then occupied by source vertices, the
one-dynamic route classification yields adjacency to a selected source vertex.
There is no unstated assumption that an arbitrary slot mate initially belongs
to T. Recovery precisely selects the source-to-slot pairs, handles both edge
orientations, and returns a dominating set of size k. Additional matching edges
cannot change this implication. Source NO instances therefore have no feasible
target matching.

Both maps are deterministic, use no optimization oracle, and agree with their
mathematical descriptions. The malformed-dimension length check avoids expanding
an integer-specified cube before verifying the explicit activity array. Large
binary/decimal budgets are compared before any size-dependent construction.

## Encoding and membership in NP

With N=2^d, the explicit target has V=4096N^9 vertices. The fixed number of ball
enumerations, O(V) demands, O(log N)-bit labels and weights, and the explicit
O(V log N)-edge cube all have polynomial encodings. A dense matrix is also
polynomial. Thus the theorem does not derive hardness from a succinct-network
encoding alone. Parsing an arbitrarily long k is separately input-polynomial.
Recovery takes polynomial time in source and witness length, even when presented
with far more matching edges than needed.

The compact target is in NP: retain the at most two matching edges on a chosen
route for each demand. Their union is a partial matching of polynomial size and
preserves those routes. The explicit distance formula checks its workload with
integer arithmetic of polynomial bit length. The source-hardness composition is
valid: Kutner–Stewart Theorem 7 uses an explicitly computable induced grid inside
Q_(2d), with d logarithmic in grid side length. Writing all activity bits is
polynomial in that construction; the source language here is not stronger than
the cited source through a hidden representation change.

Minor correction: proof.md line 129 attributes O(ell) bit operations to forming
each label. The implemented sum of up to ell shifted ell-bit integers admits
the direct conservative bound O(ell^2) per label. Replacing that local estimate
with O(ell^2) leaves the stated overall O(V ell^2)=O(N^9 log^2 N) bound unchanged.
This is a presentation correction, not a gap in polynomiality or the theorem.

## Novelty

Primary comparison: Kutner and Stewart, *Reconfigurable routing in data center
networks*, [arXiv:2401.13359](https://arxiv.org/abs/2401.13359), full supplied
preprint text inspected independently at Sections 2 and 3.1, Theorems 6–8,
Corollaries 3 and 5, and Section 4. Theorem 8 gives the closest construction:
weighted occupied regions and k slots encode Partial Domination under a
one-dynamic-edge restriction. Its Corollary 5 does not settle the present target,
because DSD routes are legal here. The explicit open discussion on pp.35–36
identifies precisely that missing case. The candidate correctly credits this
framework; it does not claim to invent the underlying domination/slot budget.

The actual added ingredient is occupying a ball around the forced mate of the
destination, with separated translated partners. This blocks the new DSD shape
while retaining polynomial cube size and the tight domination argument. It is
not a direct corollary of hardness for three alternations (Theorem 4), since
removing allowed routes can destroy YES instances, or of hardness with one
dynamic edge, since adding allowed routes can destroy NO instances.

I also inspected Foerster, Pacut and Schmid, [*On the Complexity of Non-Segregated
Routing in Reconfigurable Data Center Architectures*](https://schmiste.github.io/ccr19danr.pdf),
2019, Table 1 and Section 2. Their classifications concern general weighted
static networks and do not establish the uniform-cost hypercube restriction.

Independent web queries on 2026-09-16 included `"reconfigurable routing" "two
alternations"`, `hypercube reconfigurable routing two alternations hardness Kutner
Stewart 2026`, `"reconfigurable routing" "guard" matching`, `"reconfigurable
routing" "σ = 2"`, `"reconfigurable routing" "two dynamic" hypercube`, and
`"reconfigurable routing" "alternations" 2025 2026`. No superseding result was
identified. Journal search-index text at
[ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0304397525000921)
also distinguishes Theorems 4 and 8 in Section 3/Table 1 and labels the single-dynamic-edge discussion Section 3.1. The final article is Theoretical Computer Science 1038, 115154, dated 22 May 2025, DOI 10.1016/j.tcs.2025.115154. These journal locations are confirmed only in indexed text; the Theorem 7 and Corollary 5 citations above use preprint numbering. The repository exposes a
[final journal PDF URL](https://durham-repository.worktribe.com/OutputFile/3708453),
but direct opens of it and the publisher page returned 403. Accordingly I do
not claim a full final-PDF comparison. Search-index results and the thesis are
corroborative; the complete proof comparison is to the inspected preprint.

Novelty is supported relative to these checked primary results and equivalent
route restrictions. Unindexed, unpublished, or missed work remains possible;
negative search results alone are not proof of novelty. Human expert review
should assess this explicit extension against the broader literature.

## Significance and next action

The contribution meets the fixed moderate significance criterion: it establishes
NP-completeness at two alternations on hypercubes, with a fixed link-cost ratio,
one port per vertex, and recovery from every feasible witness. This closes a
specifically stated boundary of the closest work through an additional geometric
guard. It does not resolve one alternation, provide a practical algorithm, or
make a broad new claim about all graph classes or all cost ratios. The large
polynomial expansion is acceptable for this complexity result but limits
practical interpretation.

Proceed to the required manuscript and rendering checks, carrying the local
bit-cost wording correction and literature limitations into the write-up.
