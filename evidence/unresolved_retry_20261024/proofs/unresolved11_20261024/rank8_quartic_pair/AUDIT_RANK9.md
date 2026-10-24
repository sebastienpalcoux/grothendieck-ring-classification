# Independent audit of the new rank-nine restrictions

Audit date: 2026-10-24. The published project baseline is classification
commit `323c4227ffb796a72eef506f1eb289437fbc95db`.

**Result: PASS for the categorical implications and the three positive-TY-sign
branch exclusions described below. No whole fusion ring is excluded, and no
category model is produced.** The negative-sign branches remain open. The
new conclusions use the explicitly identified published project dependencies;
they do not assume a unitary classification of spherical categories.

## 1. Categorical scope

I read `rank9_commutative/NO_CENTRAL_BOSON.md`,
`rank9_noncommutative/NEW_RESTRICTIONS.md`,
`rank6_pair/POINTED_AUTOMORPHISM_OBSTRUCTION.md`, and
`rank9_commutative/TY_SPECTRUM.md`, together with the referenced published
rank-six sphericalization/center arguments and the prior TY module reduction.

The no-central-boson arguments are valid for arbitrary complex fusion
categorifications. The following points are essential.

* The integral subcategory is the already forced nonalternating
  `TY(V4,chi,tau)`. Trivial universal grading makes the forgetful map on
  central invertibles injective. Consequently a lift of the free isotropic
  involution has order two. Restricting its half-braiding to TY gives
  self-braiding `chi(g,g)=+1`, so its generated subcategory is Tannakian.
* The central `Rep(C2)` forgets fully faithfully to the full subcategory on
  `1,g`. Central de-equivariantization therefore is a fusion category and
  the original category is its `C2`-equivariantization. These statements
  use no pivotal structure. The free orbits and the fixed dimension-two
  simple give quotient dimensions `(1,1,1,1,d,d)`, as claimed.
* For the commutative cases, the two quotient tensors are exactly
  `R6_4_174` and `R6_4_6`, with general-complex exclusions in the project.
  For `R9_2_1975` they are `R6_4_155` and `R6_4_1`. The former is **not**
  excluded: its tensor-autoequivalence obstruction instead forbids the
  required equivariantization.
* The `R6_4_155` obstruction really covers each original category. The
  published spherical/Galois argument gives a spherical structure in each
  original complex categorification. The fusion rules make
  `Aut_tensor(Id)` trivial, so its pivotal structure is unique. Its four
  unique central lifts have pairwise distinct twists in the PU Galois
  representative, and inverse Galois transport preserves distinctness.
  Thus every complex-linear tensor autoequivalence fixes every
  invertible. This excludes the nontrivial invertible normalizer in the
  extreme rank-twelve tensor, and makes a `C2`-equivariantization have
  eight invertibles, contrary to the rank-nine source.

The new integral-center argument also has the stated scope. For
`D=144+96 sqrt(2)`, the norm is `2304=2^8*3^2`. Algebraic-integer
FP-dimension divisibility forces a Tannakian group's order to involve
only primes 2 and 3. Burnside solvability then forces a nontrivial
one-dimensional character if the group is nontrivial, contradicting the
absence of central bosons.

The integral central simples form a fusion subcategory: their forgetful
images are exactly the objects of the integral TY subcategory, because
every central simple has dimension `a+b d` with nonnegative integer
`a,b` and irrational `d`. Its integer FP dimension again has only
primes 2 and 3. ENO Theorem 1.6 implies solvability. This integral braided
subcategory is weakly anisotropic because it contains no nontrivial
Tannakian subcategory. Natale Theorem 4.1 therefore makes it pointed.
The theorem does **not** require it to be nondegenerate. It follows that
the integral center is `Vec` or `sVec` in the three commutative cases,
and `Vec` for `R9_2_1975`.

The universal statement about no faithful nontrivial group grading
anywhere in the Morita class follows from the standard central
`Rep(G)` associated to such a grading and Morita invariance of the
braided center. No existence of a central lift is inferred merely from
centrality of a basis element in the fusion ring.

## 2. TY indicator and spectral restrictions

Shimizu's TY indicator formula uses the canonical positive pivotal
structure; this is stated explicitly in Section 3.1 of his paper. The
restriction of the canonical positive pivotal structure of a PU source
to its TY subcategory is that structure. The exact finite formula gives

`nu_1,...,nu_8 = (0,epsilon,0,0,0,epsilon,0,2)`

for its dimension-two object `Y`, where `epsilon=sign(tau)`.
Full inclusion preserves the invariant spaces and their rotation maps.

The Ng-Schauenburg center formula expresses `D nu_n(Y)` as the sum of
`[F(Z):Y] FPdim(Z) theta_Z^n`. Since the weights are positive and
`nu_8(Y)=FPdim(Y)=2`, equality in the triangle inequality forces
`theta_Z^8=1` on every constituent of `I(Y)`. This is an exact
saturation argument, not an assumed twist-conductor bound. The discrete
Fourier transform gives primitive-eighth-root fibers of weight `D/4`,
and either the two `+/-1` fibers of weight `D/2` for positive tau, or
the two `+/-i` fibers of that weight for negative tau. The relative
trace restrictions implemented in the screens are exactly these.

