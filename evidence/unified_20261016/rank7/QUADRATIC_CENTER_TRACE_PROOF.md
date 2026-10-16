# A common two-moment obstruction for three rank-seven rings

**Theorem.** None of R7_4_106, R7_4_2155, or R7_3_146 admits a complex fusion categorification.

The argument uses one Galois transport lemma, one finite root-of-unity moment hull, and four universal integer inequalities. It does not solve associator equations or assume unitarity of an arbitrary categorification. The prior source-bound signed quotient theorem, `THREE_CASE_GALOIS_PU.md`, proves that any categorification of these rings has a Galois conjugate which is pseudo-unitary. We work with that conjugate and its canonical positive spherical structure.

## 1. Common source data

Write `d_i=a_i+b_i sqrt(r)` and `D=sum_i d_i^2=48 eta`, where `eta` is a positive quadratic unit of norm one.

| Ring | r | source-label dimensions | eta |
|---|---:|---|---|
| R7_4_106 | 3 | 1,1,4+2sqrt(3),7+4sqrt(3),7+4sqrt(3),4+2sqrt(3),6+4sqrt(3) | 7+4sqrt(3) |
| R7_4_2155 | 3 | 1,4+2sqrt(3),4+2sqrt(3),1,6+4sqrt(3),7+4sqrt(3),7+4sqrt(3) | 7+4sqrt(3) |
| R7_3_146 | 6 | 1,1,4+2sqrt(6),5+2sqrt(6),5+2sqrt(6),4+2sqrt(6),6+2sqrt(6) | 5+2sqrt(6) |

The formal codegrees are `D,sigma(D),4,8,8,8,12` in the first two cases, and `D,sigma(D),4,6,6,8,12` in the third. All rings are commutative. Consequently `I(1)` has seven different simple constituents, each with multiplicity one and twist one, of dimensions `D/f_E` (Ostrik, Theorems 2.5 and 2.13).

For a center simple `A`, write its forgetful row as `v(A)_i=[F(A):X_i]`. The source tensor determines

`B_ij = [I(X_i):I(X_j)] = sum_(k,l) N_(ki)^l N_(kj)^l = sum_A v(A)_i v(A)_j`.

Every center dimension `z=sum_i v_i d_i` lies in `K=Q(sqrt(r))`. The modular formal-codegree identity says `D^2/z^2` is an algebraic integer. Since `D/z` belongs to `K`, integral closure implies `D/z` is an algebraic integer. The unit `eta=D/48` therefore gives `48/z` integral. For `z=a+b sqrt(r)`, where the ring of integers is `Z[sqrt(r)]`, this is exactly

`a^2-rb^2 divides 48a and 48b`.

This divisibility, entrywise Gram bounds, and positivity give a finite exhaustive domain for every forgetful row.

## 2. Transporting the complete forgetful row

Normalize the center matrix by `S_00=1/D`. For every source character `chi_E`, the constituent `A_E` of `I(1)` is defined by

`chi_E(F(A)) = S_(A,A_E)/S_(0,A_E)`,  with `S_(0,A_E)=1/f_E`.

This is the definition immediately before Ostrik's Theorem 2.13, using Example 2.9. Modular Galois symmetry therefore gives

`chi_E(F(pi_sigma A)) = epsilon_sigma(A) (f_E/f_(sigma E)) chi_(sigma E)(F(A)).`  (1)

The integral multiplicity vector `m` of `I(1)` satisfies `Sm=m` by Ostrik's Proposition 2.8. Thus the signed Galois permutation fixes `m`; its support is preserved and its signs there are positive. In particular the Galois image of the central unit has a forced nonnegative forgetful row.

Choose `sigma` to flip `K` and fix all other source character values. This choice needs a character-field argument, not merely rational additional codegrees. The source matrix `M=sum_i w_i N_i`, for `w=(1,3,11,37,101,307,997)`, has respectively the characteristic polynomials

```
(x-1860)(x+66)(x+494)(x²-16448x-12738752)(x²-124x-171388),
(x-1314)(x-654)(x+1064)(x²-19656x+889872)(x²+1452x+527204),
(x-654)(x-184)(x+66)(x+234)(x+1852)(x²-15896x+12501688).
```

Their roots are distinct. The remaining character fields are `Q(sqrt(2))`, `Q(sqrt(-2))`, and `Q`, respectively: simultaneous one-dimensional eigenspaces are defined over their separating eigenvalue fields. These fields are disjoint from `K`, so the stated cyclotomic automorphism exists.

Put `a(v)=sum_i a_i v_i`, `b(v)=sum_i b_i v_i`, and let `bvec=(b_i)`. Character orthogonality and (1) yield the integral involution

```
r=3: T(v)=v+bvec*(4a(v)-7b(v))/4,
r=6: T(v)=v+bvec*(2a(v)-5b(v))/2.
```

