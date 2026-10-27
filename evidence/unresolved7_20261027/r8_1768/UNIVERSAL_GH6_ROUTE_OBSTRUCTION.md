# A Frobenius-parity obstruction to every proposed GH(C6,2), 1+sigma route

## Scope and conclusion

No categorification of R8_3_1768 can be obtained as the bimodule dual of
a category with the `GH(C6,2)` fusion rules, by a
connected separable algebra on any object `1+g^j sigma`.

This applies to **every associator**, not only the
specific RW precursor. It therefore supersedes the precursor-specific
wrong-dual argument as an obstruction to this particular proposed route.
It does **not** exclude R1768 itself: no theorem forces every
categorification of that ring to arise by this route.

The key is a general parity condition for a pivotal Frobenius functor.
It transports a nondegenerate selfduality pairing, not the numerical
Frobenius--Schur indicator.

## 1. Pairing parity for pivotal Frobenius functors

Let `F:D -> C` be a linear pivotal Frobenius monoidal functor between
pivotal semisimple rigid categories. A Frobenius monoidal functor
preserves duals: its canonical comparison

\[
        F(V^*)\xrightarrow{\sim}F(V)^*
\]

is invertible. The pivotal condition makes this comparison commute with
the pivotal transpose. Consequently a selfduality isomorphism
`f:V -> V*` with transpose `f^t=epsilon f`, `epsilon in {+1,-1}`,
gives a selfduality isomorphism of `F(V)` of the same sign.

Equivalently, if `b:V tensor V -> 1_D` is the corresponding pairing,
the transported pairing is

\[
 F(V)\otimes F(V)\xrightarrow{F_2}F(V\otimes V)
 \xrightarrow{F(b)}F(1_D)\xrightarrow{F^0}1_C.
\]

Its inverse copairing uses the comonoidal structure and the unit map.
The two snake equations are precisely the Frobenius interchange
identities together with the snakes for `b`. Thus no strong-monoidal
hypothesis is necessary here, and nondegeneracy is not being assumed
merely from nonvanishing of the displayed composite.

If a selfdual simple `X` of `C` has indicator `delta`, its isotypic
component in an `epsilon`-paired object carries a nondegenerate
bilinear form on its multiplicity space of sign `epsilon/delta`.
When `epsilon != delta` this form is alternating, so the multiplicity
of `X` is even. In particular, an object with a negative-sign pairing
cannot contain a positive-indicator selfdual simple exactly once.

For a symmetric separable Frobenius algebra `A` in a pivotal fusion
category `H`, the forgetful functor

\[
                U:{}_A H_A\longrightarrow H
\]

has precisely this pivotal Frobenius structure. Its monoidal map is the
projection onto tensor product over `A`; the comonoidal map is the
separability inclusion; the unit and counit are those of `A`. The
induced duality and pivotal structure on bimodules are the usual ones.

This is stated explicitly in Mulevicius, *Condensation inversion and
Witt equivalence via generalised orbifolds*, TAC 41 (2024), Example
4.18. The preceding paragraph assumes only a pivotal multifusion
category and a symmetric separable Frobenius algebra, not a braiding.
The full primary-source text is available in the preprint as Example
4.15, with the definition and duality comparison in Definitions 4.1
and 4.3: <https://arxiv.org/html/2206.02611v1>.

## 2. The positive spherical setup covers arbitrary original complex categories

Suppose the proposed Morita realization of a categorification `C` of
R1768 exists. The previously verified general-complex gate gives a
Galois transport of `C` that is pseudo-unitary. Transport the actual
Morita context and the algebra at the same time. Its other fusion
category `H` is also pseudo-unitary, by Morita invariance of categorical
global dimension and FP dimension.

Use the canonical positive spherical structures. A semisimple module
category over a pseudo-unitary fusion category has a positive module
trace (Schaumann, Proposition 5.8), which equips the internal end of
each simple module with a symmetric special Frobenius structure.
The algebra `A`, as the internal end of its simple regular module, has
such a structure. Its multiplication and underlying object are the
original ones, up to algebra isomorphism.

There is also the direct symmetry criterion: a haploid algebra of
nonzero pivotal dimension is symmetric for any counit, Schaumann,
Lemma 2.9. Here `dim(A)=1+u>0`.

The induced pivotal dimension of an `A`-bimodule `M` is
`dim_H(U(M))/dim_H(A)>0`; thus the induced pivotal structure is the
canonical positive one on the Morita dual. Indicators and the pairing
parity in section 1 are therefore being compared in the same pivotal
structures. No unitarity assumption has been added.

## 3. Total second indicator forces all six GH simples to be positive

