# R315 and R317: incompatible intrinsic pointed associators

**Conclusion.** Neither ring admits a fusion category over the complex field.
The argument uses two rank-four subcategories separately. It does not require
simultaneous Galois conjugation of the ambient category.

## 1. The two rank-four rings

Write their bases as `1,g,x,y`, with `g^2=1`, `gx=y`, and `gy=x`.
Their noninvertible FP dimensions are `d=1+sqrt(2)`.

The ordinary PSU(2)_6 ring has

    x^2=y^2=1+x+y,    xy=g+x+y,    x*=x, y*=y.

The pseudo-PSU(2)_6 ring instead has

    x^2=y^2=g+x+y,    xy=1+x+y,    x*=y.

The source-bound verifier finds the following closed subrings with a common g:

| Ring | Ordinary basis map | Pseudo basis map | Common g |
| --- | --- | --- | --- |
| R8_2_315 | [0,7,3,4] | [0,7,1,2] | 7 |
| R8_2_317 | [0,7,5,6] | [0,7,1,2] | 7 |

Swapping the two noninvertible basis labels gives equivalent witnesses.
All 64 coefficients and closure are checked against the original census.

## 2. The ordinary ring forces a trivial pointed class in the PU case

Suppose an ordinary PSU(2)_6 category is pseudo-unitary, equipped with its
canonical spherical structure. FRS odd-multiplicity parity gives
`nu_2(x)=nu_2(y)=+1`, since both simples occur with odd multiplicity in
`x*x`. Assume for contradiction that `nu_2(g)=-1`.

An exact induction/indicator certificate excludes this sole indicator choice.
It is replayed by `verify_psu_pointed.py`, which invokes the existing
`balanced_traces.py` engine with height four. It uses only exact arithmetic;
it does not invoke an optimization solver. The complete low-column counts
are `[3,2,2]`, giving precisely these three low restriction matrices, displayed
as column lists:

    [(1,0,0,0),(1,0,0,2),(1,0,1,0),(1,0,1,0)]
    [(1,0,0,0),(1,0,1,1),(1,0,0,1),(1,0,1,0)]
    [(1,0,0,0),(1,0,2,0),(1,0,0,1),(1,0,0,1)]

For each branch the necessary center data satisfy `A n=b` with `n>=0`.
The stored integer separating vector `v` satisfies `v^t A>=0`, whereas
`v^t b` is respectively `-48,-12,-48`. This is a contradiction in each
branch. Each system has 38 integer equations. The systems have respectively
102, 152, and 102 variables, including nonnegative slack variables.

For precision, the necessary conditions in these systems are:

1. Frobenius reciprocity for induction, `A A^t=C`, with `C` the exact
   induction matrix of the ring. The low columns are obtained from the
   complete list of formal codegrees and have trivial twist. All remaining
   restriction columns have first coordinate zero and lie in the residual
   positive-semidefinite Gram matrix.
2. The center indicator identity
   `sum_Z [F(Z):X] dim(Z) theta_Z^j = dim(C) nu_j(X)`,
   for `j=1,2,3,4`. Here `nu_1(X)=0` for every nonunit simple, and the
   second indicators are `(-1,1,1)`. A higher indicator is the trace of an
   operator of order j on `Hom(1,X^j)`. Its rational cyclotomic average
   therefore has the elementary upper and lower bounds used in the engine.
3. The Cauchy theorem for spherical fusion categories restricts the primes
   in twist orders to the primes in the absolute norm of
   `dim(C)=8+4sqrt(2)`, whose norm is 32. Thus the twists have 2-power order.
   All joint relative traces through height four to `Q(sqrt(2))` are covered
   by ten trace vectors. The finite divisor box is 32; any larger 2-power
   order has the zero trace vector through this height, which is explicitly
   included. This is a finite trace classification, not an exponent bound.
4. Center simple dimensions are d-numbers and `dim(C)/dim(Z)` is integral.
   These impose the exact algebraic-integer tests used to enumerate all
   possible high columns; they do not remove an admissible center simple.
5. Galois symmetry of the normalized center S matrix permutes its simple
   dimensions according to
   `z -> abs(dim(C) z' / dim(C)')`.
   This follows by applying the nontrivial automorphism of `Q(sqrt(2))`
   to the first row `z/dim(C)` of the normalized S matrix. Consequently
   the total number of simples of dimension z equals the number of the
   paired dimension. These are the two additional Galois balance equations.

The normal and Python `-O` receipts record the same three integer systems,
the same separating products, and complete source witnesses. Optimization
is used neither to discover nor to verify this published certificate.
Hence every pseudo-unitary ordinary PSU(2)_6 categorification has
`nu_2(g)=+1`.

For a pseudo-unitary pointed C2 subcategory, with a normalized associator,
`nu_2(g)=omega(g,g,g)`. This scalar is +1 for the trivial H^3(C2,C*) class
and -1 for the nontrivial class. Thus the ordinary ring forces the trivial
pointed class in every pseudo-unitary categorification.

## 3. Galois passage makes both pointed constraints general

Schopieray's **published** Lemma 3.1 says that every categorification of a
two-dimension fusion ring is Galois conjugate to a pseudo-unitary one.
Both rank-four rings above have just the two FP dimensions 1 and d.

The two classes of `H^3(C2,C*)` have normalized representatives with
`omega(g,g,g)=+1` and `-1`. These classes are fixed separately by every
field automorphism. Consequently the ordinary ring forces the trivial
pointed class in **every** complex categorification, not only a
pseudo-unitary one.

For the pseudo ring, Larson's Proposition 5.5 and Theorem 5.8, Case 1,
force `nu_2(g)=-1` in the pseudo-unitary case. Its excluded positive sign
would require eight roots of unity from a set with only seven elements.
The same Galois argument therefore forces the nontrivial pointed class in
every complex categorification. See `R312_GENERAL_PROOF.md` for the full
statement and hypothesis audit of this side of the argument.

If either census ring had a complex categorification, its two rank-four
fusion subcategories would restrict the **same ambient associator** to
the same pointed subcategory generated by g. One restriction would have
trivial H^3 class and the other nontrivial class. This is impossible.

## Primary references and exact reproducibility

- A. Schopieray, *Categorification of integral group rings extended by one
  dimension*, J. London Math. Soc. 108 (2023), DOI 10.1112/jlms.12789,
  published Lemma 3.1.
- H. K. Larson, https://arxiv.org/pdf/1401.1879, Proposition 5.5 and
  Theorem 5.8, Case 1(c)(1).
- S.-H. Ng and P. Schauenburg, https://arxiv.org/pdf/math/0601012,
  the center indicator identity and order-j pivotal rotation.
- P. Bruillard, S.-H. Ng, E. C. Rowell and Z. Wang, *Rank-finiteness for
  modular categories*, the Cauchy theorem for spherical fusion categories.
- V. Ostrik, *On formal codegrees of fusion categories*, the d-number
  theorem, applied to the modular center.
- S.-H. Ng and P. Schauenburg, *Congruence subgroups and generalized
  Frobenius-Schur indicators*, Galois symmetry of normalized modular data.
- Fuchs--Runkel--Schweigert odd-multiplicity parity, in the precise pivotal
  form of https://arxiv.org/pdf/2203.06522, Theorem 3.9.

Run from any directory:

    python3 verify_psu_pointed.py --output psu_pointed_normal.json
    python3 -O verify_psu_pointed.py --output psu_pointed_optimized.json

No numerical search or explicit modular S/T reconstruction is required.
