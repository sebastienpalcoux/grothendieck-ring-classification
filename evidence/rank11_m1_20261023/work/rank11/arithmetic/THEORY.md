# Exact arithmetic audit for the rank-eleven multiplicity-one census

All 182 physical input lines are retained as `R11_1_1` through `R11_1_182`.
The tensor hash is SHA-256 of compact JSON in the original basis. An arithmetic
pass means only that the stated necessary condition holds. It is never a
categorification or an existence assertion.

## Results

`arithmetic.json` contains 182 records and excludes 97 inputs over the complex
numbers. Individual criteria overlap: the Casimir d-number test excludes 86,
the commutative matrix cyclotomic test 33, integral commutative Drinfeld
divisibility 13, its noncommutative block-multiplicity test 2, generalized
near-group divisibility 2, nonabelian Tambara–Yamagami 1, the small near-group
multiplicity condition 1, and the primitive-codegree condition 5.

`subring_indices.json` checks all 919 proper nontrivial based subrings of the
182 inputs. There are 162 nonintegral-index certificates, on 69 inputs; these
inputs were already excluded by the preceding arithmetic inventory.

`cyclotomic_complete.json` makes a complete decision for 286 distinct
irreducible polynomials. Of these, 169 have degree at most two, 48 have an
explicit complete set of commuting root substitutions, and 69 have a
nonuniform squarefree Frobenius-cycle witness. The complete criterion excludes
41 inputs: 33 commutative and 8 noncommutative. All are among the 97 arithmetic
exclusions. No bounded prime search is interpreted as an affirmative result.

`noncomm_codegrees.json` computes every irreducible representation degree and
formal codegree for all 29 noncommutative input algebras. Its 16 negative cases
are also already covered by the initial arithmetic inventory.

## Casimir and formal codegrees

For the fusion matrices in their supplied convention, put
\(C=\sum_i N_iN_i^T\). In a simple algebra representation of dimension \(e\),
the corresponding Casimir eigenvalue is \(ef_E\), where \(f_E\) is its formal
codegree. Multiplication by a nonzero rational integer does not change the
d-number property. Thus the d-number test on every irreducible factor of the
characteristic polynomial of \(C\) is valid also for noncommutative rings.
The explicit divisibility condition is
\(a_d^j\mid a_j^d\) for the coefficients of a monic irreducible degree-\(d\)
polynomial. The certificates record a nonzero integer remainder.

An integral fusion category is pseudo-unitary, and its center is integral:
forgetting a central simple object expresses its FP dimension as a sum of
integer simple dimensions. Consequently every formal codegree is a positive
integer dividing the global FP dimension. When a rational Casimir eigenvalue
\(\lambda\) has regular multiplicity \(m\), the admissible representation
degrees satisfy \(e^2\le m\), \(e\mid\lambda\), and
\(\lambda/e\mid D\). The multiplicity must be a sum of their squares. This
necessary partition test does not assume that a Casimir eigenvalue belongs to
only one irreducible representation.

For the full noncommutative calculation, a separating central element \(H\)
is constructed as below. Expressing \(C\) as a rational polynomial in \(H\)
gives its scalar on each simple block. A factor with regular multiplicity
\(e^2\) then yields the exact value \(f_E=C(H)/e\). The replay verifies the
matrix polynomial identity and that the sum of all block dimensions is 11.