Put `u=6+sqrt(37)`. In `H`, the simples are `g^j` and `b_j=g^j sigma`,
for `j in C6`, with

\[
 g^j b_k=b_{j+k},\quad b_k g^j=b_{k-j},\qquad
 b_jb_k=g^{j-k}+2\sum_t b_t.
\]

All `b_j` are selfdual and have positive dimension `u`. Write
`epsilon=nu_2(g^3) in {+1,-1}`. The unit has indicator plus one and
the other four invertibles have zero indicator. The pointed contribution
to the dimension-weighted total second indicator is `1+epsilon`.
No pointed associator class is assumed.

The known necessary indicator theorem for R1768 gives

\[
 \nu_2(1)=1,\quad\nu_2(g_C)=-1,\qquad
 \nu_2(X_i)=1\quad(i=2,\ldots,7).
\]

Its six noninvertible dimensions are
`u-1,u,u+1,u+1,u,u-1`. Thus

\[
                  T_2(C)=\sum_X\dim(X)\nu_2(X)=6u.
\]

In canonical positive spherical structures this weighted total is
Morita invariant, because

\[
 T_2(C)=\frac1{\dim(C)}
  \sum_{Z\in\operatorname{Irr}Z(C)}\dim(Z)^2\theta_Z^2.
\]

Consequently

\[
            1+\epsilon+u\sum_{j=0}^5\nu_2(b_j)=6u.
\]

The irrationality of `u` first forces `epsilon=-1` and then forces the
sum of the six large indicators to be six. Every summand is plus or
minus one, so

\[
                      \boxed{\nu_2(b_j)=+1\text{ for every }j.}
\]

## 4. The quaternionic invertible of R1768 cannot forget to a bimodule

Let `Q` be the unique nontrivial invertible simple in the putative
R1768 dual. It is selfdual and has `nu_2(Q)=-1` in its canonical
positive pivotal structure. Since `Q` is invertible,

\[
                 \dim_H U(Q)=\dim_H A=1+u.
\]

Every simple of `H` has FP dimension either one or `u`. Since `u` is
irrational, the nonnegative integral dimension equation
`a+b u=1+u` forces `a=b=1`. In particular, for some indices `j,k`,

\[
                     U(Q)=g^j\oplus b_k.
\]

The pivotal Frobenius forgetful functor transports the negative-sign
pairing of `Q` to a nondegenerate negative-sign pairing on this object.
But its selfdual simple constituent `b_k` has indicator plus one and
occurs exactly once. Section 1 requires its multiplicity to be even.
This is the contradiction.

Notice that this proof needs neither the trivalent multiplication
coefficients, a classification of algebra automorphisms, nor a module
Gram factorization. It covers all associators in the stated route and
all translated choices of `sigma`. It also explains, categorically, why
finding an associative algebra in a new RW precursor cannot by itself
overcome the problem.

More generally, if `dim_H(A)=a+b u` for nonnegative integers `a,b` and
`b` is odd, this same reasoning excludes R1768 as the bimodule dual.
Indeed `U(Q)` has total multiplicity `b` among the six positive-indicator
large simples; a negative-sign pairing requires every one of those
multiplicities to be even. This odd-coefficient criterion closes a
larger class of algebra routes at once.

## 5. The remaining scope gap

The existence of a categorification of R1768 has not been shown to force
the particular Morita context in this note. Earlier work constructs
only commuting based actions for that context. Therefore the theorem
closes a substantial construction route and leaves the census case
unresolved. Treating it as a general exclusion would repeat precisely
the error of promoting necessary based data to categorical existence.

## References and source bindings

* G. Schaumann, *Traces on Module Categories over Fusion Categories*,
  arXiv:1206.5716v3, Lemma 2.9, Proposition 5.8, and the internal-end
  symmetric Frobenius correspondence in section 6:
  <https://arxiv.org/pdf/1206.5716>.
* V. Mulevicius, *Condensation inversion and Witt equivalence via
  generalised orbifolds*, TAC 41 (2024), Example 4.18:
  <https://www.tac.mta.ca/tac/volumes/41/36/41-36abs.html>;
  preprint <https://arxiv.org/abs/2206.02611>.
* R1768 indicator theorem: `manuscripts/rank8/paper/m3_creative_20261022.tex`,
  Proposition `creative-r1768-sector`, and the exact replay in
  `evidence/rank8_creative_20261022/r1768/`.
* The pointed class and the eight-object module factor:
  `evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/`
  `rank8_quadratic_pair/GH6_ROUTE.md`, sections 1 and 4.
* General-complex gate: existing rank-eight pivotality/sphericalization
  proof; its conclusion is used only after transporting the complete
  hypothetical Morita context.

No long computation enters the new argument.
