# R455: a finite central integer and correlated-rotation obstruction

The new general Galois-pseudo-unitary gate for `R8_3_455` reduces
complex categorification to pseudo-unitary categorification. The
following necessary central-data campaign then gives a contradiction.
No prohibition on integral central simples is assumed for this ring.

## Integer domain and monodromy parity

The FP field is Q(√3,√13), with global dimension D=39+9√13 and
quadratic norm468. The complete low/S domain has one frame and two
assignments of two identical columns. There are13 possible high
restriction vectors. All pass complete-character S-ratio algebraic
integrality. Two independent exact integer-Gram enumerations agree
on812 multiplicity patterns; all49 entries of the unreduced Gram are
rechecked. Twenty distinguished self-dual cubic Verlinde coefficients
leave24 patterns. All24 pass full field-Galois eigenvalue multiplicity
balance for each fixed distinguished fusion matrix.

There are two distinct distinguished central simples whose restrictions
are the tensor unit. One is the tensor unit; call the other G. Their
codegrees coincide, so the verifier explicitly identifies the FP
character first. This is essential to distinguish the tensor-unit
S row from the grading character. Since I(1) is multiplicity-free on
these constituents, these are the only central simples forgetting to
one. Therefore G²=1. Also θ_G=1 because G occurs in I(1).

For a central simple Z with S(G,Z)/d_Z=−1, balancing gives
θ_(G⊗Z)=−θ_Z. Thus G⊗Z is not Z. Since F(G)=1, the two simples have
the same restriction column. Every negative-monodromy column must
therefore occur an even number of times. This exact necessary parity
condition leaves12 patterns. All120 distinguished low-pair products
on these patterns admit exact nonnegative *integer* aggregate
forgetful decompositions; this is a recorded positive necessary test,
not a categorical construction.

## Complete correlated trace domain

Use basis(1,√3,√13,√39). The primitive quadratic conductors are12,13,156.
The spherical Cauchy theorem restricts twist-order prime support to
{2,3,13}, from the norm of D. For retained powers1 through6, the
complete relative-trace bound is

B6 = 2^(2+floor(log2(6))) 3^(1+floor(log3(6))) 13^(1+floor(log13(6)))
   = 1872.

This is a bound on retained trace types, not on the categorical exponent.
For a primitive Nth root and retained power k, put g=gcd(N,k), n=N/g.
The rational coefficient is μ(n)/φ(n). For q∈{3,13,39}, with quadratic
conductor Fq and character χq, the √q coefficient is zero unless
Fq|n and gcd(n/Fq,Fq)=1. Otherwise it is

εq μ(n/Fq) χq(n/Fq) χq(k/g) sqrt(Fq/q) / φ(n).

The four sign choices are linked by ε39=ε3 ε13 across every retained
power. These are the exact Ramanujan and quadratic Gauss projections.
If an order has a p-valuation larger than the exponent in B6, every
retained reduced order has valuation beyond both one and all conductor
valuations. Every rational and quadratic term vanishes. Thus orders
dividing1872, together with the joint zero vector, give the complete
finite domain. There are55 distinct joint trace types.

This is the existing manuscript Proposition `prop:m3-biquadratic-traces`
instantiated at height6 in Q(√3,√13). The new code adds the field adapter
to the full-character STS and fixed-integer-pattern campaign; the older
noncommutative quartic engine only handled Q(√2,√3).

## Complete joint rotation and STS contradiction

For each of12 integer patterns and all four allowed second-indicator
tuples, the system includes the Gram identities, first and second
indicator moments, every divisor-power tensor rotation on
Hom(1,X^n) through n=6, full distinguished STS equations, and the exact
high multiplicities. The two possible distinguished-character assignments
give identical systems because the corresponding restriction columns
are equal. Each system has381 rows and792 nonnegative variables.

All48 systems have exact Farkas certificates. In fact one common exact
integer dual vector verifies every branch: Aᵀy≥0 and bᵀy<0. The
numerical solver only discovered it; the replay recomputes all equations
and checks the inequalities exactly. Consequently no pseudo-unitary
categorification exists, and the independent general gate promotes this
to nonexistence of a complex fusion category.

## Controls and replay

The adapter reproduces the complete earlier Q(√2,√3) height-six trace
domain exactly. Independently computed cyclotomic relative traces at
orders12,13,24,26,52,156 agree with the formula, for every retained power
and every primitive root. The actual center Z(Vec(C2)) passes full STS
and all tensor-rotation identities through height6.

Canonical read-only complete replay:

```
python evidence/rank8_frontier_20261021/r455_center_integer/verify_all.py
python -O evidence/rank8_frontier_20261021/r455_center_integer/verify_all.py
```

The first stage reconstructs812 integer patterns and all filters; the
second replays120 exact integer tensor decompositions; the third checks
all48 exact infeasibility certificates. The separate files
`verify.py`, `pair_tensors.py`, and `joint_rotation.py` expose each stage.
The general scope dependency is
`noncommutative_followup/additional_scope_gates.py/.json`.

Primary sources: Ostrik arXiv:1309.4822 Theorem2.13 (I(1)); Ostrik
arXiv:0810.3242 Theorem1.8 (d-numbers); ENO arXiv:math/0203060
Proposition3.3 (D/d_Z); Deshpande arXiv:1611.04486 equation(39)
(distinguished S rows); Bruillard–Ng–Rowell–Wang arXiv:1310.7050v3
(spherical Cauchy theorem); Ng–Schauenburg arXiv:math/0601012
(categorical indicators and rotations).
