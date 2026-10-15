# Guarded destination partners for two-alternation routing

Status: candidate general proof; independent review pending.

## Theorem and representations

Partial Domination on an explicitly represented hypercube Karp-reduces to
one-switch reconfigurable routing on a hypercube with one port per vertex,
static cost 1, dynamic cost 1/2, and at most two medium alternations per path.
The rule recovers a source dominating set from every feasible target matching.
The proposed consequence is NP-completeness, including the ordinary explicit
network representation. The question and contract fix the compact executable
representation; the explicit expansion bound below is part of the reduction.

Write h(u,v) for Hamming distance and B(c,j) for a closed Hamming ball.
For a partial matching E with mate function m, the doubled shortest route cost is

    min { 2h(u,v),
          1+2h(u,a)+2h(b,v) for both orientations of every {a,b} in E,
          2+2h(m(u),m(v)) if both endpoints have mates }.

A simple path cannot contain consecutive distinct dynamic edges, since E is a
matching. At most two alternations therefore permits exactly the all-static,
static–dynamic–static, and dynamic–static–dynamic shapes (empty segments allowed).
The displayed expressions produce walks, but cycle deletion does not increase
length or medium alternations, so they determine the exact optimum. All costs
are positive. This also supplies polynomial witness checking. A feasible instance
has a matching witness with at most twice as many edges as positive demands:
retain only dynamic edges used on a chosen route for each demand. The compact
language is therefore in NP (dimension is unary, and bit labels have that length).

## Construction

Let T be the active vertices of Q_d, t=|T|, and k the source budget. Malformed
inputs map to fixed NO. Empty T or k>=t maps to fixed YES and recovers T; nonempty
T with k=0 maps to fixed NO. Hence assume 1<=k<t and d>=1.

Set r=d, b=2d+3, ell=4b+d=9d+12. Reserve the low d coordinates for the source
cube and four disjoint b-coordinate blocks. Let o,s,g,h denote the bit masks
of these respective blocks, with every bit in that block equal to one.
Let M be the source cube with all four blocks zero and N[M] its closed
neighborhood in Q_ell. Let L be the first k integer-labeled vertices of the
sphere at distance r from o. There are at least 2^d such vertices: choose one
coordinate from each of d disjoint pairs among the ell coordinates.

Let F=(N[M] union B(o,r+1)) minus (T union L). The forced matching consists of

1. {v,v XOR h} for v in F minus {o};
2. {o,s};
3. {v,v XOR g} for v in B(s,r) minus {s}.

Give each of these q edges a demand of weight alpha=t(r+2)+1. Give each t in T
a unit demand to o. In doubled units the bound is

    K = alpha*q + t(2r+3) - 2k.

The algorithm enumerates finite balls and sorts integer labels, so it is
deterministic. The matching is not part of the output: only demands and the bound
force its presence in a feasible solution.

## Geometric separation

N[M] is contained in B(0,r+1). The six regions containing forced endpoints have
centers 0, o, h, o XOR h, s, and s XOR g, and radii at most r+1. Distinct centers
are at distance at least b=2r+3, so these regions are disjoint. Each translated
pair has length b; {o,s} has length 2b. Within each region the XOR translations
are injective. Excluding o from the first family and s from the last makes the
entire forced edge set a matching. No forced endpoint lies in T or L. All of
B(s,r) is occupied, as is B(o,r+1) except L, and N[M] except T.

Every t in T has h(t,o)>=b and h(t,s)>=b. A point v in B(o,r+1) minus (L union {o})
is forced to v XOR h, at distance at least 2b-(r+1) from every t in T:
h(t,o XOR h)>=2b and h(v XOR h,o XOR h)<=r+1. The forced mate of o is s, also far
from T. Similarly, mates of all vertices of B(s,r) are outside T: the mate of s
is o; other mates lie in B(s XOR g,r), separated from T.

## Completeness

Pad a dominating set X subset T of size at most k to size k. Add a bijective
matching between X and L to the forced matching. Each selected source vertex
reaches o through its slot at cost r+1/2. Each remaining source vertex is adjacent
to a selected vertex, so reaches o at cost at most r+3/2. Forced demands use their
direct edges at cost 1/2. The total cost is at most K/2.

