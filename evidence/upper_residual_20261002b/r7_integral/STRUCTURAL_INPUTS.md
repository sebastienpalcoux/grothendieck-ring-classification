# Structural inputs and scope

Every conclusion here excludes categorification by an arbitrary fusion category
over the complex numbers. The input fusion rings are integral. No braiding or
choice of pivotal structure is assumed.

The following standard results are used, with their hypotheses retained.

* Etingof–Nikshych–Ostrik, [arXiv:0809.3031](https://arxiv.org/abs/0809.3031),
  Definition 1.2 and Proposition 4.4: a solvable category is obtained through
  successive prime cyclic extensions or equivariantizations. Theorem 1.6:
  dimension with at most two prime divisors implies solvability. Theorem 1.5:
  dimensions of simples in a weakly group-theoretical fusion category divide
  its global FP dimension. Theorem 9.2: an **integral** category of dimension
  a product of three distinct primes is group-theoretical.
* Burciu–Natale, [arXiv:1206.6625](https://arxiv.org/abs/1206.6625),
  Corollary 2.13: equivariant simples are labelled by an orbit and an
  irreducible projective stabilizer representation; their FP dimensions are
  orbit size times representation degree times the underlying simple dimension.
* ENO, [arXiv:0909.3140](https://arxiv.org/abs/0909.3140), Theorem 1.1 and
  Corollary 1.2: an invertible pointed bimodule is represented by an isometry
  of the hyperbolic metric group (A\oplus\widehat A); in particular
  (\operatorname{BrPic}(\mathrm{Vec}_A)=O(A\oplus\widehat A)).
* ENO, [arXiv:math/0203060](https://arxiv.org/abs/math/0203060), Corollary 8.30:
  a fusion category of prime FP dimension is pointed. We also use the
  divisibility of FP dimensions of fusion subcategories.
* DGNO, [arXiv:0906.0620](https://arxiv.org/abs/0906.0620), Section 4.2,
  Theorem 4.18 and Proposition 4.19: a central Tannakian subcategory with
  faithful forgetful restriction admits inverse equivariantization and
  de-equivariantization constructions.

Two elementary consequences are useful throughout. First,

\[
\operatorname{Aut}_\otimes(\mathrm{Id}_{\mathcal D})
 =\operatorname{Hom}(U(\mathcal D),\mathbb C^\times).
\]

The ratio of two central structures on the same invertible object is such an
automorphism. Thus, when (U(\mathcal D)=1), an underlying invertible has at
most one central lift. If the entire invertible subgroup is the underlying
canonical (\operatorname{Rep}(K)) in a (K)-equivariantization, every outer
tensor action preserves it, including its central structure and symmetry.
Taking equivariant objects in this preserved central subcategory gives a
central Tannakian (\operatorname{Rep}(H)), where

\[
1\longrightarrow K\longrightarrow H\longrightarrow Q\longrightarrow1.
\]

Its restriction to the outer equivariantization is fully faithful: the
underlying inclusion before equivariantization was fully faithful and the
same equivariance equations define both Hom spaces. De-equivariantizing this
larger Tannakian subcategory identifies the original category with an

\(H\)-equivariantization of the category obtained after the two steps. This
retains arbitrary action coherence, rather than replacing the extension by
a guessed semidirect product.

Second, distinct components of a faithful grading cannot be equivalent as
left modules over the neutral category unless the quotient component has
the regular left-module type. More precisely, for invertible bimodules

\(M,N\), a left-module equivalence (M\simeq N) transports the right action
on (N) to (M); their relative quotient is then the regular bimodule with
one right action twisted by a tensor autoequivalence. In a grading,

\(M_a^{-1}\boxtimes_{\mathcal D}M_b\simeq M_{a^{-1}b}\).
If every nonneutral component has rank one and the regular neutral module
has rank greater than one, the rank-one components are therefore pairwise
inequivalent as left modules.

The exact verifier checks the full source tensors and the finite group
calculations used below. It verifies these algebraic premises, not the cited
fusion-category theorems. No output labelled PASS is a claim that category
theory was formally proved by the program.
