# A forced third indicator at the rank-six multiplicity-eight frontier

Date: 16 October 2026. **Necessary-condition refinement only.** Both rank-six
categorification questions remain unresolved. The indicator statements concern
the canonical positive spherical structure on the positive Galois representative
of any hypothetical complex categorification.

The exact replay is `verify_r1660_higher_indicators.py --repo REPOSITORY`.
It uses only the Python standard library, binds the source tensor and the two
previously certified finite-group character tables by SHA256, and regenerates
all torus, compression, and matrix-coefficient calculations below. It does not
assume a particular retained center profile or low-branch labelling.

## 1. Categorical inputs and normalization

Use the source order `(1,g,X,gX,sigma,T)`, where `T=sigma X`,

    d=dim(X)=3+2 sqrt(2)+2 sqrt(3)+sqrt(6),
    D=4(1+d^2)=144+96 sqrt(2)+80 sqrt(3)+56 sqrt(6),
    1/D=(6-2 sqrt(3)-sqrt(6))/48.

The existing rank-six manuscript establishes the following facts for every
hypothetical categorification, after its proved positive Galois reduction:

* the twist-one central simples are precisely the six multiplicity-one
  constituents of `I(1)` (Proposition `1660-twist-one-support`);
* the modular representation factors through `SL2(Z/48)`;
* four constituents `L_gamma` are indexed by the four conjugates of the
  dimension character; the remaining two characters are rational;
* the coherent tensor involution exchanges `X` and `gX`, so all their
  indicators coincide (Proposition `1660-tensor-involution`);
* odd powers of `g` and `sigma` have no unit summand, so their odd indicators
  vanish.

Write `s` for the normalized center S matrix and `t` for the twist matrix.
The representation is unitary as a finite-group representation; no unitary
structure on the original fusion category is assumed. The canonical modular
matrix is itself unitary in the positive spherical normalization, as used in
the existing dimension-block argument.

For `r=3,6`, let `chi_r` be the quadratic character corresponding to `sqrt(r)`
and put

    w_r=sum_gamma chi_r(gamma) e_(L_gamma).

Then `||w_r||^2=4` and `<e_unit,w_r>=1`. On the whole twist-one space the
diagonal torus has character multiplicities `(3,1,1,1)` for discriminants
`1,8,12,24`. Its `chi_r` eigenspace is therefore exactly `C w_r`.
The known compression `P s P` has eigenvalue `-sqrt(3)/6` on `w_3` and
`-sqrt(6)/12` on `w_6`. Its remaining eigenvalues are `1,1,-1/2,0` in
one low branch and `1,-1/2,0,0` in the other branches.

These are categorical conclusions already proved in the rank-six manuscript,
not assertions deduced from the existence of a numerical modular witness.
The finite-group character tables used here have complete exact prior
class-algebra, orthogonality, degree, T-spectrum, and central-sign certificates
in `supplements/rank6/research/round5/m8_modrep/finite_spectra48.py`.

## 2. Unique saturated irreducible summands

The replay exhausts all 532 tensor products of local irreducibles of
`SL2(Z/16)` and `SL2(Z/3)`. It recomputes torus traces by

    Tr(h_a P)=(1/m) sum_j character(h_a T^j)

and compression traces by

    Tr(P s P)=(1/m) sum_j character(T^j S),
    Tr((P s P)^2)=(1/m^2) sum_(j,k) character(T^j S T^k S).

An eligible compression polynomial must divide one of the two low-block
polynomials above, its central sign must be positive, and its torus weights
must be nonnegative and bounded by `(3,1,1,1)`. On a one-dimensional
`chi_r` fixed space the scalar compression must equal the specified
`chi_r` eigenvalue. Every eligible irreducible
containing `chi_3` or `chi_6` has one-dimensional T-fixed space. The complete
lists, in the frozen ordering of the local character tables, are

| sector | possible irreducible pairs |
|---|---|
| `chi_3` | `(33,4)`, `(36,5)` |
| `chi_6` | `(54,4)`, `(61,5)` |

Because the full T-fixed torus multiplicity is one, `w_r` lies in exactly one
copy of exactly one such irreducible `W_r`, and `W_r^t=C w_r`. Orthogonal
projection of the central unit vector into `W_r` is consequently `w_r/4`.
This is the step that turns a character trace into the required matrix
coefficient. Merely knowing the eigenvalue of the low compression would not
suffice.

For an eligible pair define

    m_r(n)=Tr(P_(W_r) s^(-1) t^n s).