Indeed the correction vanishes on all other characters, and evaluation on the two dimension characters gives exactly their codegree ratios in (1). Thus every actual row has Galois partner `T(v)` or `-T(v)`, with the sign chosen to make it nonnegative. A row with a mixed-sign image is impossible. Partner row types have equal multiplicities; involutivity is only needed on row types, not on the permutation of center simples.

For the central unit, this forces the following other `I(1)` row:

```
106:  (1,0,2,4,4,2,4),
2155: (1,2,2,0,4,4,4),
146:  (1,0,2,2,2,2,2).
```

Its dimension is `eta^2`. Enumerating the remaining five nonunit rows of `I(1)` by their known dimensions, their sum `B_(0,*)-e_0`, and the positive semidefinite residual Gram matrix leaves respectively 194,194,1323 blocks. This enumeration is entirely over nonnegative bounded integers and is reconstructed by the verifier.

## 3. Why the nonrational rows have restricted twists

Let `J=pi_sigma(1)` and `w=e_1-e_J` in the center's modular representation. All automorphisms fixing `K` fix the central unit: (1) with `A=1` and fixed codegrees forces its row to be `e_0`, which is the unique constituent of I(1) having formal codegree D, namely the central unit. Those flipping `K` send it to `J`. The diagonal torus therefore acts on `w` by the quadratic character of conductor `f=12` or `24`.

On the twist-one subspace spanned by the seven known constituents of `I(1)`, the compression of `S` sends

`w -> (eta^(-1)-eta)/48 * w = -w/sqrt(f)`.

To see this directly, the `1,J` block has diagonal entries `eta^(-1)/48` and off-diagonal entries `eta/48`; every other entry in the two columns agrees because its codegree is rational.

The local compression bound of Schopieray, *The dimension block of a spherical fusion category*, arXiv:2609.35287v1, Lemma 4.1, bounds the squared norm by `1/f`. We attain it already on the known twist-one block. The equality refinement proved in `CONDUCTOR_EQUALITY_LEMMA.md` shows the cyclic representation generated by `w` factors through level `f`. The accompanying quadratic Gauss-sum refinement, `QUADRATIC_RESIDUE_SATURATION.md`, shows its primitive twist exponents have quadratic character `-1`.

For a center simple of dimension `z`, its coordinate in `Sw` is

`z/D - sigma(z/D)`.

Therefore whenever `z/D` is nonrational, its twist has order dividing `f`; at a primitive `f`-th root, its exponent belongs to the negative quadratic-residue class. This conclusion is valid for the pseudo-unitary modular representation; no dagger structure on the original category is assumed.

Furthermore Galois symmetry sends twists to their `k^2`-th powers. Every unit `k` modulo 12 or 24 has square one. The nonrational partner rows from Section 2 consequently have the same twist, so their multiplicity counts agree separately for each twist. Rows with rational `z/D` are fixed by `T` and need no twist pairing constraint.

## 4. A finite hull for two moments of arbitrary roots

Let `t(theta)` denote normalized relative trace to `K`. In the four coefficient coordinates representing `(t(theta),t(theta^2))`, every root of unity, of any order, lies in the convex hull of these nine vectors:

```
(1,0,1,0), (-1,0,1,0),
(1/2,0,-1/2,0), (-1/2,0,-1/2,0), (0,0,-1,0),
(0,h,s,0), (0,-h,s,0), (0,0,0,h), (0,0,0,-h),
```

where `(h,s)=(1/2,1/2)` for `r=3` and `(1/4,0)` for `r=6`. The complete elementary root-order proof is included in `QUADRATIC_TWO_MOMENT_HULL.md`. Briefly, rational moments are Ramanujan sums, while a nonzero irrational first moment requires root order `f*m`, with `m` squarefree and coprime to 6. The induced quadratic Gauss sum scales the primitive moment by `mu(m)chi_f(m)/phi(m)`; for `m>1`, `phi(m)>=4`, which places it in the stated hull. Nonzero irrational second moments with zero first moment lie on the segment from the primitive `2f` roots.

For a nonrational dimension ratio, Section 3 restricts this to the first five vectors and `(0,-h,s,0)`. We use the six-vertex hull on such rows and the nine-vertex hull on every other row. This imposes no unproved global bound on root orders.

## 5. Pivotal signs and the two trace identities

For arbitrary `X` and self-dual `Y`, every self-dual simple of odd multiplicity in `X Y X*` has the same second Frobenius–Schur indicator as `Y`. One obtains the requisite nondegenerate form using

`j_X tensor f_Y tensor id_(X*)`,

whose pivotal transpose has sign `nu_2(Y)`. On an odd-dimensional multiplicity space an alternating nondegenerate form is impossible. Likewise a self-dual `X` supplies a form of sign `nu_2(X)` on `X^3`, since this tensor word is palindromic; no braiding is used. These forms, already audited in `PIVOTAL_ODD_ISOTYPIC_LEMMA.md`, give exactly the following possible indicator vectors in source order:

