# The Galois-unit restriction criterion

This single exact criterion excludes R9_2_114,128,1487,1635,1636,1959.
It determines one central restriction vector from the source ring alone,
then detects its half-integral coefficients. No LP or twist-order search is
needed. The general-complex conclusion uses each ring's independently verified
Galois-pseudo-unitarity gate.

## Theorem

Let R be a commutative fusion ring. Suppose its FP dimensions generate the
real quadratic field K, all its formal codegrees belong to K, and sigma is
the nontrivial automorphism of K. Let N_i be the regular fusion matrices and
C=sum_i N_i N_i^t the Casimir matrix. Factor its minimal polynomial over Q
into distinct monic irreducible factors. Each factor has degree one or two.

Define p(t), modulo this square-free polynomial, by the Chinese remainder
conditions

    p(t) = 1                       modulo every linear factor,
    p(t) = t^2 / n                  modulo t^2 - a t + n.

If R admits a pseudo-unitary categorification, the first row of p(C) must be
a nonnegative integer vector with unit coefficient one. It is the restriction
of the distinguished central simple associated to sigma(FP).

## Proof

Write D for the global FP dimension. For each scalar character chi_h let f_h
be its formal codegree, A_h its distinguished central simple in I(1), and
d_h=D/f_h. Let B be the distinguished simple associated to the scalar
character sigma(FP). Its formal codegree is sigma(D), so dim(B)=D/sigma(D).

The central-character identity and symmetry of S give

    (D/f_h) chi_h(FB)
      = S_(A_h,B)
      = S_(B,A_h)
      = (D/sigma(D)) sigma(dim(A_h))
      = D/sigma(f_h).

Here sigma(FP)(F(A_h))=sigma(dim(A_h)), since restriction multiplicities are
integers. Therefore every scalar character satisfies

    chi_h(FB) = f_h / sigma(f_h).

For rational f_h this ratio is one. For a quadratic f_h with norm n,
sigma(f_h)=n/f_h and the ratio is f_h^2/n. Thus the CRT polynomial p has
exactly these values on every character eigenvalue of C.

The source algebra is commutative and semisimple, so its scalar characters
separate elements. Since C is multiplication by the Casimir element, p(C)
is therefore multiplication by F(B). Its unit row is the coefficient vector
of F(B), which must be nonnegative integral. Moreover [F(B):1]=1, since
the source character sigma(FP) has degree one. This proves the criterion.

The argument uses all scalar characters, including those with values outside
K. Only their formal codegrees must lie in K. This is why it is stronger than
labelling only the K-valued characters in a center LP.

## Six applications

Each listed vector is the exactly computed first row of p(C), in original
census basis order. Every one contains halves.

| Ring | Forced restriction of B |
|---|---|
| R9_2_114 | (1,0,0,0,1/2,1/2,1,0,0) |
| R9_2_128 | (1,0,0,1/2,1/2,1/2,1/2,0,0) |
| R9_2_1487 | (1,1/2,1/2,0,0,0,0,1/2,1/2) |
| R9_2_1635 | (1,1/2,1/2,0,0,0,0,0,1) |
| R9_2_1636 | (1,1/2,1/2,0,0,0,0,1/2,1/2) |
| R9_2_1959 | (1,1/2,1/2,1/2,1/2,0,0,0,0) |

All six have K=Q(sqrt(3)) and D=96+48sqrt(3), so B has dimension
7+4sqrt(3). Each fraction is incompatible with a restriction multiplicity.

The code also verifies that the whole matrix p(C) equals sum_i v_i N_i,
not merely that its first row has these values. The formal-codegree factor
field is checked exactly. Repeated codegrees are treated by their distinct
minimal factors, which is correct because the semisimple Casimir operator has
no Jordan blocks.

## Controls, other cases and replay

`galois_unit_restriction.py` and `galois_unit_results.json` contain the exact
CRT polynomials, vectors and source identifiers. Independent verification is
provided by the separate audit branch. The original labelled-S LP certificates
for 1487,1635,1636 and1959 remain alternative checks; they are unnecessary for
this theorem.

The known model1983 gives the valid vector (1,0,0,0,0,1,1,1,0). The separate
`galois_unit_positive_controls.py` checks every available commutative model
with quadratic FP field and codegrees in that field, recording the explicitly
out-of-scope cases as such. Integral global dimension is allowed in this
control: sigma(D)=D and the distinguished central simple can forget to the
unit while differing from the central unit.

Cases137,1607,1976 give nonnegative integral vectors and this criterion makes
no conclusion about them. The separately excluded516 also passes this test;
its structural proof in `R516_STRUCTURAL.md` supplies the additional argument.
Passing a necessary condition is not a model.

## Primary ingredients

- Ostrik, *Pivotal fusion categories of rank 3*, Theorem2.13, identifies the
  distinguished central simples and their dimensions:
  https://arxiv.org/pdf/1309.4822
- Deshpande, *On centers of bimodule categories and induction-restriction
  functors*, Corollary2.18 and section4.3 give the central-character identity:
  https://arxiv.org/pdf/1611.04486

The new step is to apply S symmetry to the distinguished sigma(FP) simple
and reconstruct its entire restriction by rational functional calculus on
the Casimir matrix.