Ostrik, *On formal codegrees of fusion categories*,
[arXiv:0810.3242v2](https://arxiv.org/html/0810.3242v2), Theorem 1.2,
Lemma 2.6, Lemma 2.7, and Corollary 2.8 supply these formal-codegree facts.
For the center-divisibility theorem and its hypothesis, see Ostrik's
*Pivotal fusion categories of rank 3*, Theorem 2.13 and Corollary 2.14, as
also stated in Liu–Palcoux–Ren Theorems 2.3 and 2.4.

## Complete character-trace cyclotomicity, including noncommutative rings

The known theorem is cyclotomicity of irreducible **character traces**. We do
not assume cyclotomicity of arbitrary matrix eigenvalues in a noncommutative
fusion algebra. The following finite reduction applies that theorem exactly.

Let \(A=R\otimes\mathbb Q\), and compute its center by the rational equations
\([z,b_i]=0\). Let \(c=\dim Z(A)\). A rational linear combination \(h\) of
the center basis is chosen until left multiplication \(H\) has precisely
\(c\) distinct eigenvalues. This condition proves that \(h\) separates every
simple block after extension to \(\overline{\mathbb Q}\). The search is finite:
using coefficients \(1,k,k^2,\ldots\), each pair of distinct central characters
can collide for at most \(c-1\) values of \(k\).

Fix an irreducible representation \(E\) of dimension \(e\), with central
scalar \(\alpha\). Write \(p\) for the squarefree characteristic polynomial
of \(H\). Its primitive central projector is

\[
 P_E=\frac{p(H)/(H-\alpha)}{p'(\alpha)},
\]

where the quotient denotes polynomial division before substitution. Therefore
\(P_E\) has entries in \(\mathbb Q(\alpha)\). Since the regular block is
\(E^{\oplus e}\),
\[
 \chi_E(b_i)=\operatorname{Tr}(P_EN_i)/e\in\mathbb Q(\alpha).
\]
Conversely, if \(h=\sum_i h_i b_i\), then
\(e\alpha=\sum_i h_i\chi_E(b_i)\). Hence the field generated by all the
character values of \(E\) is exactly \(\mathbb Q(\alpha)\). This proves that
testing every irreducible factor of the separating central characteristic
polynomial tests the full character-trace cyclotomicity theorem. The software
also checks that every regular block multiplicity is a square.

An irreducible polynomial defines a cyclotomic subfield exactly when its root
field is Galois and abelian. Negative certificates give a prime where the
squarefree modular factor degrees differ; a Frobenius element then has
nonuniform cycle lengths, impossible for the regular action of an abelian
Galois group. Positive certificates provide all distinct roots as rational
polynomials in one root, verify each root equation, and verify every pair of
substitutions commutes. The full root list proves normality and completeness
of the automorphism list. The compositum of the resulting abelian fields is
abelian. The degree-one and degree-two cases are elementary.

The character-trace theorem is Etingof–Nikshych–Ostrik,
*On fusion categories*, Theorem 8.51. Its precise formulation is recalled in
Ostrik [arXiv:0810.3242v2](https://arxiv.org/html/0810.3242v2), paragraph after
Example 1.6. The commutative specialization is Liu–Palcoux–Ren,
[arXiv:2010.10264v5](https://arxiv.org/html/2010.10264v5), Theorem 2.11.
The central-element algorithm is a finite implementation of that known
theorem; no claim that the mathematical observation is new in the literature
is made.

## Every subring index without a commutativity assumption

Put \(A=\sum_iN_i\). Every entry is strictly positive by Frobenius
reciprocity and nonzero fusion products. Its Perron eigenvalue is simple.
The maximal real root is identified using exact rational isolating intervals,
and its irreducible polynomial defines the field in which an eigenvector is
solved with unit coordinate equal to one. Every coordinate is certified
positive by interval refinement, and every fusion-product identity is then
checked in the number field. This proves that the vector is the FP dimension
character, independently of any approximate profile.

All subsets closed under the unit, duality, and multiplication are enumerated.
For each proper nontrivial subring \(S\), the quotient
\(q=\sum_i d_i^2/\sum_{i\in S}d_i^2\) is constructed exactly. The characteristic
polynomial of multiplication by \(q\) on the FP field has integer
coefficients exactly when \(q\) is an algebraic integer. Any noninteger
coefficient provides the recorded obstruction. The unit subring is omitted
because its index is the FP dimension itself, already an algebraic integer;
the full subring has index one.

The theorem that subcategory FP-dimension indices are algebraic integers is
Etingof–Gelaki–Nikshych–Ostrik, *Tensor Categories*, Theorem 7.17.6; its use here
is exactly Liu–Palcoux–Ren Theorem 2.13. The polynomial and interval steps only
implement this known theorem and make its hypotheses explicit.

## Other arithmetic scopes

The near-group and generalized near-group exclusions use Schopieray,
*Categorification of integral group rings extended by one dimension*,
[doi:10.1112/jlms.12789](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12789),
Propositions 3.2 and 3.3. Proposition 3.2 requires commutativity; Proposition
3.3 does not. The tests verify transitivity on noninvertible objects before
forming the stabilizer and the quadratic dimension relation. The nonabelian
Tambara–Yamagami obstruction is the usual abelian-group requirement in the
Tambara–Yamagami classification, equivalently Liptrap Corollary 4.10.

Schopieray, *Norm, trace, and formal codegrees*,
[arXiv:2005.13760v1](https://arxiv.org/html/2005.13760v1), Corollary 4.3 and
Theorem 4.4, applies to **general** complex fusion categories: a formal codegree
with no nontrivial rational integer divisor forces rank equal to its field
degree, all codegrees in its Galois orbit, and commutativity. Norm prime
exponents smaller than the degree certify that hypothesis. This is distinct
from the spherical-only results in Section 4.2 of that paper. In particular,
the squarefree-norm classification there is not silently used for arbitrary
categories.

## Replay

From the workspace or portable package root:

```bash
python work/rank11/arithmetic/run.py --verify-only
python work/rank11/arithmetic/subring_indices.py --verify-only
python work/rank11/arithmetic/cyclotomic_complete.py --verify-only
python work/rank11/arithmetic/noncomm_codegrees.py --verify-only
```

The arithmetic primitives previously used in ranks nine and ten are vendored
byte-for-byte under `legacy/`; `legacy_sources.json` records their source paths
and hashes. New entry points use explicit checks rather than Python assertions.
The common input reader and tensor utilities are in `../common.py`. Every
listed JSON file can be regenerated by omitting `--verify-only`.
