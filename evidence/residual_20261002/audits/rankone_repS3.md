# Rank-one component obstruction over a Rep(S3) fusion ring

Independent audit, 2026-10-02. This excludes general fusion categorification over
the complex field; no pivotal, spherical, pseudo-unitary, or unitary hypothesis is
used.

## Criterion and proof

There is no faithfully group-graded complex fusion category whose neutral
component has the Rep(S3) fusion ring and which has a homogeneous component with
exactly one simple object.

Suppose such a category exists and write its neutral component as D and a
rank-one component as M. As a finite semisimple complex linear category, M is
equivalent to Vec. Its D-action defines a strong tensor functor
F: D -> End(Vec) = Vec. This is exact and faithful: a nonzero object cannot act
by zero because its dual product contains the tensor unit, and morphism
faithfulness then follows by semisimplicity. Thus F is a fiber functor.

Tensor reconstruction gives D = Rep(H) for a finite-dimensional semisimple Hopf
algebra H. The Rep(S3) fusion ring has simple dimensions 1, 1, 2, so dim(H)=6.
The semisimple dimension-pq theorem says that H is a group algebra or its dual.
The groups of order 6 are C6 and S3. Only H = C[S3] has three irreducible
modules; C[C6] and both function algebras have six. Therefore H = C[S3].

The dual category End_D(M), for precisely this reconstructed fiber functor, is
Rep(H*) = Vec_S3 and has rank 6. In a faithful grading, every homogeneous
component is an invertible D-bimodule category. Invertibility would imply that
the right action identifies D with End_D(M), up to the harmless opposite-tensor
convention. That is impossible because D has rank 3. This proves the criterion.

## Exact census applications

`audit_rankone_repS3.py` independently reads the rank-8 census tensors, compares
their canonical SHA-256 values against the repository decisions, verifies the
complete support grading, checks the neutral multiplication, and checks the
rank-one actions. Its machine-readable output is `rankone_repS3_audit.json`.
Indices below use the original census basis, with tensor unit 0.

| Ring | Components | Neutral basis (1,g,x) | Rank-one components |
|---|---|---|---|
| R8_2_78 | {0,5,7}, {1,2,6}, {3}, {4} | (0,7,5) | {3}, {4} |
| R8_2_168 | {0,3,4}, {1}, {2}, {5,6,7} | (0,3,4) | {1}, {2} |

In both cases the neutral ring satisfies g^2=1, gx=x, x^2=1+g+x, and the
component group is C4. The criterion excludes both rings.

Tensor SHA-256:

- R8_2_78: `57cc7c0c281f0ba6b2ca92417f11e2fa73df6a188e64459a1e50d49b780c36b3`
- R8_2_168: `39014e9a825d42c9eb0fdf92158702b1a5e19f4bafd8d12b989e9fc52f56f7ba`

## Primary sources

- P. Etingof and S. Gelaki, *Semisimple Hopf algebras of dimension pq are
  trivial*, arXiv:math/9801129, https://arxiv.org/pdf/math/9801129. The theorem is
  over an algebraically closed field of characteristic zero. The special
  dimension-6 result also appears in A. Masuoka, *Semisimple Hopf algebras of
  dimension 6, 8*, Israel J. Math. 92 (1995), 361–373,
  https://doi.org/10.1007/BF02762089.
- P. Etingof, S. Gelaki, D. Nikshych and V. Ostrik, *Tensor Categories*,
  Sections 5.2–5.3 (reconstruction) and Example 7.12.26 (the fiber-functor module
  has dual Rep(H*)), https://math.mit.edu/~etingof/egnobookfinal.pdf.
- P. Etingof, D. Nikshych and V. Ostrik, *Fusion categories and homotopy theory*,
  Quantum Topol. 1 (2010), 209–273, Theorem 6.1 (homogeneous components are
  invertible) and Proposition 4.2 (dual-category characterization of
  invertibility), https://arxiv.org/pdf/0909.3140.
