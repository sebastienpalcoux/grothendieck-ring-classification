# Independent audit of the three prime-descent exclusions

**Verdict: approved in general complex fusion-category scope.**

The proofs in `phase2/weak_integral/frobenius52.md` and
`phase2/integral_theory/prime_descent.md` establish the exclusions of
`R9_2_1071`, `R9_2_1724`, and `R9_2_907`, respectively. No unproved assertion
that every weakly integral category is weakly group-theoretical is used.
The statements also require no braiding, pivotality, sphericality, or
unitarity of the hypothetical input category.

## Published inputs checked

I checked the actual statements in the primary sources:

* ENO, *Weakly group-theoretical and solvable fusion categories*,
  [arXiv:0809.3031v2](https://arxiv.org/html/0809.3031v2): Theorem 1.6 applies
  unconditionally to FP dimension involving only two primes; Theorem 9.2
  applies to **integral** categories of dimension the product of three
  distinct primes. Proposition 4.4 provides cyclic-prime extension/
  equivariantization chains. Proposition 4.5(i),(ii) supplies Morita
  invariance of solvability and solvability of pointed categories over
  solvable groups. Theorem 9.2 is the needed integrality-sensitive statement,
  rather than a conjecture about all weakly integral categories.
* DGNO, *On braided fusion categories I*,
  [arXiv:0906.0620v3](https://arxiv.org/html/0906.0620v3), Theorem 4.18,
  Proposition 4.19 and Remark 4.21: central fully faithful `Rep(K)` embeddings
  give fusion de-equivariantizations, inverse to group equivariantization.
  The nonbraided tensor-category form is the one needed here.
* Burciu--Natale, *Fusion rules of equivariantizations of fusion categories*,
  [arXiv:1206.6625v2](https://arxiv.org/html/1206.6625v2), Section 2: simple
  equivariant objects are described by object orbits and projective
  stabilizer representations. Cyclic stabilizers have trivial complex
  Schur multiplier in the cases used here.
* ENO, *Fusion categories and homotopy theory*,
  [arXiv:0909.3140](https://arxiv.org/pdf/0909.3140), Section 6: the components
  of a faithful fusion-category grading are invertible bimodule categories.
* Ostrik, *Module categories, weak Hopf algebras and modular invariants*,
  [arXiv:math/0111139](https://arxiv.org/pdf/math/0111139): indecomposable
  module categories over a finite-group representation category arise from
  subgroup projective-representation categories. The associated dual is the
  usual group-theoretical category, with the double-coset description used
  in the dimension-52 proof.

## The common central-subcategory step

This is the most delicate step, and it is valid in the form used.

For any fusion category `E`, a central structure on the tensor unit is exactly
a tensor automorphism of the identity functor. If `U(E)=1`, this group is
trivial. Two central invertible objects with isomorphic underlying objects
differ by such a structure on the unit; consequently each invertible of `E`
has at most one central lift. The inner canonical `Rep(Cq)` in `Z(E)` is
therefore preserved by the outer action: that action permutes its underlying
invertibles, which exhaust `Inv(E)` in these applications.

Its equivariantization is a symmetric category, because the induced action
on the center is braided. It has a symmetric fiber functor obtained by
forgetting equivariance and then using `Rep(Cq) -> Vec`. Hence it is
Tannakian, not merely super-Tannakian. Its central functor into the outer
equivariantization is fully faithful: the original central subcategory is
full after forgetting to `E`, and the morphism-equivariance condition is the
same on both sides. Thus one obtains an honest central `Rep(K)` to which
fusion de-equivariantization applies. The usual subgroup/quotient
correspondence for this Tannakian exact sequence justifies de-equivariantizing
in stages and identifying the restriction of the `K` action with the earlier
inner action. No arbitrary central lift or unidentified super sign has been
silently chosen.

## Dimension 104: R9_2_1071 and R9_2_1724

The neutral dimension is `52=4*13`, so solvability follows from ENO Theorem
1.6. Its trivial universal grading forces the last step to be a C2
equivariantization. The invertible action gives the stated intermediate
type `(1^2,2^6)`, of dimension 26 and rank 8. A nontrivial universal grading
there would have order two and a prime-dimension neutral part of rank 13,
contradicting rank 8. The second descent to a pointed category of dimension
13 is therefore justified.

The common central argument gives `K=C4`: the equivariantized central
subcategory has dimension four and its four invertibles exhaust the
specified cyclic group of invertibles. The order-four action on C13 must be
faithful, because a kernel would bound nontrivial object-orbit sizes by two;
cyclic stabilizers then cannot yield the dimension-four simples.

The cohomology conclusions are also correct. The order-four automorphism
acts as multiplication by `-1` on `H^3(C13,C*)`; thus an invariant associator
class vanishes. Tensor automorphism functors have no remaining `H^2(C13,C*)`
ambiguity, and action coherence has no `H^2(C4, C13-hat)` ambiguity by
coprimality. Hence the category is indeed tensor equivalent to the indicated
ordinary representation category, not merely Grothendieck-ring equivalent or
Morita equivalent to it.

For each subgroup of `C13 semidirect C4`, the Schur multiplier vanishes.
For a subgroup containing C13 this follows from the total-degree-two terms
of the Lyndon--Hochschild--Serre spectral sequence: the two cyclic H2 terms
are zero and the remaining H1 term vanishes by coprimality. Subgroups not
containing C13 are cyclic. Thus no twisted projective module category was
missed. The only rank-two possibility is the C2 subgroup module category.
Its dual has four invertibles and twelve dimension-two simples, hence rank
16, whereas an invertible bimodule would have dual rank 7. This is a genuine
contradiction.

## Dimension 222: R9_2_907

Its dimensions are integral, so ENO Theorem 9.2 applies at `222=2*3*37`.
The Morita-equivalent pointed group has order 222 and is solvable: its
Sylow-37 subgroup is normal and its quotient has order six. Therefore the
input category is solvable, by the cited closure results. The proof does not
assume solvability of a group-theoretical category without checking its
pointed group.

The subsequent dimension and adjoint-subcategory arguments are exact. In
the dimension-111 intermediate category, a dimension-three simple has all
three invertibles in `XX*`, since `9=|Stab(X)|+3m`. Its adjoint subcategory
contains those invertibles and a dimension-three simple. Its possible
dimension has form `3+9k`; none of the proper divisors `1,3,37` is possible.
Thus the second equivariantization descent is justified.

The outer involution inverts the three intermediate invertibles. The common
central argument therefore gives `K=S3`, not C6. Its normal C3 would have to
act nontrivially on the pointed C37 category, but any induced homomorphism
`S3 -> Aut(C37)` annihilates C3 because the target is abelian. This contradicts
the inner free orbits of length three. The contradiction does not depend on
the pointed associator.

## Independent finite checks

`audit_theoretical.py` independently checks all tensor dimension equations,
the two C2 gradings, neutral adjoint generation and invertible action, and the
dimension-222 hypotheses. For the dimension-104 cases the computation uses
exact pairs in `Z[sqrt(26)]`, not approximations. It independently enumerates
the 30 subgroups of the order-52 group and recomputes the dual double-coset
dimension type for **all thirteen** C2 subgroups. All checks pass, as recorded
in `audit.json`. These finite checks verify the hypotheses and group counts;
the categorical deductions above are the theoretical proof audit.
