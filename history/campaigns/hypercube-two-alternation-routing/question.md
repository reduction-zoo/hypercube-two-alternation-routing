---
status: admitted
openness: supported-within-search-coverage
difficulty: moderate
importance: moderate
tags: [Karp-reduction, routing, hypercube, domination]
last-literature-check: 2026-09-16
---

# Two-alternation reconfigurable routing on hypercubes

## Fixed question

Construct a deterministic polynomial-time Karp reduction from Partial Domination
on explicitly represented hypercubes to one-switch reconfigurable routing on a
hypercube, with one port per vertex, static link cost 1, dynamic link cost 1/2,
and at most two alternations of link medium on each route. Implement polynomial
recovery of a dominating set from every feasible target matching. A complete
proof, executable maps, independent decision tests, native independent review,
and a Typst manuscript are required. A failed construction is not a disproof.

Source: dimension d >= 1, a binary activity array of length 2^d defining T,
and integer k >= 0. Decide whether some X subset T, |X| <= k, dominates the
induced cube graph on T. Malformed encodings are NO. Target: dimension ell >= 1,
positive integer weighted ordered demands between distinct bit-labeled vertices,
and nonnegative integer K denoting twice the permitted total cost. The cube is
encoded by its dimension, written in unary (a string of ell ones). A witness is
any partial matching on its vertices with two-alternation shortest-route workload
at most K/2. All vertices have one switch port; matching edges have cost 1/2.
Zero demands need not be encoded. Routes have no capacity or congestion constraint.
The forward output can be expanded into an explicit cube in polynomial time
in the source size: the proposed ell = 9d+12 gives 2^ell = 4096(2^d)^9 vertices.
Thus the intended hardness also applies to the usual explicit-network model.
Recovery must work for arbitrary feasible, possibly nonoptimal matchings.

## Primary results and openness

Kutner and Stewart, *Reconfigurable routing in data center networks*,
[TCS 1038 (2025), 115154](https://doi.org/10.1016/j.tcs.2025.115154),
[full arXiv preprint](https://arxiv.org/abs/2401.13359): Section 2 defines the
model; Theorem 7 (p.29) proves the source NP-complete, including a polynomial-size
coordinate embedding. Theorem 4 proves hardness at three alternations. Theorem 8
and Corollary 5 prove hardness with at most one dynamic edge. The end of Section
3.1 and Section 4 (pp.35–36) explicitly leave two alternations open. One dynamic
edge implies at most two alternations, but the latter admits dynamic–static–dynamic
paths and is a different target language. A sentence introducing Section 3.1 uses
sigma where the formal result uses delta; the formal statement and conclusion
control this reading.

Kutner's [thesis](https://etheses.dur.ac.uk/16219/1/Eventful_Graphs_DCK_thesis_version_for_etheses.pdf),
Corollary 4.20 and Section 4.4 (printed p.158), retain the same open question.
The [coauthor's publication list](https://iastewart.webspace.durham.ac.uk/publications/)
identifies the 2025 journal article. Its publisher page returned 403, so the full
argument was read in the arXiv version and compared with the thesis, not falsely
attributed to an inspected publisher PDF.

Actual Web/arXiv searches, 2026-09-16: `"Reconfigurable routing in data center networks" arxiv`,
`"Reconfigurable routing" "Theorem 8"`, `"reconfigurable routing" "sigma" "2" 2026 hardness`,
`"1-switched" "2" "hypercubes"`, `"2401.13359" "2026"`,
`"reconfigurable routing" "two alternations"`, `"Kutner" "Stewart" "routing" 2026`,
and `"hypercubes" "routing" "σ = 2"`. No superseding result was found. This is
bounded coverage, not a guarantee against overlooked or unpublished work.

## Mechanism and executed screening

Place the original cube far from a destination o. Leave k free matching slots on
a radius-d sphere around o, and occupy all other nearby vertices with weighted
forced matching demands. Force o to a remote partner s. Crucially, also occupy
the radius-d ball around s: this blocks cheap dynamic–static–dynamic shortcuts.
A tight workload budget should then force all k slots to select source vertices,
with every other source target adjacent to one selected vertex.

The [probe](../../research/evidence/two-alternation-routing-probe.py) and its
[actual output](../../research/evidence/two-alternation-routing-probe.json) cover all nonempty
T in dimensions 1 and 2 and all k in 1..|T|: 36 sources, 70 canonical matchings,
192 low-demand distance checks, 54 feasible matchings, 291–5105 forced edges.
The unguarded variant of this proposed construction admits a false positive for
T={00,11}, k=1. This is not a counterexample to the published delta=1 theorem.
The guarded finite checks pass but do not quantify over arbitrary matchings.
The first campaign obligation is an independent exact solver that does so.

## Assessments and admission

Difficulty: **moderate**, because the main unresolved obligation is a universal
short-route classification and its tight-budget consequence, supported by a
specific guard mechanism. Solver scale and encoding size need explicit treatment.
Importance: **moderate**, resolving a named routing boundary on a standard network
family. This would not settle the one-alternation case or provide a practical
routing algorithm.

| Gate | Decision | Evidence |
|---|---|---|
| Precise endpoints | pass | Source, target, every-witness recovery, unary cube encoding and explicit expansion fixed above |
| Known results | pass | One dynamic edge and two alternations have distinct feasible routes |
| Supported openness | pass | Explicit open question, thesis confirmation, dated update searches |
| Significance | pass | New hardness boundary on hypercubes |
| Proof route | pass | Occupied ball at the destination's forced partner blocks the additional path shape |
| Executed investigation | pass | Exact finite distances and an unguarded counterexample; general correctness unreviewed |

Campaign allocation: 20 rounds under the latest user instruction. Stop early if
complete or if no supported next hypothesis remains; do not manufacture rounds.
