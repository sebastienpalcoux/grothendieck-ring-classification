# R439: a centerless Morita partner fails the cubic Verlinde test

## Statement and scope

There is no complex fusion category with based ring `R8_3_439`.
The proof uses the independently verified general Galois-pseudo-unitary
reduction, the unconditional full-S3 condensation, the complete rank-five
Morita-partner enumeration, and the integral-center-subcategory lemma.
It does not assume uniqueness of an associator on a known based ring.

The canonical arithmetic replay is

```
python evidence/rank8_frontier_20261021/r439_centerless_rank5/verlinde_exclusion.py
python -O evidence/rank8_frontier_20261021/r439_centerless_rank5/verlinde_exclusion.py
```

Both reconstruct the finite domain and all exact obstructions. Neither
uses a numerical optimizer. Both passed on 2026-10-21.

## Reduction to one rank-five based ring

1. `noncommutative_followup/additional_scope_gates.py` proves that any
   categorification of R439 has a pseudo-unitary Galois conjugate.
2. `structural_models/pointed_s3_scope.py` proves the pointed S3
   associator class is zero. Its restriction to C3 is zero because C3
   fixes a noninvertible simple; the forced transposition indicator +1
   makes its restriction to C2 zero. Restriction/corestriction then
   annihilates the class by both 2 and 3. Thus the full regular S3
   separable algebra exists.
3. `structural_models/s3_full_condensation.py` exhausts the possible dual
   based rings; `rank5_route_bindings.py` binds all of them to the frozen
   rank-five census and replays the applicable exclusions. Only
   `R5_3_40` remains. Morita invariance of categorical dimension and FP dimension preserves
   pseudo-unitarity of this dual (ENO Theorem 2.15 and Corollary 8.14);
   ENO Proposition 8.23 supplies its canonical spherical structure.
4. `structural_models/known_model_routes.py` proves that the original
   category has no nontrivial invertible object in its center. Centers
   are Morita invariant, so the same holds for the rank-five dual.
5. `review/INTEGRAL_CENTER_SUBCATEGORY.md` strengthens this to absence
   of every nonunit integral-dimensional central simple. Briefly,
   these simples form a fusion subcategory E. Its integer dimension N
   divides 576, by ENO Proposition 8.15 and
   Norm(D²/N)=576²/N². Thus E is solvable by ENO's p^a q^b theorem;
   a nontrivial solvable category has a nontrivial invertible, a
   contradiction.

The source rank-five tensor, all 125 entries, is bound to the frozen
archive by SHA256 in the receipt. Its labels are `(1,s,V,P,Q)`, all
self-dual, with dimensions `(1,1,2,3+2√3,3+2√3)` and
D=48+24√3. The formal codegrees are D, D′=48−24√3, 3, 4, 4.

## Complete central induction domain

The complete low-column enumeration has 24 frames. The ordinary
positive-semidefinite/moment conditions leave five. Full symmetry of
all distinguished S entries leaves exactly the following frame:

```
(1,0,0,0,0)
(1,0,0,1,1)
(1,1,1,2,2)
(1,0,1,1,2)
(1,0,1,2,1)
```

There are two assignments of the last two equal-codegree characters;
both fix the distinguished simple A corresponding to D′. The high
Gram matrix on `(s,V,P,Q)` is

```
[4 2 4 4]
[2 6 7 7]
[4 7 34 31]
[4 7 31 34]
```

Every high restriction is a nonnegative integer vector v with
Q−vvᵀ positive semidefinite, central simple dimension a d-number
(Ostrik, arXiv:0810.3242, Theorem 1.8), and D/d_Z an algebraic integer
(ENO, Proposition 3.3, applied to the modular center of dimension D²). This finite complete domain has 38 vectors. Four have
integral dimension, and are forbidden by the preceding lemma. A fifth
has a nonintegral S-ratio eigenvalue (−3/2), impossible for an integral
fusion matrix. `rank5_integer_gram/verify.py` uses two independent exact
finite enumeration algorithms; they agree on exactly 58 nonnegative
integer multiplicity vectors satisfying all ten Gram equations.

## A single cubic coefficient excludes all 58 patterns

Use the unnormalized modular S matrix of the center, with S(1,Z)=d_Z
and center global dimension D². Deshpande's distinguished-row formula
is S(A,Z)=(D/D′)χ(FZ), where χ is the conjugate-FP character. Since
A is self-dual, Verlinde gives

N(A,A;A) = (D/(D′)³) Σ_Z χ(FZ)³/d_Z.

The sum includes each of the five distinguished central simples once,
and every high restriction with its complete integer multiplicity.
The character is `(1,1,2,3−2√3,3−2√3)`. A is self-dual because it is
the unique distinguished simple of dimension D/D′=7+4√3 and I(1) is
stable under duality. This coefficient must be a nonnegative integer.

The 58 complete possibilities give exactly:

| N(A,A;A) | Number of patterns |
|---|---:|
| (7−√3)/6 | 16 |
| 1/3 | 16 |
| (19−5√3)/12 | 16 |
| (6−√3)/3 | 6 |
| (1+2√3)/3 | 4 |

None is an integer. This excludes every possible center of the forced
rank-five dual and hence excludes R439 in general complex scope.

The verifier independently checks the same normalization on the
actual Fibonacci center Fib⊠Fib^rev: the distinguished object `(X,X)`
has N((X,X),(X,X);(X,X))=1.

## Exploratory exact relaxations

`verify.py` and `results.json` preserve the preceding exact height-six
joint rotation, full STS, partial-S integrality, and Galois spectrum
balance experiment. One rational centerless branch is feasible and
one is infeasible. This does not conflict with the final obstruction:
all 58 *integer* Gram completions fail a cubic fusion coefficient.
`initial_rotation_results.json` is an explicitly noncanonical discovery
snapshot from before the stronger integral and Galois balance filters.
It is not an exclusion certificate or an additional completed test.

## Primary sources

- V. Ostrik, *On formal codegrees of fusion categories*,
  arXiv:0810.3242, Theorem 1.8: braided pseudo-unitary simple dimensions
  are d-numbers.
- V. Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822,
  Theorem 2.13 and Corollary 2.15: induced-unit constituents and formal
  codegrees.
- T. Deshpande, *On centers of bimodule categories and
  induction-restriction functors*,
  arXiv:1611.04486, equation (39): the distinguished S rows.
- P. Etingof, D. Nikshych, V. Ostrik, *On fusion categories*,
  arXiv:math/0203060, Proposition 8.15, Theorem 2.15, and Corollary 8.14:
  dimension divisibility and Morita dimension invariance.
- P. Etingof, D. Nikshych, V. Ostrik, *Weakly group-theoretical and
  solvable fusion categories*, arXiv:0809.3031, Theorem 1.6 and
  Proposition 4.5(iv): the integral-center-subcategory step.
