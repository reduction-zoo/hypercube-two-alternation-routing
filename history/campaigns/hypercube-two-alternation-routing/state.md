# Two-alternation hypercube routing

Status: **ready_for_expert_review**. Allocation: 20 rounds; 1 started and completed,
19 unused because the fixed positive target was reached. One construction route;
solver-formulation and manuscript repairs were not counted as new rounds.

Result: Partial Domination on explicit hypercubes reduces to one-port, one-switch
hypercube routing with static cost 1, dynamic cost 1/2, and at most two medium
alternations. Both maps are deterministic and polynomial, including explicit
network expansion, and recovery works for every feasible target matching.
The result has agent-level review; human expert verification remains outstanding.

- [Paper PDF](work/manuscript.pdf), [Typst source](work/manuscript.typ),
  [complete rule](work/algorithm.py), [proof](work/proof.md).
- [Initial independent advance review](reviews/initial/review.md) and
  [manuscript consistency advance review](reviews/manuscript/review.md).
- [Prepared suite](rounds/001/prepared-checks.jsonl): 9 sources, 10 recoveries.
- [Separate verification](rounds/001/verification.jsonl): 36 sources, 124 solver
  queries, 66 recoveries. [Coverage and commands](work/verification.md).
- [Independent dimension-3 check](reviews/initial/check-output.json): 102374
  forced edges, with recovery after adding a source-to-source matching edge.
- Final PDF: 6 pages, compiled without diagnostics; all six
  `work/evidence/manuscript/final-page-*.png` images inspected.

| Round | Scope | Outcome |
|---|---|---|
| [1](rounds/001/round.md) | Guard the destination partner's ball; one construction and complete maps | General proof, both oracle suites, independent review, inspected manuscript |

The candidate algorithm is unchanged since the passing suites. Reviewer-approved
wording fixes and visual formula/layout corrections are complete. No mathematical
obligation remains acknowledged by the agents. Novelty coverage is bounded; the
full publisher PDF was inaccessible, and detailed comparisons use the full
preprint plus corroborating journal metadata and thesis evidence.

Post-campaign maintenance complete: **1 shared experience entry created, 0 existing
entries updated, 0 pending**. [Forced partner ball](../../research/experience/forced-partner-ball.md)
records the reviewed premises and unguarded counterexample. The board and problem
card are synchronized. Next action for this result: human expert assessment;
no further construction round is justified on the completed candidate.
