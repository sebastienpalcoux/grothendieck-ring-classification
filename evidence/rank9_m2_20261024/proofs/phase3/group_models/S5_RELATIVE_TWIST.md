# A relative Schur-cocycle model for R9_2_92

## Construction

Let G=S5 and H=S({1,2,3})×S({4,5})≅S3×C2. Write ε:G→F2 for the sign.
Choose a normalized mod-two Schur cocycle α:G×G→F2. We choose the version
for which a transposition lifts to an involution; starting from either
Schur double cover this is achieved, when necessary, by adding
ε(g)ε(h). Define

\[
\omega(g,h,k)=(-1)^{\epsilon(g)\alpha(h,k)}.
\]

This is an actual normalized three-cocycle: it is the cup product of the
one-cocycle ε and the two-cocycle α, followed by F2→{±1}. The saved
finite table verifies the two-cocycle identity for α on all 120^3 triples.
Consequently the three-cocycle identity follows algebraically, without
an unverified associator-existence assertion.

For h∈H let x(h) be the sign of its S3 coordinate and y(h) the sign of its
C2 coordinate, so ε|H=x+y. The restriction of α is cohomologous over F2
to x(h)y(k). The script solves and verifies a normalized one-cochain f
such that

\[
\alpha(h,k)=x(h)y(k)+f(h)+f(k)+f(hk)\quad\text{in }F_2.
\]

In particular, this step is checked as an equality of cochains, not
merely inferred from a cohomology dimension. Index F2² by x+2y. Let r be
the following normalized Z/4-valued two-cochain on F2², with rows and
columns in order 0,1,2,3:

\[
r=\begin{pmatrix}
0&0&0&0\\
0&0&0&2\\
0&1&0&3\\
0&3&0&3
\end{pmatrix}.
\]

Directly, its coboundary is
`δr(a,b,c)=2(x(a)+y(a))x(b)y(c) mod4`. Therefore

\[
\psi(h,k)=i^{\,r((x(h),y(h)),(x(k),y(k)))+2\epsilon(h)f(k)}
\]

satisfies δψ=ω|H. Since ω takes values ±1, this also equals ω^{-1}|H,
which is the algebra convention used below. The script verifies this
identity on all 12^3 triples. All the data are roots of unity.

Let A be the twisted H group algebra in Vec_G^ω, with basis a_h of degree
h and multiplication a_h a_k=ψ(h,k)a_hk. Its associativity follows from
δψ=ω^{-1}|H. The category of A-bimodules in Vec_G^ω is a well-defined
unitary group-theoretical fusion category, denoted C(G,ω,H,ψ). Thus
coherence is established before any fusion tensor is calculated.

The full integer fusion tensor computed below is based-isomorphic to
`R9_2_92`, under the source-to-model permutation

```
[0,3,1,5,7,6,4,2,8].
```

The remaining sections derive the exact tensor calculation. Independent
review is required before promoting the accompanying candidate record.

## Simple objects and projective multipliers

For t∈G representing an H double coset, put
`K_t=H∩tHt^{-1}`. A simple A-bimodule supported on HtH is specified by
an irreducible projective representation ρ of K_t. With the conventions
used here, its multiplier is

\[
\alpha_t(a,c)=
\frac{\psi(a,c)\,\omega(a,t,t^{-1}ct)}
{\omega(a,c,t)\,\omega(t,t^{-1}at,t^{-1}ct)\,
 \psi(t^{-1}at,t^{-1}ct)}.
\tag{1}
\]

To verify this convention, let L_a and R_b be left and right algebra
multiplications on a bimodule. On its degree-g fiber, the three module
identities read

\[
L_aL_c=\frac{\psi(a,c)}{\omega(a,c,g)}L_{ac},\qquad
R_cR_a=\omega(g,a,c)\psi(a,c)R_{ac},
\]
\[
R_cL_a=\omega(a,g,c)L_aR_c.
\tag{2}
\]

On the degree-t fiber define `ρ(a)=R_{t^{-1}at}^{-1}L_a`.
Substituting (2) gives (1). The categorical dimension of this simple is
`[H:K_t] dimρ`.

For this particular (G,H), the double cosets have sizes 12,72,36 and
stabilizer orders 12,2,4. The first has multiplier one and gives the six
ordinary irreducibles of H, of dimensions (1,1,1,1,2,2). The second has a
cyclic stabilizer and gives two projective one-dimensional representations,
hence two categorical simples of dimension six. The last has stabilizer
V4 and a nondegenerate projective multiplier: its commutator radical is
trivial. Its twisted group algebra is M2(C), so it has one projective
irreducible of dimension two, contributing one categorical simple of
dimension six. Thus the total type is (1^4,2^2,6^3), with dimension 120.

The projective characters needed by the calculation are explicit:
ordinary H characters; on C2, the two square roots of α_t(s,s), with
opposite signs; on the nondegenerate V4 twisted algebra, character two at
the identity and zero elsewhere. They take values in Q(ζ8).

## Transporting a projective character between fibers

