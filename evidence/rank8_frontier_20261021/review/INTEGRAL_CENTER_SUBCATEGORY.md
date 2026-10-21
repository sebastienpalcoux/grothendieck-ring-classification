# No nonunit integral central simples for R439 and R567

This is a general-complex necessary condition, not by itself a
noncategorification certificate. It also applies to every category Morita
equivalent to a hypothetical category with either source ring. In particular,
it applies to the R5_3_40 Morita dual forced for R439 by the separately verified
full-S3 condensation argument. It does not apply to arbitrary categorifications
of R5_3_40, whose centers can have nontrivial invertibles.

## Proposition and proof

Let C have ring R8_3_439 or R8_3_567, or let C be its R5_3_40 Morita dual.
Write d=3+2 sqrt(3). Source simple Frobenius--Perron dimensions are respectively
six copies of 1 and two copies of d, or 1,1,2,d,d. In each case the simple
objects with integral dimension form a fusion subcategory C_int: the tensor
checks verify closure, and duality preserves it. The global FP dimension is

    D = 48+24 sqrt(3),   Norm(D)=576,
    FPdim Z(C)=D^2=4032+2304 sqrt(3).

The known-model route proof establishes Inv Z(C)={1} for the two rank-eight
sources without pivotal assumptions: the only invertible source basis object
central in its based ring is 1, and C_ad=C, so the kernel over 1 of the
forgetful map on invertibles, Aut_tensor(Id_C), is also trivial. Braided Morita
invariance of the center gives the same conclusion for the specified rank-five
dual.

Consider the full fusion subcategory E of Z(C) consisting of objects whose
forgetful images lie in C_int. Its simple objects are precisely the central
simples of integral FP dimension: their restrictions have dimensions a+b*d,
where a,b are nonnegative integers, and this is rational if and only if b=0.
This proves closure here; no unsupported assertion about integer-dimensional
simples in arbitrary fusion categories is needed.

Set N=FPdim(E). It is a positive integer, because all its simple dimensions
are integers. By ENO, *On fusion categories*, Proposition 8.15, D^2/N is an
algebraic integer. Taking the norm in Q(sqrt(3)) gives

    Norm(D^2/N) = 576^2/N^2 in Z.

Consequently N divides 576=2^6*3^2. By ENO, *Weakly group-theoretical and
solvable fusion categories*, Theorem 1.6, E is solvable. Proposition 4.5(iv)
of that paper says that a nontrivial solvable fusion category has a nontrivial
invertible simple. Such an object would be invertible in Z(C), contrary to
Inv Z(C)={1}. Therefore E=Vec.

Thus the tensor unit is the only integral-dimensional simple object of Z(C).
In any central restriction enumeration every nonunit column supported entirely
on the source integral subcategory must be removed. For the rank-eight rings
this removes columns supported on their six invertibles; for the specified
rank-five dual it removes columns supported on 1,s,V.

No pseudo-unitarity or Galois argument is required for this proposition, since
only Frobenius--Perron dimensions, tensor subcategories, and Morita invariance
are used. Application inside spherical center computations uses their existing
scope gates.

## Primary references

* P. Etingof, D. Nikshych and V. Ostrik, *On fusion categories*,
  https://arxiv.org/abs/math/0203060, Proposition 8.12 (center FP dimension),
  Corollary 8.14 (Morita FP dimension), Proposition 8.15 (subcategory
  divisibility). The PDF locates Proposition 8.15 on printed page 32.
* P. Etingof, D. Nikshych and V. Ostrik, *Weakly group-theoretical and solvable
  fusion categories*, https://arxiv.org/abs/0809.3031, Theorem 1.6 and
  Proposition 4.5(iv), printed pages 2 and 13.

`integral_center_subcategory.py` verifies the source dimensions, fusion
identities, duals, integral-subcategory closure, center-invertible source
conditions, and exact norms. It is an arithmetic binding of the written
categorical argument, not a machine proof of the cited theorems. Its normal
and optimized invocations have the same explicit checks.
