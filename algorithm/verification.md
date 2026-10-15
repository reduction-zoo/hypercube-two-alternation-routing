# Verification evidence

The actual candidate is work/algorithm.py, unchanged since its first tests.
`python3 work/check.py --candidate work/algorithm.py` from the campaign root
passes 9 injected sources and 10 recovery calls, including malformed source
objects, empty sets, zero budgets and nontrivial YES/NO instances. Its target
solver is independent of the candidate and ranges over arbitrary matching
endpoints. Raw output: [prepared-checks.jsonl](../history/campaigns/hypercube-two-alternation-routing/rounds/001/prepared-checks.jsonl).

`python3 work/verify.py --candidate work/algorithm.py` passes all 36 sources
with d=1 or 2, nonempty active sets, and 1<=k<=|T|. It makes 124 Boolean solver
queries and executes 66 recoveries, including witnesses with an extra unused
matching edge. Raw output: [verification.jsonl](../history/campaigns/hypercube-two-alternation-routing/rounds/001/verification.jsonl).
The source answers use exhaustive subset enumeration. The second target program
imports neither the candidate nor check.py.

Its target oracle first proves mandatory edges by the generic demand-gap bound.
For each remaining demand it enumerates all legal route shapes through a finite
length cutoff, enforcing consistency of new matching edges with the mandatory
matching and one another. Longer routes receive an unconstrained optimistic
cost of cutoff+1. UNSAT therefore certifies infeasibility even before reaching
the full bound. A SAT model is accepted only when it uses no overflow option,
and its actual matching's workload is then evaluated exactly. Otherwise the
cutoff increases by one, at most to the residual budget. All demand weights are
positive, so overflow cannot occur in a feasible model at that final cutoff.
This is a finite exact test oracle, not a polynomial-time claim. In particular,
when both demand endpoints are free, it may enumerate all cube vertices.

Both target programs passed tiny exhaustive matching crosschecks. A Q4 instance
whose strict optimum uses two dynamic edges passes at doubled workload bound 24
and fails at 23 in both programs. Incorrect subprocess forward outputs and
incorrect recovered witnesses were detected. See
[foundation checks](../history/campaigns/hypercube-two-alternation-routing/work/evidence/preparation/negative-and-enumerator-checks.json).
[Transport checks](../history/campaigns/hypercube-two-alternation-routing/work/evidence/preparation/transport.json) additionally cover seven
malformed objects, three malformed JSON values, and a 5001-digit source budget.

Finite coverage does not establish correctness for arbitrary source dimensions,
all target matchings or all encodings. Those are obligations of proof.md and the
independent review. The forward cube dimension can be 30 even in these tiny
source tests; the target cube is represented implicitly and no billion-vertex
explicit cube was materialized. The polynomial explicit expansion is a theorem
obligation, not an observed execution-size claim.
