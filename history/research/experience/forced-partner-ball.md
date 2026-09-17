# Occupy the destination partner's ball to block two-dynamic-edge shortcuts

Tags: Karp-reduction, hypercube, routing, matching, shortcut, guard-ball.

## Claim and applicability

In the one-port hypercube routing model, dynamic links form a partial matching.
Suppose every feasible configuration contains the pair {o,s}. Let T be the source
vertices, and suppose every vertex of B(s,r) is forced to a mate outside T.
Then any dynamic–static–dynamic route from a vertex of T to o has cost at least
r+2 when static links cost 1 and dynamic links cost 1/2. Its first mate cannot
lie in B(s,r), and its final dynamic edge must be {s,o}. Thus this route shape
cannot meet a threshold r+3/2 used to encode adjacency to selected source vertices.

Occupancy alone is insufficient: all occupied vertices in the partner ball must
have mates outside T. A complete reduction must separately force these pairs,
prove that their endpoints are disjoint, exclude short one-dynamic routes through
those pairs, and bound their size. This lemma does not assert that such guards
can always be constructed. Multiple ports or additional alternations invalidate
the stated path-shape argument.

## Evidence and status

Evidence type: general lemma plus counterexample to an unguarded local variant.
Agent review status: independently advanced; human expert assessment pending.

The [originating round](../../campaigns/hypercube-two-alternation-routing/rounds/001/round.md)
uses four separated coordinate blocks and translated endpoint pairs to realize
this condition. Its [proof](../../campaigns/hypercube-two-alternation-routing/work/proof.md)
and [independent review](../../campaigns/hypercube-two-alternation-routing/reviews/initial/review.md)
cover every feasible matching, not just the tested configurations.
The [screening probe](../evidence/two-alternation-routing-probe.py) and
[output](../evidence/two-alternation-routing-probe.json) exhibit an unguarded false
positive for T={00,11}, k=1. This is a local construction counterexample, not a
refutation of the published one-dynamic-edge hardness result.

The complete rule supplies a Karp map, arbitrary-witness recovery, polynomial
explicit cube expansion, two separately implemented target oracles and a
[Typst paper](../../campaigns/hypercube-two-alternation-routing/work/manuscript.pdf).
The general source-to-slot framework is due to Kutner and Stewart,
[arXiv:2401.13359](https://arxiv.org/abs/2401.13359), Theorem 8; the added partner-ball
condition addresses the extra route shape in their stated two-alternation question.

## Consequence for search

When transferring a reduction from one dynamic edge to two medium alternations,
inspect the destination's forced mate as well as its own neighborhood. A free
vertex close to that mate can create a NO-to-YES shortcut even when destination
slots are correctly forced. A guard at the mate can restore the intended cost
gap without changing the tight slot-counting recovery argument.

## Use history

- 2026-09-16: extracted during post-campaign maintenance from the completed first
  round. The condition was developed in that round, not retrieved beforehand.
  No subsequent independent campaign has used this entry, and no measured
  improvement to discovery efficiency is claimed.
