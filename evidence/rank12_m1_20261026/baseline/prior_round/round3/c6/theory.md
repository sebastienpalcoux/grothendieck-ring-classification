# Rank-12 order-six quadratic families: third pass

## Decisions

**R12_1_350 is excluded from categorification by any fusion category over C.**
The other four cases R12_1_332, R12_1_561, R12_1_623, and R12_1_628 remain unresolved.
No new model is asserted.

The exclusion uses a rank-independent central-induction argument, followed by a
small, complete exact certificate calculation. It does not assume unitarity,
a trivial pointed associator, or completeness of the known Haagerup models.

## The general-complex gate

Each ring has two Frobenius-Perron values, 1 and d. The published version of
Schopieray, *Categorification of integral group rings extended by one dimension*,
Lemma 3.1, gives a Galois conjugate which is pseudo-unitary for any complex
categorification with two FP values. Do not replace this by the stronger claim
that the original category is necessarily pseudo-unitary. For these rings, a
contradiction in the pseudo-unitary setting therefore excludes arbitrary complex
categorification. The independent audit checked the published wording.

## R350: exact structure and low central induction

Let G=S3 and choose rho corresponding to input label 11. The relations are

    g rho = rho g,
    rho^2 = 1 + sum_{g in G} g rho,
    d = 3 + sqrt(10),  d^2 = 1 + 6d,
    D = FPdim(C) = 12 + 36d = 120 + 36sqrt(10).

The group irreducibles give the complete complex irreducible representations of
this based algebra. The trivial G-character has the two rho-eigenvalues d and
-1/d. The sign representation has rho-eigenvalues +1 and -1. The standard
2-dimensional G-representation has rho=+I and rho=-I. Their dimensions are
1,1,1,1,2,2, and their formal codegrees are D,D',12,12,6,6.
Consequently the six distinct simple summands of I(1) have central dimensions

    1, d^2, 1+3d, 1+3d, 2+6d, 2+6d

and their multiplicities in I(1) are 1,1,1,1,2,2. Their twists are all 1.
All these statements use the spherical central-induction/formal-codegree theorem,
not the unitary classification part of Edie-Michell–Izumi–Penneys.

The actual Gram matrix used throughout is

    B[j,i] = sum_{a,k} N[a,j,k] N[k,a*,i].

Thus B is the matrix of FI, with B=MM^T for the complete restriction matrix M.
In the noncommutative setting this must not be replaced by the Casimir matrix
sum_a N_a N_{a*}.

Every forgotten central object is central in the based algebra. For R350 this
means its coefficients are constant on each of the following classes:

    pointed: {0}, {1,2}, {5,8,10};
    nonpointed: {3,4}, {6,7,9}, {11}.

The unit row of B has no other pointed support, so the five nontrivial low
columns have only their forced unit coefficient plus nonpointed entries. If the
three nonpointed class coefficients are (a,b,c), their weighted sum is
2a+3b+c. It is 6,3,3,6,6 for the five columns. Combining this with

    L (1,1,1,1,2,2)^T = B[:,0]

gives exactly 30 ordered low-column possibilities. The exact Gram test
B-LL^T >= 0 excludes 26. Rational vectors with negative quadratic form are
stored, rather than floating eigenvalue decisions. Four branches remain.

## Complete high-column domain and the trace contradiction

For each remaining branch put Q=B-LL^T. A high central restriction column has
unit coefficient zero, nonnegative integer entries, and the class constancies
above. It must satisfy Q-vv^T >= 0. The implementation exhausts the five class
coefficients, using the exact bounds v_i <= floor(sqrt(Q_ii)), all entrywise
bounds, the nullspace of Q, and an exact inverse on a nonsingular principal
submatrix. These conditions are equivalent to the required rank-one PSD bound
on that support; no numerical PSD decision is used.

For beta=dim(v), impose the necessary algebraic-integrality conditions
D/beta integral and beta a d-number. These apply to simple objects in the
pseudo-unitary modular center. This leaves respectively 30,43,43,28 possible
high restriction columns in the four branches.

We then apply the project's existing finite relative-trace criterion at heights
1 through 6. The dimension field is Q(sqrt(10)), of conductor 40. The prime
support of the Frobenius-Schur exponent is contained in {2,3,5}, by the categorical
Cauchy theorem and Norm(D)=1440. The exact joint relative traces of all permitted
roots of unity are covered by 45 types. Orders not represented in the bounded
Gauss-sum box contribute the zero trace vector, which is explicitly included.
The displayed order bound 7200 is a trace-type reduction, not an assumed bound
on the actual categorical exponent.

The equations include the Gram identity, the first and second twist traces, and
the normalized rational higher-indicator traces. The latter are bounded by the
dimension [X^k:1] of the pivotal rotation space; all these dimensions are computed
from the full tensor. Selfdual noninvertibles have second indicator +1 by the
adjoint-parity criterion, because they occur with odd multiplicity in Y Y*.
The two nonselfdual noninvertibles and two nonselfdual invertibles have indicator
zero. We allow both signs independently for each of the three involutions:
eight choices, an overapproximation which avoids requiring conjugacy invariance.