## Soundness for every matching

First every forced edge must be present. Its endpoints have Hamming distance
at least b>=5. Without its direct dynamic edge the route cost is at least 3/2:
a static route costs at least b; a one-dynamic route needs at least one static
edge; a two-dynamic simple route needs a nonempty static segment and costs at
least 2. Thus a missing edge adds at least alpha to the unavoidable forced-demand
baseline alpha*q/2. But the entire remaining budget is

    t(r+3/2)-k < alpha.

All other demands have nonnegative cost. Hence a missing forced edge is impossible.

Fix a low demand from t in T to o, and classify routes of cost <=r+3/2.
A static route is too long because h(t,o)>=b>r+3/2. For a route using one dynamic
edge {u,v}, oriented toward o, the cost is at least h(t,u)+1/2+h(v,o). Thus v must lie
in B(o,r+1). If v is a forced vertex, its mate is too far from t by the preceding
separation bounds. The only remaining possibility is v in L, where h(v,o)=r;
the cost bound then requires h(t,u)<=1.

For a route using two dynamic edges, its final edge is {s,o}, and the first
edge is {t,m(t)}. Since all vertices in B(s,r) are already matched to vertices
outside T, m(t) cannot lie in this ball. Its route cost is consequently at least
1/2+(r+1)+1/2=r+2>r+3/2. This excludes precisely the extra route shape missing
from the one-dynamic-edge model.

It follows that every low demand costs at least r+1/2; equality holds exactly
when t is matched directly to a slot. A demand without such an edge costs at
least r+3/2 (single-edge route costs have half-integer fractional part; a
static or two-dynamic route is even more expensive under the stated bounds).
Let a be the number of source vertices matched to slots. Since |L|=k, a<=k.
The sum of low-demand costs is at least t(r+3/2)-a. Feasibility requires a>=k,
so a=k and every nonselected demand must attain r+3/2. Its short-route
classification shows adjacency to a source vertex matched to a slot.

Therefore X={t in T: m(t) in L} has exactly k vertices and dominates T. Additional
matching edges, unused cube vertices, nonoptimal witnesses and reversed edge
orientations do not alter this argument. Recovery computes L again and reads X
from the supplied matching; it never solves the source instance.

## Bounds and known hardness

Let N=2^d be the number of explicitly encoded source activity bits. The output
cube has V=2^ell=4096N^9 vertices. Ball enumeration visits at most V vertices per
ball and uses O(ell^2) bit operations to form each label; sorting costs O(V ell^2)
bit operations with a conservative comparison bound. The matching has O(V)
edges. Alpha=O(N log N), and K=O(VN log N), so weights and bound have O(log N)
bits. The sparse executable output has O(V log N) bits; a dense demand matrix
would still have polynomial size O(V^2 log N). The explicit cube edges can be
enumerated in O(V ell^2) bit time and have O(V ell^2) encoded bits. Thus using a
compact cube description does not conceal an exponential blowup in this map.
A conservative bound for construction and explicit expansion is O(N^9 log^2 N)
bit operations, in addition to parsing the source integer k. The trivial cases
handle arbitrarily large k without loops depending on its numeric value.

Recovery recomputes the sphere and scans the witness in time polynomial in N
and the encoded witness length; it returns at most N source indices and hence
O(N log N) bits. Source-domain validation checks the activity length before any
exponentiation depending on a malformed dimension. Python's integer conversion
limit is disabled so valid large encoded integers are not rejected accidentally.

Source hardness is Kutner–Stewart, arXiv:2401.13359, Theorem 7, pp.28–29. Their
coordinate-producing induced-grid embedding supplies the explicit activity
encoding used here. The resulting composed reduction is Karp, not an oracle
reduction. Their delta=1 hardness does not itself settle this sigma=2 target;
the additional occupied partner ball is the claimed new ingredient. Current
novelty coverage is recorded in question.md and requires independent review.
