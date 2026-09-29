# Full-character ambient cyclotomic continuation

This directory records further necessary-condition calculations on the four
multiplicity-four inputs R6_4_155, R6_4_211, R6_4_243, and R6_4_629. Discovery
and classification are distinct: a surviving relaxation does not construct a
category, and a pseudo-unitary obstruction needs a separate general-scope
reduction before allocation.

`software/round3_m4.py` extends central-induction constraints when the complete
character field is larger than the Frobenius–Perron dimension field. Its
computations use the complete input tensor, with no identifier exception.
The implementation supports ambient conductors 1, 3, 4, 5, 8, 12, 15, 16,
20, and 24, reconstructs all low induction frames and all character labellings,
and imposes Gram, Frobenius–Schur, cyclic-rotation, joint-spectrum Galois, and
low modular-pair equations. Eligibility is checked exactly; unsupported fields
are explicitly ineligible. Every reported separating ray is checked over the
integers.

## A direct relative trace formula

Fix K = Q(zeta_F). Let zeta_n^a be a root of unity, reduce it to primitive
order m = n/gcd(n,a), and put b = a/gcd(n,a), d = gcd(m,F), r = m/d.
Its normalized relative trace from Q(zeta_lcm(F,m)) to K is zero if
`gcd(r,F)>1`. Otherwise it is

    mu(r)/phi(r) * zeta_d^(b * inverse(r mod d)),

with the exponent interpreted as zero when d=1.

For the zero case, some p-adic order of m exceeds the p-adic order of F;
the kernel of restriction to K contains the full primitive p-extension, whose
root sum is zero. In the other case gcd(r,F)=1. The identity
`zeta_m = zeta_d^inverse(r mod d) * zeta_r^inverse(d mod r)` and the
cyclotomic Chinese remainder theorem reduce the relative trace to the
primitive r-th root sum mu(r), divided by phi(r). This includes r=1 and
r=2 without exceptions. Evaluation uses exact polynomial arithmetic.

For moments j=1,...,h and roots whose order has prime support P, put

    B = product_{p in P} p^(max(1,v_p(F)) + floor(log_p h)).

Every order outside the divisor box n|B has zero joint trace: an excessive
p-power remains excessive after division by gcd(n,j). Thus the finite domain
consisting of all normalized joint traces for n|B plus the zero vector is
exhaustive. This domain deliberately overapproximates all possible center
exponents; no exact Frobenius–Schur exponent is assumed.

The direct formula avoids constructing the much larger field Q(zeta_B).
`trace_formula_controls.py` independently compares it with explicit Galois
averaging in compositum fields.

## Rotation and modular equations

For each simple X and 3 <= n <= h, cyclic rotation on Hom(1,X^n) has n-th
roots as eigenvalues. Its dimension is [X^n:1]. For every proper divisor r
of n, its r-th power has trace nu_(n/r)(X^r). Applying normalized relative
trace to K expresses these identities linearly in the center twist-type
counts and nonnegative rotation-eigenvalue multiplicities. The latter counts
are relaxed to nonnegative real numbers, so infeasibility is necessary while
feasibility remains inconclusive.

The complete character table is embedded and checked in K. For low central
objects A,B with twist one, the modular identity STS = D T^(-1) S T^(-1)
gives the low-pair equation. Joint fusion eigenvalue integrality and Galois
orbit-count equality give further exact rows. Version 1 imposes Galois equality on total joint-type counts; this already
excludes R6_4_211. Version 2 couples a joint eigenvalue type with its trace
type: sigma acts on the eigenvalues and sigma squared acts on twist traces.
The two paired-type counts must agree, including the known low objects.
This specializes to fixed-trace-type equality only when every Galois square
fixes the ambient field. The implementation reconstructs the induced trace
permutation exactly, so no unjustified fixed-type assumption is made.

## Reproduction

From the package root, for example:

```sh
python software/round3_m4.py R6_4_211 --height 3 --conductor 24 --seconds 840 --output research/round3/m4/R6_4_211_ambient_h3.json
python software/round3_m4.py R6_4_629 --height 6 --conductor 15 --seconds 840 --output research/round3/m4/R6_4_629_ambient_h6.json
python research/round3/m4/trace_formula_controls.py
```

The separate R6_4_243 probe adds nonnegative integral low Verlinde
coefficients, restriction-product decompositions, and rational-rotation
congruences to the existing quadratic engine. The proof of the inherited
modular-moment hypotheses must be retained when interpreting its result.

## New exclusions under exact replay

Two complete discovery campaigns give additional pseudo-unitary obstructions:

- `R6_4_211`: dimensions `(1,1,d,2d+1,2d+1,d)` with `d=2+sqrt(6)`;
  global dimension `120+48sqrt(6)`; full character field
  `Q(sqrt(2),sqrt(3))`. The ambient conductor 24, trace height 3, and
  exhaustive order bound 144 give 53 joint trace types. There are 130 low
  frames and 16 exact separating rays.
- `R6_4_243`: dimensions `(1,1,d,d+1,d+1,d)` with `d=7+sqrt(57)`;
  global dimension `456+60sqrt(57)`. The height-six low-Verlinde,
  restriction-product and rational-rotation system exhausts 210 low frames
  and gives 48 exact separating rays. No congruence-only branch is needed.

The separate unrestricted sphericalization reductions reconstruct 128 signed
quotients in four sign orbits for `R6_4_211`, and 1,584 signed quotients in
53 sign orbits for `R6_4_243`. In each case exactly one orbit is sign-gauge
isomorphic to the original tensor; all other character components are
rejected by the established exact arithmetic obstructions. These reductions
prove that any complex fusion categorification would be spherical and have
a pseudo-unitary Galois conjugate. The combined records are
`R6_4_211_general.json` and `R6_4_243_general.json`.

The exact replay reports `R6_4_211_exact_replay.json` and
`R6_4_243_exact_replay.json` both have `passed: true` and certify
exhaustive reconstruction with numerical optimizers disabled, under
optimized Python. The verifier modules are respectively
`software/round3_m4.py` and `software/round3_verlinde.py`.

R6_4_155 survives the full-character conductor-eight height-six system,
including coupled Galois spectrum/twist counts. R6_4_629 survives the
conductor-fifteen height-six system with the same refinement. These records
are retained as genuine surviving necessary-condition branches.


The complete initial control scans have 76 records each (54 positive models
and the frozen 22-ring frontier), with explicit nonapplicability and budget
outcomes. Follow-up positive-control scans try the opposite indicator order
to reach feasible branches sooner; they establish only survival, never an
exclusion from a partial search. Four certificate-mutation controls verify
that both checkers reject an omitted low frame or omitted indicator case.

Here `no_exact_obstruction` records failure to find an exact negative
certificate in the tested relaxation. Unless separately accompanied by an
exact primal witness, it is not a certified feasibility assertion.


The additional `probe_629_verlinde.py` combines the conductor-fifteen
height-three full-character system with low Verlinde positivity and
restriction products. Its first surviving branch has 4,493 equations and
4,810 nonnegative variables; no exact obstruction was found in 792.799
seconds. This is a completed bounded search outcome, not an exact primal
feasibility witness and not a categorification.
