# Rank-eight quadratic cases: new theoretical reduction

Working date: 2026-10-27. Source snapshot: public `main` at
`6a426acf6465dd674351be92dcca41b72f371521`.

## Status and division of work

Neither ring is declared excluded or categorified by this report. For
R1768, the eleven arithmetic boundary identities below have now been
proved by two independent companion arguments, so the connected separable
algebra `1+sigma` in the actual RW precursor is constructed. A further
independently audited argument shows that its Morita dual has **only one
invertible object**, whereas R1768 has two. Thus this closes the algebra
gap but also proves that this particular construction does not model
R1768. See `R1768_DUAL_OBSTRUCTION.md` for the full argument, which also
rules out changing to a mixed multiplication on this same object.

R1154 was independently assigned to the `r8_quartic` investigator during
this work. Its new anomaly-cancellation reduction is recorded in that
investigator's report; see the last section here for the initial handoff.

## 1. R8_3_1768: the constructed separable algebra

Set `n=12`, `G=(Z/n)^2`, and

\[
 B((x,y),(a,b))=\exp(2\pi i(yb-xa)/n),\quad
 q(x,y)=(-1)^{x+y}\exp(2\pi i(y^2-x^2)/(2n)).
\]

The diagonal subgroup `L={(l,l)}` is Lagrangian, with `q|L=1`.
Let `E` be the **actual** finite quantum dilogarithm constructed by
Radchenko–Wheeler for

\[
 \gamma=\begin{pmatrix}145&12\\12&1\end{pmatrix}.
\]

Write `d=-n/E(0)`, `c=d/n=6-sqrt(37)`, and choose `kappa=sqrt(d)/sqrt(n)`.
Thus `kappa^2=c`, `c^2=nc+1`, and `E(0)=n-c=-1/c`.
The actual Fourier scalar is `lambda=1`: the eta-multiplier exponent is
`146/144-s(1,12)-1/4=73/72-55/72-1/4=0`.

Use the algebraic Leavitt realization, its untwisted crossed product by
`L`, and the old primitive idempotent

\[
 p=\frac1n\sum_{l\in L}\lambda_l.
\]

The idempotent object `rho_0=(p,tau)` generates the previously verified
`GH(C12,1)` category. Primed letters below denote the algebraic dual
generators; no adjoint or positivity is used. Define

\[
 r=\frac1{\sqrt n}\sum_{l\in L}S_l\lambda_l,
 \qquad s=\frac1{\sqrt n}\sum_{l\in L}\lambda_{-l}S'_l,
 \qquad t'=\frac1{\sqrt n}p\sum_{l\in L}T'_l.
\]

Their source/target corners are understood as in the earlier audited
orbifold construction. We have `sr=1`, and `t'` spans
`Hom(rho_0^2,rho_0)`. On `1+rho_0`, normalize the product to the tensor unit
as `s`, and its other component as `b t'`.

**Construction lemma.** Under the boundary condition

\[
                  E(l,l)=1\quad(1\le l\le11),                 \tag{B}
\]

the proof below constructs the algebra, for either square root of

\[
                     b^2=\frac{c-1}{\kappa},                 \tag{N}
\]

These components define a connected separable algebra on `1+rho_0`.
Consequently its image under the audited tensor functor
`GH(C12,1) -> twisted GH(C6,2)` defines a connected separable algebra
`1+sigma` in the actual twisted precursor.

### Direct associativity calculation

The cubic/linear associativity equation is automatic: the old exact
rotation computation gives `lambda=1` on the one-dimensional parent
trivalent space (and on the target's two-dimensional space). It remains
to verify

\[
       p s+b^2(t')^2\tau^2(p)
           =p\tau(s)+b^2t'\tau(t').                         \tag{A}
\]

Put `S'_L=sum_(l in L) S'_l` and

\[
             F(h)=\sum_{l\in L}B(l,h)E(-h-l).
\]

Expanding the explicit RW formula for `rho(T'_l)` and cancelling Leavitt
generators gives

\[
 t'\tau(t')=
 \frac1{\sqrt d}pS'_L+
 \frac1{n^2}\sum_{h\in G,\,r\in L}F(h)
                    pT'_{-h}T'_{h+r}.                    \tag{1}
\]