Each of the 4 x 8 = 32 resulting rational feasibility systems A x=b, x>=0 has an
integer Farkas witness y satisfying A^T y>=0 and b^T y<0. All 32 have been checked
using exact integer arithmetic. Thus none of the complete low branches can be
completed to a categorical restriction matrix and twist system.

An independent audit reconstructs the systems without importing the rank-six
implementation, and without optimization:

    ../d120/audit_R350.py
    ../d120/audit_R350.md
    ../d120/audit_R350.json

That audit passed and confirms the general-complex scope.

## New restrictions on the other cases

### R623

The same central-column method applies to the nonselfdual inversion-action C6
ring. There are 16 low possibilities, 12 eliminated by exact Gram witnesses and
four surviving. At height 6 all four surviving branches exclude nu_2(z)=+1 for
the unique pointed involution z (input label 11). No exclusion certificate was obtained for the nu_2(z)=-1 branches. Therefore, subject to the same audited indicator theorem, any
pseudo-unitary categorification would have nu_2(z)=-1. Equivalently its pointed
associator restricted to <z>=C2 is nontrivial. This is a restriction, not a full
exclusion. In particular the ordinary algebra 1+z is unavailable in such a
categorification.

As a positive control, the identical method applied to the known HI_C6 model
R326 obtains no exclusion in the four nu_2(z)=+1 branches and rejects nu_2(z)=-1. This agrees with
its actual trivial pointed associator. Neither an unseparated relaxation nor failure to find a separating ray is a model.

The known central fermion of R326 must not be conflated with nu_2(z)=-1: a
fermionic central half-braiding can have underlying pointed associator trivial
and second indicator +1, exactly as in this control.

### R561 and R628

If the order-three pointed subgroup had a fully faithful central Tannakian
Rep(C3) lift, de-equivariantization would be defined. Its action on simples is
free, and the resulting orbit fusion ring has four simples (1,g,X,gX), with

    g^2=1, gX=Xg,
    X^2=1+3X+3gX       for R561,
    X^2=g+3X+3gX       for R628.

The complete tensor orbit maps are checked. The first quotient is excluded by
the project's uniform diagonal two-invertible theorem (m>=3); the second by
its nonselfdual induction theorem. Both exact certificates were replayed.
Consequently neither ring can have that central Tannakian lift.
Commutativity of a Grothendieck ring does not supply a central lift, so this
does not exclude the original rank-12 rings.

Schopieray's published *Irrational braided generalized near-groups*, Theorem3.6,
also excludes braided categorifications of these two rings: their noninvertible
FP dimension 3+sqrt(10) is neither the Fibonacci nor PSU(2)_6 value. The other
three rings in this packet are noncommutative and hence also nonbraidable.
This restricts direct braided/quantum-group model searches, not general complex
categorification or Morita constructions.

### R332

The neutral Haagerup-C3 subring remains categorifiable. A putative crossed-product
construction requires a genuine order-two tensor autoequivalence inverting C3
and fixing a suitable rho, with coherence. The untwisted unitary Haagerup
outer-automorphism computation is not a classification of all spherical twisted
categories. Twisted Haagerup precursors exist via near-group C9+9, not C3^2+9.
Their existence alone supplies neither the required involution nor the crossed
product. No full exclusion or verified construction was obtained.

## Other attempted routes and precise limitations

* Izumi's odd-group, odd-multiplicity obstruction does not apply to a group of
  order six. Its offending half-integer coefficient becomes integral here.
* The free pointed action on noninvertible simples forces no nontrivial subgroup
  algebra by the fixed-simple method.
* R350's earlier conditional rank-six Morita proof required a pointed subgroup
  algebra. The new central-induction proof removes that premise entirely.
* Known HI_C6 central-fermion/subgroup constructions were inspected. No explicit
  separable algebra plus full fusion-tensor transport producing R623 was found.
* Ordinary graded twists cannot alter the four uniform sqrt(10) rings: their
  adjoint ring is the whole ring, so their universal grading is trivial.
* Relative-center constructions or matching modular data are not category models.
* No classification of unitary categories was used to exclude arbitrary spherical
  or complex categories.

## Sources checked

- Schopieray, *Categorification of integral group rings extended by one dimension*,
  published Lemma3.1: https://doi.org/10.1112/jlms.12789
- Edie-Michell–Izumi–Penneys, *Classification of Z/2Z-quadratic unitary fusion
  categories*, general spherical TheoremC: https://arxiv.org/abs/2108.01564
- Izumi, *The classification of 3^n subfactors*, Theorem2.2 and its hypotheses:
  https://arxiv.org/abs/1609.07604
- Izumi, near-group reconstruction and Examples12.13–12.14:
  https://arxiv.org/abs/1512.04288
- Grossman–Izumi, center computations, Example4.5 (C6 and its fermion):
  https://arxiv.org/abs/1501.07679
- Grossman–Izumi–Snyder, graded extensions and actual categorical outer actions:
  https://arxiv.org/abs/2201.11901
- Schopieray, *Irrational braided generalized near-groups*, Theorem3.6:
  https://doi.org/10.4153/S0008439523000334

No online repository or website was changed.
