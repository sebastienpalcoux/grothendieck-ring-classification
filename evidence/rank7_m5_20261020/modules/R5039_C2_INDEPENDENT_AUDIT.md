# Conditional C8 exclusion for the conductor-eight branch c=2

This note audits a conditional exclusion for `R7_5_5039`. It does not
exclude the other branch c=0, and does not by itself classify the ring.

## Complete categorical alternatives

The established general-to-Galois-pseudo-unitary reduction permits use of
the canonical spherical structure and its anomaly-one center. The source
second indicators have the unique assignment `(1,0,0,1,1,1,1)`; no other
sign choice is dropped. Exact source-character reciprocity leaves only
low frames 1 and 3 in the current canonical enumeration. Their twist-one
conductor-eight weights are respectively 8 and 0. The uniform local
projection bound gives total weight at two-primary order one at most 2,
so frame 1 is impossible independently of all higher-moment constraints.

Frame 3 has two distinct character-to-restriction-row assignments.
Repeated restriction rows identify the other enumerated assignments;
the two remaining assignments are both retained as cases 0 and 1. No
source automorphism is assumed to exchange the conductor-five signs.

The sign-safe projection argument in
`CHI_MINUS8_SIGN_SAFE_DICHOTOMY.md` gives c=0 or c=2. In c=2 the exact
active weights at two-primary orders 1,2,4,8 are 2,2,4,8, exhausting the
total 16. A fifth-primary order at least 25 would require a source-fixed
five-cycle and its distinct source-dual row, of total weight at least 10
within one of these groups, which is impossible. Thus every active twist
has order dividing 40. This is a consequence for active rows only.

## All-order phase coverage and signs

Inactive rows retain the complete 61-record inventory for moments
1,2,4,8 over `F=Q(sqrt(5),sqrt(2),i)`. A twist of order `2^a 5^b`
has all four relative moments zero exactly when `a>=7` or `b>=2`.
Every other moment vector occurs already at an order dividing 320.
The zero vector remains in the domain; there is no bound on the actual
orders of inactive twists.

For a fixed restriction row, automorphisms fixing the complete source
field have positive normalized signs, and their square action supplies
packets of size `2^max(a-3,0) 5^max(b-1,0)`. Thus genuine-zero counts
lie in `16N+5N`. For a row fixed up to duality by the *actual positive*
conductor-five transport, fifth-primary inversion exchanges two disjoint
source-fixed packets. The zero counts, split by fifth-primary part
1,5,or at least25, have necessary units 16,32,10 respectively.

The implementation selects the nonnegative row from `T(v)` and `-T(v)`.
Mixed signs are inadmissible. The conditional doubling test compares this
selected row with `v` and its source dual. It never assumes the raw linear
transport is positive. The full transport-plus-duality row orbits preserve
the relative F-moment vector: one may choose the conductor-five-changing
automorphism to fix the entire two-primary factor, while its square
inverts the fifth-primary factor; that inversion fixes its relative
trace over `Q(sqrt(5))`. Source duality also preserves the twist.

The finite row domain is exhaustive under the necessary bounds. Each
high restriction coordinate is at most the square root of the corresponding
diagonal of the induction Gram matrix. The code enumerates every such
nonnegative integer vector and tests dimension divisibility, residual Gram
compatibility, signed transport and duality closure. The additional central
eigenvalue-integrality filter is also necessary. These tests may leave
spurious rows, which only enlarges the relaxation.

## Higher-indicator equations and exact contradiction

The fourth- and eighth-indicator systems use the complete nonnegative
integer characters of pivotal cyclic rotation on `Hom(1,X^4)` and
`Hom(1,X^8)`. The grouping identities are

`Tr(R8^2)=nu4(X^2)` and `Tr(R8^4)=nu2(X^4)`.

They hold for the canonical pivotal structure; the source unit contribution
is included. The eighth trace is allowed its full `Z[zeta8]` coordinates,
including half-integral coefficients in the sqrt2/i sqrt2 basis. See
`EIGHTH_INDICATOR_SYSTEM.md` and the independent coefficient and actual-center
controls accompanying the builder.

For each of the two low assignments the exact exported system has 1,700
integer columns and 625 equations. Its stored integer functional has 86
nonzero entries and satisfies

`y * column = 0 (mod 256)` for every column,

but `y * right_hand_side = 128 (mod 256)`.

Consequently neither system admits even an unrestricted integer solution.
The functional uses only restriction-Gram equations, first and second
moments, the conductor-eight/five projection budgets, and fourth/eighth
rotation equations. No numerical infeasibility report is used in this
argument. The complete system additionally contains other valid necessary
conditions; these do not invalidate the direct modular contradiction.

`verify_r5039_c2_domain.py` regenerates both eligible low domains and the
complete high domains from the canonical tensor, checks the low-frame
elimination and both surviving assignment classes, reconstructs both frozen
systems, and independently checks every modular scalar product. Its
conclusion is exactly: the c=2 alternative for R7_5_5039 is impossible.
