# The constructed algebra has the wrong pointed Morita dual

## Scope

This note concerns the specific RW twisted `GH(C6,2)` category constructed
and audited in this project, and the particular object `1+sigma` in it.
It does **not** exclude R8_3_1768 from general complex categorification.

The arithmetic boundary is now proved by the root investigator's
`../root/DIAGONAL_PHASE.md` and the independent
`../r6_1660/R1768_LATTICE_LEMMA.md`. Together with `REPORT.md` and the
independent algebra audit in
`../r9_commutative/R1768_ALGEBRA_AUDIT.md`, this constructs a connected
separable algebra on `1+sigma`. The following argument explains why this
does not yet categorify R1768: its Morita dual has no nontrivial
invertible simple object, whereas R1768 has two invertible simples.

This argument was sent to independent investigators for audit. Its
critical transport calculation and finiteness argument are explicit
below.

## 1. Two algebra lines are exchanged by conjugation

Continue the notation of `REPORT.md`, and put `z=(0,6)`, `Z=lambda_z`.
Let

\[
 p_\eta=\frac1{12}\sum_{l=0}^{11}\zeta_{12}^{-\eta l}
                    \lambda_{(l,l)}.
\]

The parent `GH(C12,1)` category contains the simple idempotent objects
`(p_eta,tau)`. Conjugating its `p_0` object by the pointed object indexed
by 3 gives the `p_6` object: conjugation by `beta_g` changes the projector
index by `-2g`. This can be checked directly from

\[
 \beta_g\tau\beta_{-g}=\operatorname{Ad}(U_{-g})\tau,
 \qquad U_g\beta_g(p_0)U_{-g}=p_{-2g}.
\]

The parent trivalent space at `p_6` is one dimensional, spanned by

\[
              t'_6=12^{-1/2}p_6\sum_{l\in L}T'_l.
\]

Therefore conjugating the parent algebra gives an algebra whose
non-unit multiplication lies on this line, with nonzero coefficient.

In the twisted target, `p_6` and `p_0` are equivalent through `Z`, since
`Z p_6=p_0 Z` and `Z` belongs to `End(tau)`. The tensor square of this
equivalence is `Z tau(Z)`, with source and target projections inserted.
As

\[
                    \tau(Z)=-U_z Z,
\]

its square transport is `-U_z`. Thus the transported trivalent map is

\[
 Zt'_6\bigl(Z\tau(Z)\bigr)^{-1}
 =-12^{-1/2}p_0Z\sum_{l\in L}T'_{l-z}
 =-t'_1.                                                   \tag{1}
\]

Here `T'_l U_{-z}=T'_{l-z}`, and `z=-z` modulo 12. The original algebra
lies on the `t'_0` line. Thus conjugation by the target's pointed
involution `g^3` exchanges the two distinct multiplication lines.

For projection bookkeeping in (1), `p_6 U_z=U_z p_0` and
`Z U_z Z=U_z`. Hence
`(Zp_6) tau(Zp_6)=-U_z p_6 tau(p_6)`, whose inverse on its source corner
is `-p_6 tau(p_6) U_{-z}`. Multiplication by `t'_6` removes this source
projection and gives (1).

## 2. There cannot be a mixed multiplication line

Normalize the unit-output multiplication to `s` and write the other
component as

\[
                 t=a t'_0+b t'_1,
 \qquad a^2-b^2=K:=\frac{c-1}{\sqrt c}\ne0.                 \tag{2}
\]

The cubic equation is automatic for both basis vectors. The remaining
associativity equation has the form

\[
                  C+a^2Q_{00}+abQ_{01}+b^2Q_{11}=0,         \tag{3}
\]

where `C,Q_ij` are fixed morphisms. The original parent-descended algebra
gives `(a^2,b)=(K,0)`, so `C+K Q00=0`. The conjugate algebra in section 1
is purely on the second line; equation (2) gives `b^2=-K`, hence
`C-K Q11=0`. Consequently `Q11=-Q00`, and on the conic (2), (3) reduces
to

\[
                              abQ_{01}=0.                  \tag{4}
\]

We must have `Q01 != 0`. Otherwise every point of the nondegenerate conic
(2) gives an associative algebra. Every one of these algebras is
connected and separable: its invariant pairing is always `1+s`, with
inverse copairing `1+c r`, and the same computation in `REPORT.md`
splits multiplication by the scalar `1+c != 0`.

These would give infinitely many algebra-isomorphism classes. An
isomorphism of the underlying object fixing the unit is
`1 tensorunit + lambda id_sigma`; preserving the normalized unit-output
coefficient forces `lambda^2=1`. It therefore identifies at most two
points of the conic.

