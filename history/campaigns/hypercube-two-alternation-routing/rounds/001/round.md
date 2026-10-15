# Round 1 — Occupy the partner ball

## Plan

Develop the screened guard-ball construction into a complete Karp rule.
Hypothesis: forcing every vertex within distance d of the destination's forced
partner excludes every cheap two-dynamic-edge route; then the workload threshold
forces exactly k source-to-slot matching edges and domination.
This adds a protection mechanism to the one-dynamic-edge approach, rather than
assuming the more permissive routing language has the same feasible solutions.

Scope: one construction, all prepared sources (9), followed by all nonempty
active subsets in dimensions 1–2 and all budgets 1..|T| if the initial suite passes.
Establish endpoint disjointness, every-route lower bounds, tight-budget recovery,
and polynomial source-size bounds. Preserve the screening unguarded counterexample.
Stop this attempt for a genuine counterexample; routine code or oracle repairs
stay within this round. Independent review follows a complete passing rule.

Experience retrieval: `rg -l 'shortcut|forced matching|routing' research/experience`
returned no entries. The screening probe supplies the applicable counterexample,
not a previously reviewed shared lesson. Finite probes do not justify the general
proof or the arbitrary-matching oracle answer.

## Evidence and diagnosis

Preparation is recorded in [preparation.md](../../work/preparation.md).


Prepared checks now pass 9 source decisions and 10 recovery calls. The mathematical
construction is unchanged. Three manually interrupted mixed-theory solver calls
returned unknown/interrupted and are not counted as NO; saved checker snapshots
record the successive oracle formulations. Exact bit-vector arithmetic, with a
proved sufficient width, resolves the same prepared source suite. The second
independent finite-route Boolean oracle passed the declared 36-case domain with
124 solver queries and 66 recovery calls.
See work/preparation.md for the generic preprocessing justification.

The foundation also tests a strict dynamic–static–dynamic optimum on Q4: forced
edges {0,3} and {15,7}, weights 10, plus unit demand 0->15. Doubled budgets 23 and
24 give NO and YES, respectively; both target programs agree. This ensures the
additional route shape is actually supported by the tests rather than excluded
by the oracle. Transport checks cover seven malformed objects, three malformed
JSON inputs, and a 5001-digit source budget with forward/recovery execution.


The [initial independent review](../../reviews/initial/review.md) advances the
complete rule. Its own dimension-3 check covers 102374 forced edges and recovery
with an extra edge between two unselected source vertices. The
[manuscript review](../../reviews/manuscript/review.md) also advances. Applied its
local inequality wording correction and the initial review's conservative per-label
bit-cost correction; neither changes the construction or final complexity bound.
The final six-page Typst PDF was compiled without diagnostics and every rendered
page inspected. Corrected a Typst case-condition comma that had split a formula,
duplicate reference supplements, and a lemma/proof page break. These were writing
repairs, not additional research rounds. Campaign question links were repaired
for its copied location without changing the statement or acceptance criteria.

Observation: one declared construction reached a complete rule. Both independent
programs decide actual target outputs; finite cases include genuine source NO
instances. The general route classification, rather than test counts, supports
correctness. The original candidate algorithm was not changed during verification
or review. Repeated solver formulations and prose/layout repairs remain in this
round. Actual campaign-specific time and token totals were not measured.

Cause and confidence: the unguarded screening variant admits a double-dynamic
shortcut because the destination's mate has unused nearby vertices. Occupying
that ball with mates outside T forces the first dynamic endpoint farther away.
This is supported by the preserved counterexample, the general proof, and native
independent review; it is not merely an inference from a passing sample.

Consequence: when extending a single-dynamic-edge reduction to two alternations,
check the forced destination partner's neighborhood, not only the destination's
own free slots. The matching and distance premises are essential. The result
does not settle one alternation or arbitrary cost ratios.

**Experience extraction:** one reusable guard-ball finding is identified for
`research/experience/forced-partner-ball.md`. During the campaign this destination
is outside the write boundary; publication to the shared collection is deferred
to authorized post-campaign board maintenance. No existing matching entry was found.

## Next action

Close discovery after 1 of the allocated 20 rounds: the fixed positive target
has reached ready_for_expert_review, so manufacturing another 19 attempts is not
justified. Transfer the single pending finding during post-campaign maintenance.
Human expert correctness and novelty assessment remains outstanding.

Post-campaign extraction, 2026-09-16: saved
[forced-partner-ball.md](../../../../research/experience/forced-partner-ball.md).
One shared entry created, zero existing entries updated, zero pending. This
supersedes the transfer-pending status above without claiming earlier retrieval.