```
106:  (1,1,e,1,1,e,1), e=+1 or -1;
2155: (1,0,0,1,1,1,1);
146:  (1,1,1,1,1,1,e), e=+1 or -1.
```

The verifier derives the constraints from the source tensor rather than trusting these lists.

For a nonunit source simple `X_i`, induction satisfies

`Tr(theta on I(X_i))=0`,
`Tr(theta^2 on I(X_i))=D nu_2(X_i)`.

The first is Ostrik's Theorem 2.5; the second is Ng–Schauenburg's indicator trace formula, also used in Ostrik's Theorem 2.7. Subtract from both the known twist-one `I(1)` constituents. Taking relative traces to `K` gives twelve rational equations from each identity. Together with the 21 lower-triangular residual Gram entries, these form 45 integer equations after multiplication by four.

More explicitly, for a paired orbit of allowable nonunit rows `(v,z)` (one row for a fixed orbit, two otherwise), and a moment vertex `(a,b,c,d)`, its column is

```
4 sum_v vech(v v^t),
4 sum_(v,z) (v_i * z*(a+b sqrt(r)))_(i=1..6),
4 sum_(v,z) (v_i * z*(c+d sqrt(r)))_(i=1..6),
```

where the last two blocks are expanded in the coefficient basis `1,sqrt(r)`. Each column has a nonnegative real multiplicity weight: actual twist multiplicities give such weights after convex decomposition. Partner rows use the same moment vertex, as proved in Section 3.

## 6. Four universal inequalities finish the proof

For each residual Gram matrix `R`, allowable rows must satisfy `vv^t <= R` as positive semidefinite matrices. The verifier checks this exactly, including singular residuals, by a principal inverse together with the range equations. It also checks entrywise bounds and the arithmetic dimension condition from Section 1.

After row pairing, some blocks are immediately impossible modulo a small prime: the vector `vech(R)` does not belong to the span of the paired Gram columns. This excludes 21,21,235 blocks, respectively. The remaining blocks are treated by only FOUR universal covectors `y` in `Z^45`, explicitly stored in `quadratic_center_trace_certificate.json`:

- one covector for every R106 block and both indicator signs;
- one covector for every R2155 block;
- one covector for every R146 block with each of the two indicator signs.

For every allowed column `c`, the verifier establishes `y.c >= 0`, whereas for the prescribed target `b` it establishes `y.b < 0`. A nonnegative combination of columns cannot equal `b`. The same fixed covectors work throughout their stated families, so no numerical solver or per-branch certificate is part of the proof.

| Ring | Complete low blocks | Modular exclusions | Remaining blocks | Trace systems | Universal covectors |
|---|---:|---:|---:|---:|---:|
| R7_4_106 | 194 | 21 | 173 | 346 | 1 |
| R7_4_2155 | 194 | 21 | 173 | 173 | 1 |
| R7_3_146 | 1323 | 235 | 1088 | 2176 | 2 |

Every hypothetical center supplies one enumerated low block, allowable paired residual rows, an allowed indicator choice, and nonnegative moment weights. Every such possibility contradicts either the exact modular span or one of the four integer inequalities. Hence no pseudo-unitary categorification exists. The initial Galois reduction proves the stated exclusion over all complex fusion categories.

## Reproduction and source binding

Run `python verify_quadratic_center_trace.py --repo PATH_TO_REPOSITORY`. The verifier uses only the Python standard library; it reads the original compressed rank-seven census, re-identifies the three IDs by multiplicity and ordinal, checks their immutable tensor hashes, and reconstructs all finite domains. No saved list of candidate rows, branch assignments, floating-point feasibility claim, associator search, or optimizer is trusted.

The categorical premises have independent primary-source audits in `QUADRATIC_CENTER_TRACE_CATEGORICAL_AUDIT.md` and `GALOIS_FORGETFUL_ROW_LEMMA.md`; the finite hull and conductor refinements are reproduced alongside this proof. The general-to-pseudo-unitary theorem is the separately source-bound prior result in `rank7/THREE_CASE_GALOIS_PU.md` and `rank7/verify_three_case_galois_pu.py`.

Primary sources: Ostrik, https://arxiv.org/abs/1309.4822, Sections 2.2–2.3; Schopieray, https://arxiv.org/abs/2609.35287, Lemma 4.1 and its finite modular-representation setting; Ng–Schauenburg, *Frobenius–Schur indicators and exponents of spherical categories*, Theorem 4.1 as cited by Ostrik; standard modular Galois symmetry and congruence for Drinfeld centers. The exact refinements used here are stated and proved in the accompanying notes, rather than attributed to a stronger theorem in those sources.