On the other hand, all the resulting module categories have rank eight,
by the forced induction Gram factor `[I6,0; I6,J_(6x2)]`. ENO,
*On fusion categories*, Corollary 2.35, gives only finitely many module
categories of that fixed rank. In each such module category a connected
algebra is the internal end of its right regular module, which is
simple because `End_A(A)=Hom(1,A)=C`. There are only finitely many simple
objects, hence only finitely many such connected algebra-isomorphism
classes. This is a contradiction.

Therefore (4) forces `ab=0`. Up to algebra isomorphism there are exactly
the two pure multiplication lines constructed above. In particular
neither is fixed by conjugation by `g^3`.

## 3. No nontrivial invertible object in either Morita dual

Write `u=6+sqrt(37)` for the positive dimension, distinct from the
negative categorical parameter `c`. Let `A` be either algebra. The
simple right `A` modules are the six free modules `m_g=gA` and two
additional modules `x,y`. Their underlying FP dimensions are

\[
          \operatorname{FPdim}(m_g)=1+u,
 \qquad \operatorname{FPdim}(x)=\operatorname{FPdim}(y)=6u.
\]

Indeed the induction factor gives `sigma A=m_0+x+y`; the pointed
generator interchanges `x,y`, and their sum has dimension `12u`.

An invertible `A`-bimodule `M` acts as an equivalence on right modules
and sends the simple regular module `A` to the simple right module `M`.
Also `FPdim_C(M)=FPdim_C(A)=1+u`. Hence it must be one of the six
right modules `gA`.

Giving `gA` an invertible bimodule structure amounts to an algebra
isomorphism `A -> g A g^{-1}`: the left action lands in the internal end
of `gA`. The two objects have equal dimension and the map is nonzero on
the nontrivial simple summand (otherwise its multiplication to the unit
would contradict the algebra-map property), so the action is an
isomorphism. Since

\[
                   g^j\sigma g^{-j}=g^{2j}\sigma,
\]

the underlying objects agree only for `j=0,3`. For `j=3`, section 2
rules out the required algebra isomorphism. For `j=0`, possible
structures are algebra automorphisms of `A`; there are none besides the
identity, since its multiplication has a nonzero `sigma` component and
its `sigma^2 -> 1` component is nonzero.

Thus the pointed subcategory of either dual is just `Vec`. R1768 has a
pointed subgroup of order two, so neither dual is a model of R1768.

This proves a failure of this specific precursor-and-`1+sigma` route,
not a general exclusion of R1768. Other algebra objects, other precursor
categories with the same fusion rules, or other categorical routes are
not eliminated here.

## 4. The same argument for every translated noninvertible

The construction and obstruction extend to every `1+g^j sigma` in this
same precursor, rather than just the choice `j=0`. In the parent,
replace the three intertwiners by

\[
 r_\eta=12^{-1/2}\sum_{l\in L}\zeta_{12}^{-\eta l}S_l\lambda_l,
 \quad s_\eta=12^{-1/2}\sum_{l\in L}\zeta_{12}^{\eta l}
                                   \lambda_{-l}S'_l,
 \quad t'_\eta=12^{-1/2}p_\eta T'_L.
\]

The averaging identity remains
`p_eta T'_L tau(p_eta)=p_eta T'_L`. Also
`p_eta lambda_l=zeta^(eta l) p_eta`, which cancels the extra character in
`p_eta s_eta` and in `p_eta tau(s_eta)`. Consequently equations (1)--(5)
of `REPORT.md` hold with `p_eta` in place of `p`. The cubic contraction
forces its two outer diagonal indices equal, so its two extra character
factors cancel; its scalar is still one. Both zigzags are still `12/d`.
Thus the same proved boundary constructs the parent algebra for each
`eta`.

Conjugation by `g^3` sends `p_eta` to `p_(eta+6)`, and `Z` identifies
these two projectors in the target. Repeating (1) exchanges the two
independent target multiplication lines. The conic and rigidity argument
then applies unchanged (a harmless nonzero change of basis can alter
the displayed coefficient signs). In particular there are just the two
pure algebra classes, exchanged by the pointed involution.

The right-module dimension argument is independent of `j`. Therefore
the dual of every connected separable algebra on any `1+g^j sigma` in
this particular precursor has only the identity invertible. None is a
model of R1768. This strengthens the scope of the route obstruction but
still does not exclude R1768 itself.

## Primary rigidity source

P. Etingof, D. Nikshych, V. Ostrik, *On fusion categories*, Annals of
Mathematics 162 (2005), 581–642, Corollary 2.35:
<https://annals.math.princeton.edu/wp-content/uploads/annals-v162-n2-p01.pdf>.
The cited finiteness is for fixed number of simple module objects,
which suffices here; no stronger unqualified finiteness assertion is
required.
