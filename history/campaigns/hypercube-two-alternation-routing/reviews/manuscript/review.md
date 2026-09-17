# Focused manuscript consistency review

Decision: **advance; no substantive deviation from the reviewed theorem**.
Date: 2026-09-16.

Read work/manuscript.typ against the previously reviewed construction, proof,
contract and evidence. This review covers mathematical consistency and
qualifications. The main session owns all-page visual QA. No algorithm suites
were rerun, and no candidate, test, or manuscript files were modified.

Theorem 1 retains the same endpoints, fixed costs, one-port matching restriction,
two-alternation budget, explicit-network claim and every-feasible-witness recovery.
Equations for route costs, dimensions, occupied sets, forced edges, demand weight,
workload threshold and recovery agree with the reviewed proof. Renaming |T| to n
and the explicit source-cube size to N is consistent. Lemmas 2–4 preserve the
region-separation, forced-edge and partner-ball arguments. The tight workload
argument correctly forces every slot to be matched to a source vertex before
inferring adjacency for remaining demands. NP membership and explicit expansion
remain valid; the local label-construction estimate now correctly uses the
conservative O(ell^2) bit bound.

One local exposition correction is recommended in Lemma 4: replace “A
one-dynamic route has cost D(u,a)+1/2+D(v,o)” with “A one-dynamic route has cost
at least D(u,a)+1/2+D(v,o), with equality when the static portions are geodesics.”
The lemma quantifies over every short route, and a non-geodesic static portion
can make its cost strictly larger. The inequality is exactly what the subsequent
inference needs; this wording issue does not change the proof or result. The
same convention appears in the original proof's route discussion.

The figure caption correctly calls the drawing schematic, marks slot-to-o
segments as length-r paths, and distinguishes the omitted edges and nonmetric
placement. Its selected Q2 vertices {00,11} do dominate Q2. The partner-ball
caption states the precise matching obstruction used in the proof.

The introduction and conclusion appropriately credit the existing domination
and slot framework. The reference explicitly restricts detailed theorem numbers
to the full preprint; the appendix preserves the final-journal access limitation
and bounded novelty-search coverage. Claims about one alternation, practical
routing utility, unpublished work, and expert assessment are suitably limited.

The appendix faithfully reports the recorded 9-source/10-recovery prepared
suite, 36-source/66-recovery/124-query second suite, and separate dimension-3
reviewer check with 102374 forced edges. It separates finite testing from the
general proof and describes the optimistic-overflow oracle without asserting a
polynomial target-solving algorithm.

No new mathematical review or algorithm rerun is required for the suggested
local inequality wording correction. Complete the main session's visual QA.