Here `P_(W_r)` projects onto the one-dimensional T-fixed space of `W_r`.
It follows that

    <s w_r,t^n s e_unit>=m_r(n).

Indeed, both `s` and `t` preserve `W_r`; replace `e_unit` by `w_r/4` and
use the normalized vector `w_r/2` to evaluate the rank-one trace.

For each local modulus `m=16,3`, the matrix coefficient is computed exactly
from the class character as

    (1/m) sum_(j=0)^(m-1) character(T^j S^(-1) T^n S),
    T^j S^(-1) T^n S = [[1-jn,j],[-n,1]] modulo m.

The global value is the product of the two local values. Thus there is no
unrecorded choice of finite-group matrices or numerical eigenvectors.

## 3. From matrix coefficients to source indicators

For a central simple `A`, write `z_A=dim(A)` and let `ell_r(z)` be the
rational `sqrt(r)` coefficient of `z/D`. The low-character S formula gives

    (s w_r)_A=sum_gamma chi_r(gamma) gamma(z_A/D)
               =4 sqrt(r) ell_r(z_A).

The center indicator formula therefore gives, for every positive integer n,

    sum_i ell_r(dim X_i) nu_n(X_i)
      = (1/D) sum_A ell_r(z_A) z_A theta_A^n
      = m_r(n)/(4 sqrt(r)).

This uses the source-character normalization `s_(A,L_gamma)=gamma(z_A/D)`.
All these entries are real, so no conjugation changes the displayed scalar
product. In source order, the rationally scaled weights are

    24 ell_3=(-1,-1,1,1,-1,-1),
    48 ell_6=(-1,-1,-1,-1,-2,2).

Consequently define `a_n=2 sqrt(3) m_3(n)` and
`b_n=2 sqrt(6) m_6(n)`. For odd n the coherent involution and the vanishing
odd indicators of `g,sigma` give

    nu_n(X)=nu_n(gX)=(3+2a_n+b_n)/2,
    nu_n(T)=2+a_n+b_n.

The independent replay verifies these weights directly in `Q(zeta_48)`
from the full source dimension character.

## 4. The third-rotation restriction

Let `omega=exp(2 pi i/3)`. At n=3 the four exact possibilities are

| `chi_3` pair | `chi_6` pair | `nu_3(X)` | `nu_3(T)` |
|---|---|---|---|
| `(33,4)` | `(54,4)` | `2+omega` | `2` |
| `(33,4)` | `(61,5)` | `-3 omega^2` | `-4 omega^2` |
| `(36,5)` | `(54,4)` | `-3 omega` | `-4 omega` |
| `(36,5)` | `(61,5)` | `2+omega^2` | `2` |

The source tensor gives `dim Hom(1,X^3)=3`. Third pivotal rotation has
order dividing three on this space, so its trace is
`a+b omega+c omega^2` for nonnegative integers `a+b+c=3`.
The two mixed traces are impossible: their real part is `3/2`, which forces
`a=2` and `b+c=1`, hence imaginary part of absolute value at most
`sqrt(3)/2`; the mixed traces have absolute imaginary part `3 sqrt(3)/2`.
The replay independently enumerates all ten possible multiplicity triples.

We have thus proved the necessary conditions

    nu_3(T)=2,
    nu_3(X)=nu_3(gX) in {2+omega,2+omega^2}.

The two remaining irreducible choices are simultaneous complex conjugates.
No assertion that a self-dual object's third indicator is real is used;
that assertion is false in general.

The same exact matrix coefficients force

    nu_5(X)=nu_5(gX)=nu_5(T)=2,
    nu_7(X)=nu_7(gX)=3,  nu_7(T)=4.

The source invariant dimensions at powers five and seven are respectively
`(402,2272)` and `(55401,626784)` for `(X,T)`. These values satisfy the
usual integer prime-rotation multiplicity bounds and congruences. They
supply no contradiction.

## 5. Scope of the refinement

The rank-37 necessary-system witness already uses the surviving pair
`(36,5),(61,5)`. The new argument excludes two mixed representation choices,
reduces the previously six-valued third indicator of `T` to the singleton
`{2}`, and determines the third rotation on `Hom(1,X^3)` up to conjugation.
It neither constructs a center nor excludes the remaining possibilities.
No rank-six classification count or categorical status changes.

Primary ingredients beyond the earlier manuscript are the standard center
indicator formula and finite-order pivotal rotation of Ng--Schauenburg
(already cited there as `NSind`, `NSpiv`), together with exact character
traces of finite groups. The proof makes no new appeal to an unverified
classification of modular categories or near-group categories.