For each double-coset representative t, choose representatives l for
left cosets H/K_t. Thus u=lt represents a right H coset in HtH. Normalize
the degree-u vector space using L_l from the degree-t space. For a∈H
stabilizing uH, write s=l^{-1}al∈K_t and c=t^{-1}st. The character of
`R_c^{-1}L_a` on the degree-u fiber is

\[
\chi_u(a)=
\frac{\psi(a,l)\omega(l,s,t)}
{\omega(a,l,t)\psi(l,s)\omega(l,t,c)}\chi_t(s).
\tag{3}
\]

This follows by writing `al=ls` and twice applying the left action and
bimodule identities (2).

For an arbitrary fiber v=uk, k∈H, normalize it by R_k from degree u.
If a stabilizes vH, put c=u^{-1}au and b=v^{-1}av=k^{-1}ck. Then

\[
\chi_v(a)=
\frac{\omega(u,c,k)\psi(c,k)}
{\omega(a,u,k)\omega(u,k,b)\psi(k,b)}\chi_u(a).
\tag{4}
\]

Indeed, move L_a past R_k, and then compare R_kR_c with R_bR_k using
(2). Equations (3),(4) are the function `char_at` in the implementation.

## Character of a relative tensor product

Let M,N be two simple bimodules. Fix an output representative t and
`a∈K_t`, and set b=t^{-1}at. In the degree-t fiber of `M⊗_A N`, choose
right-H-coset representatives u from the support of M and set v=u^{-1}t.
Only terms with v in the support of N occur. The balanced tensor-product
relation is

\[
R_hm_u\otimes n_v
=\omega(u,h,v)\,m_u\otimes L_hn_v.
\tag{5}
\]

A summand contributes to the trace of `R_b^{-1}L_a` precisely when a
stabilizes uH. Put h=u^{-1}au∈H. Using (2),(5) and the three-cocycle
identity, its contribution is

\[
\frac{\omega(u,h,v)}
{\omega(a,u,v)\omega(u,v,b)}\,
\chi^M_u(a)\chi^N_v(h).
\]

Therefore

\[
\chi^{M\otimes_A N}_t(a)
=\sum_{\substack{uH\subset\operatorname{supp}(M)\\
                  u^{-1}t\in\operatorname{supp}(N)\\
                  u^{-1}au\in H}}
\frac{\omega(u,u^{-1}au,u^{-1}t)}
{\omega(a,u,u^{-1}t)\omega(u,u^{-1}t,t^{-1}at)}
\chi^M_u(a)\chi^N_{u^{-1}t}(u^{-1}au).
\tag{6}
\]

For clarity, before applying the three-cocycle identity the extra scalar
from the last right action is
`ω(u,hv,b^{-1}) ω(v,b,b^{-1}) / ω(t,b,b^{-1})`.
Since hv=vb and uv=t, the cocycle identity reduces this to
`1/ω(u,v,b)`, yielding (6). This checks the inverse-right-action phase,
which is easy to miss in a twisted calculation.

All these characters have the same multiplier α_t. Thus the multiplicity
of the simple (t,ρ) is the ordinary projective-character inner product

\[
N_{M,N}^{(t,\rho)}=
\frac1{|K_t|}\sum_{a\in K_t}
 \chi^{M\otimes_A N}_t(a)\overline{\chi_\rho(a)}.
\tag{7}
\]

No numerical approximation is used. The implementation accumulates powers
of ζ8 as eight integer coefficients and reduces with ζ8^4=-1. The result
must have zero coefficients of ζ8,ζ8²,ζ8³ and an integer constant divisible
by |K_t|. It also checks nonnegativity, the unit, all associativity
identities, and every source coefficient under the stated basis map.

## Replay artifacts and interpretation

* `s5_schur_data.g` builds S5, its Schur cover and an explicit section.
* `s5_schur_data.json` records the group table, the mod-two section
  cocycle, the sign, the subgroup and its C2 projection. The replay uses
  this finite data and does not require GAP.
* `s5_relative_twist.py` verifies coherence, constructs (1)--(7) in exact
  cyclotomic arithmetic, and matches the source tensor.
* `s5_relative_twist.json` records the actual adjusted cocycle, the
  trivializing cochain, all stabilizers, full tensor, hash and basis map.

The fact that this is group-theoretical supplies unitarizability; more
directly, ω and ψ already have unit modulus, so this is the unitary
bimodule construction in the pointed unitary category Vec_G^ω.

The character formulas above are derived here from the algebra/module
axioms; they are not attributed as verbatim formulas of a paper. For the
standard group-theoretical category construction see ENO,
*Weakly group-theoretical and solvable fusion categories*, Section 2.5
and the group-theoretical constructions in Section 2.13:
https://arxiv.org/pdf/0809.3031 . For general complete unitarity of
group-theoretical categories, see Galindo--Hong--Rowell,
*Generalized and quasi-localizations of braid group representations*,
Theorem 5.20: https://people.tamu.edu/~rowell/GHRarx1.pdf .