For clarity, in the first RW term, the sum over the diagonal index is
`sum_(r in L) B(h-l,r)^(-1)=n 1_L(h)`; its middle term vanishes because
`T'_r S_h=0`. The third term has coefficient
`q(l+h)/q(h)=B(l,h)`, giving exactly `F(h)`.

The other three expressions in (A) are

\[
 p s=\frac1{\sqrt n}pS'_L,
 \qquad
 (t')^2\tau^2(p)=\frac1n\sum_{h,r\in L}pT'_{-h}T'_{h+r},     \tag{2}
\]

\[
 p\tau(s)=\frac{\sqrt n}{d}pS'_L+
    \frac1{\sqrt n\sqrt d}\sum_{h\in G,\,r\in L}
                   q(h)^{-1}pT'_{-h}T'_{h+r}.              \tag{3}
\]

These use `p lambda_l=p`, `T'_L U_l=T'_L`, and the fact that all
diagonal bicharacter factors are one. In (2), the source projection
can be removed using `T'_l tau^2(p)=tau(p) T'_l` and
`p T'_L tau(p)=p T'_L`.

Comparing the `S'_L` coefficient gives precisely (N). All remaining
coefficients are equivalent to

\[
 F(h)=n\mathbf1_L(h)-\frac{n}{c-1}q(h)^{-1}
     =n\mathbf1_L(h)+(E(0)-1)q(h)^{-1}.                    \tag{4}
\]

The finite Fourier identity `Ehat(x)=q(x)E(x)` converts the left side to

\[
 F(h)=q(h)^{-1}\sum_{k\in L}B(-h,k)E(k).                  \tag{5}
\]

Indeed `q(h+l)=q(h)B(h,l)`, so the sum is the sum of
`Ehat(-h-l)` over `L`, divided by `q(h)`; Fourier orthogonality kills
all indices outside `L=L^perp`. Substitution of (B) in (5) proves (4),
because `q=1` on `L`. Conversely Fourier inversion shows that (4) implies
(B). Thus this is an exact boundary condition for the indicated
one-channel multiplication, rather than a heuristic analogy with a
unitary Haagerup Q-system.

### Separability without unitarity

Let `A=1+rho_0`, and let `epsilon:A->1` be the projection. The invariant
pairing `epsilon m` is `1` on the tensor-unit summand and `s` on
`rho_0^2`. The zigzag contractions of `r,s` are `1/c`; thus the inverse
copairing is `chi=1+c r` (with its two components in
`1 tensor 1` and `rho_0 tensor rho_0`). This pairing is nondegenerate.

Associativity makes

\[
        \Delta=(m\otimes1)(1\otimes\chi)
\]

an `A`-bimodule map. As `A` is connected, every endomorphism of its right
regular module is scalar: `End_A(A)=Hom(1,A)=C`. Therefore `m Delta` is
scalar, and its value on the unit is

\[
                     m\chi=(1+c)1_A.
\]

Since `1+c=7-sqrt(37) != 0`, `Delta/(1+c)` is an `A`-bimodule section of
the multiplication. This proves separability. No C*-structure,
pseudo-unitarity, or classification of all spherical near-group
categories is needed.

The tensor functor to the twisted precursor preserves multiplication,
unit, and this displayed separability section. Its image of `rho_0` is
the simple `sigma`, so it preserves connectedness in this instance.

## 2. The arithmetic boundary and its independent checks

The boundary (B) is now established by
`../root/DIAGONAL_PHASE.md` (positivity through an exact
Hirzebruch--Jung cocycle phase calculation) and
`../r6_1660/R1768_LATTICE_LEMMA.md` (absolute value one through a direct
lattice Barnes/cone cancellation). The root independently audited the
latter, and the `r9_commutative` investigator independently re-expanded
every Leavitt term and both zigzag contractions in the construction
above; its audit is `../r9_commutative/R1768_ALGEBRA_AUDIT.md`.

The direct reciprocal argument below is an additional route recorded
during the work. The completed construction can rely on the two
independently audited phase and lattice arguments instead.

### New order-independent reciprocal identity

The following direct argument proves `E(l,l)^2=1` for each nonzero
diagonal point; unlike a naive ray-class argument it makes no assumption
that `Z[sqrt(37)]` is an ideal of the maximal order.

Put `tau=6+sqrt(37)`, `epsilon=tau^2`,
`delta=diag(1,-1)`, and

\[
 j=T^{-12}S=\begin{pmatrix}-12&-1\\1&0\end{pmatrix},
 \qquad\gamma'=j\gamma j^{-1}=\delta\gamma\delta.
\]

Then `j tau=-tau`, and the denominator of this modular transformation
is `tau>0`. For `u=(l,l)` and

\[
 z=\frac{l\tau+l}{\epsilon^{-1}-1},
 \qquad z/\epsilon=z+l\tau+l,
\]

RW's cocycle identity, applied to `j gamma=gamma' j`, gives

\[
 \Phi_{j,0,0}(z/\epsilon;\tau)\Phi_{\gamma,l,0}(z;\tau)
 =\Phi_{\gamma',-l,0}(z/\tau;-\tau)\Phi_{j,l,-l}(z;\tau).
                                                               \tag{6}
\]

The two factors belonging to `j` are exactly equal. Indeed, for arbitrary
nonreal `tau`, the q-Pochhammer definition gives

\[
 \Phi_{j,l,-l}(z;\tau)
      =\Phi_{j,0,0}(z+l\tau+l;\tau),                          \tag{7}
\]

because their numerator arguments differ by the integer `l`, and their
denominator arguments differ by an integer: `j tau=-12-1/tau`, so
`-l(j tau)=12l+l/tau`, whereas
`(z+l tau+l)/tau=z/tau+l+l/tau`. This meromorphic identity continues to
the positive real `tau` under consideration. The common factor is
nonzero and finite: its possible zeros and poles lie in `Z tau+Z`, while
`z` is a nonzero torsion class for `1<=l<=11`.

Cancelling (7) in (6) proves equality of the two `Phi` values. The
associated index on the right is

\[
       u j^{-1}=(-l,-11l)\equiv(-l,l)\pmod{12\mathbb Z^2}.
\]

Both period lattices are `12 Z^2`. Also `mu_(gamma')=mu_gamma=1`:
this follows from the eta cocycle for `j gamma=gamma' j`, taking the
limit at `tau`, where the three relevant denominator factors are
`tau`, `epsilon`, and `epsilon`, all positive. Thus

\[
                 F_{\gamma'}(-l,l)=F_\gamma(l,l).            \tag{8}
\]

RW's reflection formula (immediately preceding its equation (17)) gives

\[
 \Phi_{\delta\gamma\delta,1-l,1}(z;-\tau)
                  =\Phi_{\gamma,l,0}(z;\tau)^{-1}.
\]

Its fixed-point simultaneous-index-shift identity (16), with shift
`-1`, turns the left side into `Phi_(gamma',-l,0)(z;-tau)`.
This is the value at index `(-l,l)`. As both eta multipliers are one,

\[
                 F_{\gamma'}(-l,l)=F_\gamma(l,l)^{-1}.       \tag{9}
\]

Equations (8) and (9) prove `E(l,l)^2=1`. The proof works equally for
nonprimitive diagonal points; no ray modulus needs to be chosen.

The root investigator's separate exact Hirzebruch--Jung phase
calculation gives positivity for these eleven values. The construction
above relies on that calculation together with the independently
audited lattice proof, so it does not depend on accepting this additional
reciprocal proof. The census status remains unresolved because of the
wrong-dual obstruction, not because the arithmetic boundary is missing.

### Earlier arithmetic route and its scope warning

For completeness, the earlier arithmetic route was suggested by the square root

\[
 P=\begin{pmatrix}12&1\\1&0\end{pmatrix},\qquad
 \det(P)=-1,\quad P^2=\gamma
\]

swaps the two coordinates modulo 12, fixing every element of `L`.
The real quadratic unit `6+sqrt(37)` has norm minus one. This supplies a
promising Stark/reflection route to (B), which was sent to the root
investigator for an independent arithmetic proof.

RW's conjugation identity alone gives real diagonal values. Combining it
with an absolute-value argument would give only `E(l,l)=+1 or -1`;
substituting those facts for (B) would leave a genuine gap. The new
companion phase calculation supplies the extra positivity argument. In particular,
`<1,7+sqrt(37)>=Z[sqrt(37)]` is the conductor-two order, not a fractional
ideal of the maximal order. RW section 2.3 cannot be applied to it as an
ideal of the maximal order without an additional argument. The direct
cocycle proof above avoids this issue completely.

The resulting dual is **not** R1768: the new categorical obstruction in
`R1768_DUAL_OBSTRUCTION.md` proves that it has no nontrivial invertible
simple. The existing `GH6_ROUTE.md` only proves compatible commuting
based actions; this does not imply that those actions are realized by
the actual algebra just constructed.

## 3. R8_3_1154: handoff of a new categorical reduction

The established obstruction forces the pointed `C2` associator in every
hypothetical categorification to be nontrivial. Let `g` generate that
subgroup and `s` be the semion's nontrivial invertible object. In
`C boxtimes Semion`, the diagonal `h=(g,s)` has trivial restricted
associator, hence `1+h` is an actual connected separable subgroup
algebra. Its bimodule dual must have rank ten and dimension pattern

\[
          1^{\times4},\quad a^{\times4},\quad(2a+2)^{\times2},
          \qquad a=6+3\sqrt5.
\]

This follows from left/right diagonal-orbit stabilizers: two pointed
orbits of size two, two `a`-orbits of size two, and two `b=a+1`-orbits of
size four. The first four orbits have stabilizer `C2` with two projective
characters; its second cohomology is zero. The two last orbits have
trivial stabilizer.

This reduction and the suggestion to compare its formal codegrees with
the already constrained center dimensions were passed to the dedicated
R1154 investigator. That investigator independently found the same
reduction and is checking the resulting rank-ten rings. Do not infer
that a based ring or a candidate center proves that this dual exists.

## Primary and project sources

* D. Radchenko and C. Wheeler, *Real quadratic fields and finite quantum
  dilogarithms I*, arXiv:2609.21892v2,
  <https://arxiv.org/html/2609.21892v2>. The finite Fourier equations,
  the eta multiplier, the explicit Leavitt endomorphisms, and the actual
  complex reconstruction are used. The reconstruction's absence of a
  unitarity hypothesis is essential.
* M. Izumi, *A Cuntz algebra approach to the classification of near-group
  categories*, arXiv:1512.04288v2,
  <https://arxiv.org/html/1512.04288v2>, section 12.1 and Corollary 12.7.
  Its unitary orbifold statements motivate the formulas; the algebraic
  construction used here is the separately audited project proof.
* `evidence/unresolved_retry_20261024/proofs/unresolved11_retry_20261024/`
  `global/R1768_TWISTED_PRECURSOR_AUDIT.md` and
  `global/R1768_CUBIC_ROTATION.md` supply the prior categorical precursor,
  tensor functor, normalizations, and exact cubic contraction.
* `evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/`
  `rank8_quadratic_pair/GH6_ROUTE.md` records the precise limits of the
  old based Morita data.

No long computation or online changes were made.
