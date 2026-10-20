# A sign-safe conductor-eight dichotomy for R7_5_5039

This necessary structural reduction replaces, and does not use, the
rejected unsigned-transport orbit argument recorded in
`CHI_MINUS8_PARTIAL_PROJECTION_AUDIT.md`. In particular, normalized
transport may send a row to the negative of its rational linear image.
The argument here uses source duality and only those Galois automorphisms
which fix the **complete** source character field.

## Exact masses from the local projection calculation

Let `w` be the difference of the two induced-unit constituents whose
source characters have formal codegree eight. For a center simple `Y`
write `v_Y` for its restriction row and `k_Y=v_{Y,1}-v_{Y,2}`. The exact
character table gives

`||w||^2=2`, and `(S w)_Y=(sqrt(-2)/4) k_Y`.

Thus the total integral squared-difference weight is

`sum_Y k_Y^2=16`.

Call an object active if `k_Y!=0`. The preceding all-level calculation
proves, for `r=0,1,2,3`,

`||Q_r S w||^2=2^r ||Q_0 S w||^2`,

where `Q_r` projects only onto the two-primary twist orders dividing
`2^r`. Set `c=8||Q_0 S w||^2`. The exact weighted masses at two-primary
twist orders `1,2,4,8` are then

`c, c, 2c, 4c`, with `0<=c<=2`.

Source duality interchanges labels one and two and hence changes `k`
to `-k`. Center duality preserves the twist. An active center simple
cannot be self-dual, because its restriction row would then be fixed
under source duality. Therefore, at each exact two-primary twist order,
the active objects form disjoint dual pairs of equal squared weight.
In particular `c` is an even nonnegative integer. There are precisely
two possibilities:

* `c=0`: every active object has two-primary twist order at least sixteen.
* `c=2`: the masses at orders one, two, four, and eight are exactly
  `2,2,4,8`; these exhaust the total weight sixteen, so every active
  object has two-primary order at most eight.

This dichotomy involves actual center objects and their integral
weights, not a real relaxation of a phase-counting problem.

## Galois cycles fixing each restriction row

All source characters, formal codegrees, and dimensions belong to

`L=Q(sqrt(5),sqrt(-2))`.

Let a central twist have exact order `2^a 5^b`, as required by the
Cauchy prime-support theorem. For every cyclotomic automorphism `sigma`
fixing `L`, the normalized character transport fixes the restriction
row of a center simple. Here signs are genuinely positive: both the
global dimension and `dim(Y)=sum_i v_{Y,i}d_i` are fixed positive
numbers, so modular Galois symmetry applied to `S_{0,Y}=dim(Y)/D`
forces the sign to be positive. Applied to

`S_{A_E,Y}=chi_E(v_Y)/f_E`,

the same symmetry and the invertible complete source character table
then force the new restriction row to equal `v_Y`.

On twists the categorical permutation acts by the squared automorphism,
`theta -> theta^{u^2}`. We use the following independent local choices.

* If `a<=3`, choose the identity at the two-primary factor. This gives
  no required two-primary cycle, so its factor is one.
* If `a>=4`, choose `u=3 mod8` and the identity at the fifth-primary
  factor. The character `chi_{-8}(3)` is one, so this fixes `L`.
  Also `v_2(u^2-1)=3`, and the squared action on a primitive
  `2^a`-th root has exact order `2^{a-3}`.
* If `b<=1`, choose the identity at the fifth-primary factor; its
  required cycle factor is one.
* If `b>=2`, choose `u=6 mod25` and the identity at the two-primary
  factor. It fixes `sqrt(5)` and `sqrt(-2)`, and
  `v_5(u^2-1)=1`. Its squared action on a primitive `5^b`-th root
  has exact order `5^{b-1}`.

Chinese remaindering gives these choices independently at the complete
exponent. Thus their orbit on twists, and consequently their orbit on
center objects with a fixed restriction row, has cardinality divisible
by

`m(a,b)=2^{max(a-3,0)} 5^{max(b-1,0)}`.

The source-dual row is different for an active object. It gives a
disjoint orbit of the same size at the same exact twist order. An
active object of squared row difference `k^2` therefore forces weighted
cost at least

`2 m(a,b) k^2`

within its exact two-primary order group. This statement is unaffected
by signs in any other, non-row-fixing Galois transport.

## The two finite support alternatives

In the branch `c=2`, the two-primary orders are at most eight, and each
exact-order group has weight at most eight. If `b>=2`, the row-fixed
five-cycle and its distinct dual row cost at least ten, impossible.
Therefore `b<=1`. Every active twist has order dividing forty. The
exact group weights are `2,2,4,8` at two-primary orders `1,2,4,8`.

In the branch `c=0`, one has `a>=4`. If `b>=2`, the independent
two-cycle, five-cycle, and distinct dual row cost at least twenty,
exceeding the total sixteen. Thus again `b<=1`. If `a>=7`, even with
`b<=1` the cost is at least `2*2^{a-3}>=32`, also impossible.
Consequently every active twist has order in

`{16,32,64,80,160,320}`.

No existence assertion is made for either support alternative.

## Consequences for the full-source phase domain

Use the field `F=Q(sqrt(5),sqrt(2),i)` and the exact phase inventory in
`models/sqrt5/FULL_SOURCE_PHASES_PROOF.md`.

* In the branch `c=2`, an active row uses only the first twenty-four
  phase types, whose orders divide forty. The weighted phase totals,
  grouped by their two-primary order, are exactly `2,2,4,8`.
  Neither the twelve order-sixteen phase types nor the zero phase
  is permitted on an active row.
* In the branch `c=0`, an active row uses only the twelve order-sixteen
  phase types (orders sixteen or eighty) or the genuine zero phase.
  Each nonzero phase count at a fixed row is even. The genuine zero
  phase can arise only from two-primary order thirty-two or sixty-four,
  whose row-fixed cycle factors are four and eight. Its multiplicity
  at each fixed active row is therefore divisible by four; the more
  permissive generic semigroup `4N+5N` can be replaced by `4N` there.

Inactive rows retain the general phase-domain restrictions. The first
branch does not claim a zero phase for every active row; that stronger
claim would wrongly discard the valid `c=2` alternative.