The general-to-PU reduction preserves the sign of tau. Apply the same
field automorphism to the original category, its Morita bimodule, and
the two-dimension Morita partner. The latter has a PU Galois conjugate;
Morita invariance of global dimension and FP dimension makes the
conjugated original category PU. Its TY subcategory has the same
`chi in {+1,-1}` and rational `tau in {+1/2,-1/2}`. Thus the positive
sign obstruction genuinely excludes that sign in every original
complex category, not just in a selected PU example.

The independent finite TY verifier also confirms the source induction
columns, the Fourier weights, and the claimed primitive-fiber
dimension alternatives `(1,7)` and `(4,4)`. Those latter alternatives
are not additional unrecorded assumptions of the audited screens.

## 3. Independent exact verification

`audit_ty_systems.py` independently reconstructs every equation of the
two commutative height-four systems. It does not call the discovery
functions `quadratic_center.system` or `quadratic_s_symmetry.build`.
It rebuilds the Gram equations, formal-codegree counts, Galois counts,
first and second moments, indicator-sign relaxation, invariant-space
rotation equations, labelled character counts and S-symmetry, integral
center deletions, fermion restriction and bound, TY spectrum and fixed
TY moment rows. Its complete matrices agree entrywise with the
discovery matrices, and the saved separating rays work on the
independently reconstructed matrices.

`audit_noncomm_ty_systems.py` independently reconstructs both
height-six `R9_2_1975` systems, including the degree-two character and
the conjugate-pair S-symmetry equations. It likewise never calls
`symmetry.build` or `quadratic_center.system`. Every entry agrees with
the archived matrices.

| Source | TY sign | Matrix | Exact `b^T y` | Minimum `A^T y` | Conclusion |
|---|---:|---:|---:|---:|---|
| R9_2_1607 | + | 209 x 22133 | -1253376 | 0 | Positive sign excluded |
| R9_2_1976 | + | 183 x 21943 | -17466624 | 0 | Positive sign excluded |
| R9_2_1975 | + | 259 x 1270 | -32832 | 0 | Positive sign excluded |
| R9_2_1975 | - | 259 x 1251 | n/a | n/a | Exact rational and integer feasible witnesses verified |

The last row's witness supports are 81 and 84 respectively. They certify
only consistency of the necessary linear system; neither is a category
model. System and source-tensor hashes are recorded in the four
`audit_R9_*_TY*.json` receipts.

The independent reconstruction still uses the explicitly inherited
complete restriction-column and relative-root-trace domain helpers,
and character extraction. It is an independent audit of the full
equation construction and exact contradiction, not a fresh proof of
every older domain theorem. The relative-trace representative bound
288 is the inherited complete trace compression; it is not an asserted
upper bound on the order of every actual twist.

Additional checks performed here:

* Complete coefficientwise central-quotient transports and adjoint
  generation passed; receipt `audit_comm_no_central_boson_receipt.json`.
* The noncommutative tensor transports, extreme-branch normalizer,
  pointed cocycle and full-stabilizer cochain identities passed;
  receipt `audit_noncomm_new_results_verification.json`.
* The full inherited `R6_4_1` general exclusion was freshly replayed
  under `python -O`, with all numerical optimizer entry points disabled.
  All ten low frames and their complete higher-indicator systems pass.
  See `replay_R6_4_1_dependency.py` and
  `audit_R6_4_1_dependency.json`. The commutative quotient exclusions
  `R6_4_174` and `R6_4_6` are retained as explicit published dependencies.
  A duplicate replay by the commutative investigator was cancelled
  before completion. No fresh complete replay of those two older
  certificates is claimed in this audit.

## 4. Primary sources and a corrected citation

The initial citation to Schopieray's arXiv v1 was too strong as printed:
that version claimed positivity of the original category. The
**published** Lemma 3.1 instead gives a PU **Galois conjugate**, which is
exactly the conclusion needed here. I checked the published text and
reported this version issue; the current notes use the corrected
publication. There is no remaining scope gap from that citation.

Primary theorem statements checked:

* Gelaki-Naidu-Nikshych, Proposition 4.1 and the preceding half-braiding
  formulas: <https://arxiv.org/pdf/0905.3117>.
* Drinfeld-Gelaki-Nikshych-Ostrik, Theorem 4.18, Proposition 4.19,
  Remark 4.21: <https://arxiv.org/pdf/0906.0620>.
* Etingof-Nikshych-Ostrik, solvability Theorem 1.6:
  <https://arxiv.org/pdf/0809.3031>.
* Natale, integral weakly anisotropic Theorem 4.1:
  <https://arxiv.org/html/1704.03523v1>.
* Schopieray, published Lemma 3.1:
  <https://doi.org/10.1112/jlms.12789>.
* Shimizu, Section 3.1 and Theorem 3.4:
  <https://arxiv.org/pdf/1005.4500>.
* Ng-Schauenburg, center indicator Theorem 4.1:
  <https://arxiv.org/pdf/math/0601012>.
* EGNO, Corollary 7.16.7 and Proposition 9.3.9 (Morita invariance of FP
  and global dimensions), Proposition 9.5.1 (canonical positive
  pivotal structure): <https://math.mit.edu/~etingof/egnobookfinal.pdf>.

The lower-rank center computations and the forced rank-nine TY
bicharacter remain project theorem dependencies, explicitly identified
above. This audit found no argument replacing a missing categorical
premise with successful scalar computations.
