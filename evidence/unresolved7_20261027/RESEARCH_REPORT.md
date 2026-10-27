---
title: "Seven unresolved fusion rings: audit and theoretical continuation"
subtitle: "The three previous exclusions are retained; seven problems remain open"
date: "27 October 2026"
geometry: margin=22mm
fontsize: 11pt
colorlinks: true
linkcolor: blue
urlcolor: blue
---

## Outcome

The fresh review retains the general-complex exclusions of
**R9\_2\_1607, R9\_2\_1975, and R9\_2\_1976**. It found no gap requiring
their withdrawal. The inherited spherical/Galois and Morita reductions
remain explicit dependencies of these conclusions.

This continuation gives **no additional complete census-ring exclusion
and no new census-ring model**. All seven requested rings remain
unresolved. Each was investigated separately; the new results below
include categorical restrictions and exclusions of construction routes,
which must not be counted as exclusions of the rings themselves.

| Ring | Principal additional result | Census status |
|:--|:--|:--|
| R6\_4\_155 | Nonpointed algebra family reduced to two cases; one algebra is forced but returns to a known module category. | Unresolved |
| R6\_8\_1660 | One center subcase removed; a pairing obstruction also tests proposed Morita realizations. | Unresolved |
| R8\_3\_928 | Its nonpointed modular centralizer must be simple, with only one nontrivial connected étale algebra. | Unresolved |
| R8\_3\_941 | Its rank-22 fermion centralizer must be nonsplit and have no proper nonpointed fusion subcategory. | Unresolved |
| R8\_3\_1154 | All six third indicators are forced to be 2; all six trivalent rotations are identity. | Unresolved |
| R8\_3\_1768 | A pairing obstruction rules out the higher-Haagerup Morita construction family. | Unresolved |
| R9\_2\_137 | A nonpointed algebra is forced, but returns to an existing Morita route; both TY signs pass the strengthened exact test. | Unresolved |

The source snapshot is the classification repository at
`6a426acf6465dd674351be92dcca41b72f371521`. This is offline research:
no online repository, website, manuscript release, or classification
ledger was changed. The computations in this pass were short exact
replays or bounded certificate-discovery tests, not long associator searches.

## 1. Fresh audit of the three exclusions

For **R9\_2\_1975**, the review checked the opposite-bimodule and
normalizer conventions, cancellation for arbitrary complex cocycles,
the strict even-$V_4$ subgroup used in the projective parity argument,
and the normalized character formula for the distinguished Galois
central object. The required restriction remains

\[
F(B)=1+X_0+X_1+X_2+X_3.
\]

In the rotation branch its multiplicity at $X_0$ is odd, whereas the
forced anticommuting stabilizer operators require it to be even.
Reflection shifts are separately impossible. The audit preserves the
eighth-root coboundary witness: a fourth-root-only test would be invalid.
The inherited extreme-branch argument and complete signed gate were
also checked as stated dependencies. The fresh gate replay retained two
branches and certified completeness.

For **R9\_2\_1607 and R9\_2\_1976**, the review specifically checked
that pivotal symmetry of the Frobenius pairing, rather than merely
braided commutativity, is available. The selfdual multiplicity-one
Galois summand of the canonical algebra has a symmetric nondegenerate
pairing. Transporting that pairing forces all four large second
indicators in the zero-shift Morita category to be $+1$.
The dimension-weighted second-indicator total is Morita invariant.
Comparison of irrational coefficients then forces the same sum to be
four in the original category. The original rings have, respectively,
only two and zero selfdual large simples. This is the contradiction.
The irrational-coefficient comparison avoids a dependence on TY sign
conventions. Both complete signed gates were replayed successfully.

These arguments do not assume that arbitrary tensor functors preserve
numerical indicators. Their pairing transport and Morita-invariant
total are different, explicitly justified steps. Full fresh reviews are
`audit_parity/AUDIT_R1975.md` and `audit_fs2/AUDIT.md`.

## 2. A useful common obstruction: pairings under Morita forgetful functors

Let $\mathcal C$ be pseudo-unitary, and let $A$ be a connected separable
algebra. With its positive module trace, $A$ can be equipped with the
compatible symmetric separable Frobenius structure. The functor

\[
U:{}_A\mathcal C_A\longrightarrow\mathcal C
\]

is pivotal Frobenius monoidal. It preserves a chosen nondegenerate
pairing and its pivotal symmetry sign. In particular, if a selfdual
simple bimodule $Q$ has second indicator $\varepsilon$, then every
selfdual simple constituent of $U(Q)$ having the opposite indicator
must occur with even multiplicity.

Indeed, on such an isotypic block the multiplicity space must carry a
nondegenerate alternating form. Its dimension is even. This supplies
a short necessary test for proposed Morita restrictions. It does not
assert equality of the numerical indicators of $Q$ and $U(Q)$.

The positive pivotal normalization matters. The bimodule dimension is
$\dim_{\mathcal C}(U(Q))/\dim_{\mathcal C}(A)$, so the induced structure
is the canonical positive one. The relevant primary inputs are
Schaumann, *Traces on module categories over fusion categories*,
Proposition 5.8 and Theorem 6.6, and Mulevičius, *Condensation inversion
and Witt equivalence via generalised orbifolds*, Example 4.18.

## 3. R6\_4\_155: forced algebras and a Morita loop

Write the invertibles as $1,h,g,hg$, and the other simples as $X,Y$,
with $X^*=Y$, $hX=X$, $gX=Y$, and

\[
XY=1+h+4(X+Y),\qquad X^2=Y^2=g+hg+4(X+Y).
\]

Put $d=4+3\sqrt2$. Consider a connected separable algebra with
underlying object $A_k=1+kX+kY$. Four free pointed modules are simple
and distinct. Subtracting them from the induction Gram matrix leaves
nonnegative integral vectors $a,b$ with

\[
\|a\|^2=\|b\|^2=1+8k-4k^2,\qquad a\cdot b=8k-4k^2.
\]

Thus $k\le2$. At $k=1$ the only viable residual modules have underlying
objects $2X+Y$ and $X+2Y$. The other Gram possibilities would contain
a module with underlying object $X$, whose internal end would have
dimension $2+4\sqrt2/3$, not an algebraic integer. At $k=2$ the two
residual modules have underlying objects $X$ and $Y$. Each surviving
case has a unique necessary based module of rank six.

There is also a conditional existence statement. The canonical
central subalgebra corresponding to the pointed subcategory has
underlying central object $1+B$, where $B$ is the Galois-unit object.
Its forgetful algebra splits through its augmentation as

\[
F(1+B)\cong1\times A_2,\qquad [A_2]=1+2X+2Y.
\]

So $A_2$ is forced in any hypothetical categorification. However the
residual module underlying $X$ has internal end $1+h$. This returns
to the already available pointed-algebra module category and supplies
neither a construction of the original category nor a contradiction.
The potentially different algebra $A_1$ is not forced or constructed.

An initially tempting trace contradiction was rejected during review:
the trace on the four pointed free modules must be included. The total
is eight, not four. The accepted proof and replay are
`audit_fs2/R155_ALGEBRA_REDUCTION.md` and its companion verifier.

## 4. R6\_8\_1660: a narrower valid center restriction

The two remaining possibilities for the negative charge-conjugation
representation meeting the four spin phases were

\[
(16,2)\oplus(20,2),\qquad (44,2).
\]

The second possibility cannot occur in low frame 0. In that frame all
high restriction columns have equal $X$ and $gX$ multiplicities.
The phase-12 Gram identities force exactly one column there. It is
selfdual, leaving no negative charge-conjugation line at that phase,
whereas $(44,2)$ requires one.

A proposed extension to all of frame 1 failed independent checking.
The total asymmetric-column budget is eight, not four; the earlier
four counted only one member of each pair. The remaining budget can
support phase-36 columns that change an apparent half-integral
Verlinde entry to the integer zero. Additional negative irreducibles
away from the spin phases also cannot be omitted. Thus the entire
$(44,2)$ branch is not excluded, and both overall alternatives remain.

The pairing test in Section 2 does exclude two specific proposed
Morita module realizations, labelled `III_mixed0` and `IV_mixed1`.
A selfdual simple of their respective duals would restrict to
$\sigma+T$ and $X+gX+\sigma+T$. Here $\sigma$ has indicator $-1$
and every other displayed simple has indicator $+1$. Their odd
multiplicities cannot carry a pairing with a single symmetry sign.
The conditional route to R941 passes this test and is retained.

There is also a further rigidity condition: fusion by one distinguished
Galois-unit simple acts on the negative charge-conjugation space as a
signed permutation. Its eigenvalues there are $\pm1$; in the normalized
dual-difference basis it is a symmetric integral matrix whose square
is identity. Hence each row has precisely one entry $\pm1$.
This has not yet yielded a contradiction.

No forced algebra or categorical realization resolving R1660 was found.
The independent reviews are `audit_fs2/R1660_SPIN_AUDIT.md` and
`audit_fs2/R1660_BIMODULE_PARITY_AUDIT.md`.

## 5. R8\_3\_928 and R8\_3\_941: simple centralizers

Let $D$ be their common global dimension. Their only proper nontrivial
fusion subcategory is pointed of rank two. Consequently any central
fusion subcategory containing a nonintegral object forgets dominantly
onto the whole source category and has dimension at least $D$.
Equality would make the source braided, impossible for these
noncommutative rings.

For **R928**, write its center as $S\boxtimes\mathcal B$, where $S$
is Semion and $\dim\mathcal B=D^2/2$. The unit is the only integral
simple in $\mathcal B$. A proper nontrivial subcategory and its
centralizer would both dominate the source. Their dimensions would
therefore have product at least $D^2$, contradicting the centralizer
formula $D^2/2$. Thus $\mathcal B$ is **simple**, not just indecomposable
as a tensor product. Its possible ranks are 17, 20, and 23.

The earlier all-module rigidity theorem implies a further statement:
the entire center has exactly three connected étale algebra classes,
forming $1\subset A\subset I(1)$, with $\dim A=D/2$.
The factor $\mathcal B$ contains exactly one nontrivial such algebra,
namely $A$, and

\[
\mathcal B_A\simeq\mathcal C,\qquad
\mathcal B_A^0\simeq S^{\rm rev}.
\]

For **R941**, the fermion centralizer $\mathcal E$ has rank 22,
dimension $D^2/2$, and integral part exactly sVec. It cannot split as
$\mathcal M\boxtimes\mathrm{sVec}$: that would make the center have
rank 33 or 44, whereas the complete retained list gives 34, 37, 40, or
43. The same dominant-image and centralizer argument then proves that
its only fusion subcategories are Vec, sVec, and $\mathcal E$.

These results sharply specify the missing modular or slightly
degenerate categories, but do not prove them nonexistent. The current
*Anyon Atlas* was checked; its higher-rank numerical search is not
certified exhaustive and cannot justify exclusion by absence. The
full proofs and exact rank checks are in `r8_928_941/REPORT.md`.

## 6. R8\_3\_1154: every trivalent rotation is identity

The preceding actual equivariantization reduction gives a hypothetical
rank-ten category with a central sign object $u$ and lifts $x,ux$ of
$X_4$, satisfying $x^*=ux$. For odd $n$, the two character subspaces of
$\operatorname{Hom}(1,X_4^n)$ are the rotations on
$\operatorname{Hom}(1,x^n)$ and $\operatorname{Hom}(1,(ux)^n)$.
Spherical duality gives equal indicators of $x$ and $x^*$. Therefore

\[
\nu_n(X_4)=2\nu_n(x)\quad(n\text{ odd}).
\]

The same holds for $X_5$. Their lift's cubic vacuum spaces are
one-dimensional, so their third indicators lie in
$\{2,2\zeta_3,2\zeta_3^2\}$. This is stronger than allowing an arbitrary
sum of two cube roots.

Applying these discrete possibilities to the three already retained
center patterns forces both indicators to be two. Duality, the inner
autoequivalence, and a second small discrete check then force

\[
\boxed{\nu_3(X_i)=2\quad
i=1,2,4,5,6,7.}
\]

Each of these six cubic spaces is two-dimensional. Since its rotation
has order three, trace two means that the rotation is the identity.
All 33 excluded discrete branches have exact integer separating
certificates; the six retained branch records have exact rational
feasibility witnesses. An independent implementation checked them.
No center pattern is eliminated outright.

The theorem and solver-free replay are in
`r8_1154/ODD_ROTATION_THEOREM.md`; the independent audit is in
`audit_parity/AUDIT_R1154_ODD_ROTATION.md`.

A second short argument proves that the integral part of its center
is Vec. An integral central simple could forget only to copies of
$1$ and $g$, but $g$ is not central in the fusion ring, forcing its
coefficient to vanish. The full adjoint subring then makes every
central object supported on the unit trivial. This applies directly
to arbitrary complex categorifications. It rules out nontrivial
finite-group extensions and equivariantizations throughout the
Morita class. In the auxiliary rank-ten category, the integral center
is exactly double Semion; its unique nontrivial Tannakian subcategory
only gives back the already known descent.

Three further direct central-condensation families are ruled out:
$\mathrm{Fib}^{\boxtimes6}$,
$GH(C_4,1)\boxtimes\mathrm{Fib}^{\boxtimes3}$, and
$GH(C_4,1)^{\boxtimes2}$, with arbitrary pointed factors. In the last
case, the required index-three subgroup contains a central $C_4$;
its condensation would force the impossible rank-two rule
$x^2=1+4x$. These are specified-family obstructions, not a
classification of every possible construction.

## 7. R8\_3\_1768: a uniform higher-Haagerup obstruction

Put $u=6+\sqrt{37}$. The positive source indicators are
$(1,-1,1,1,1,1,1,1)$, and its weighted second-indicator total is $6u$.
In a category with $GH(C_6,2)$ fusion rules, the six large simples are
selfdual of dimension $u$. The pointed contribution to that total is
$1+\nu_2(g^3)$. Morita invariance and irrationality force

\[
\nu_2(g^3)=-1,\qquad
\nu_2(g^j\sigma)=+1\quad(0\le j<6)
\]

whenever such a category is Morita equivalent to R1768.

First consider the proposed algebra $A=1+g^j\sigma$. The negative
invertible of the R1768 dual has underlying dimension $1+u$ in the
higher-Haagerup category. Irrationality forces its underlying object
to contain one pointed and one large simple, each once. Its negative
pairing cannot restrict to the latter, whose second indicator is
positive. Section 2 gives a contradiction. This rules out the route
for **every associator**, not only the original arithmetic precursor.

A stronger use of the same parity principle applies on the R1768
side. For a negative selfdual simple in a Morita dual, all six positive
nonpointed source constituents must occur evenly. Thus the
$\sqrt{37}$ coefficient of its underlying dimension must be even.
The complete previously retained list has 21 possible module factors.
In 17 of them, some simple module has internal end with an odd such
coefficient. Choosing that simple as generator prevents its dual from
having a negative-indicator invertible. Each of the other four factors
has a dimension-one internal end, so its module category is regular.

It follows that a Morita representative with a negative-indicator
invertible must come from the regular module category, and hence have
rank eight.
In particular **no category with $GH(C_6,2)$ fusion rules is Morita
equivalent to it**. This eliminates the entire higher-Haagerup Morita
family, including other algebras in that family. It does not eliminate
an unknown R1768 category itself.

A second exact RW arithmetic input was also found during the
construction attempts:

\[
\gamma=\begin{pmatrix}85&144\\36&61\end{pmatrix}.
\]

It supplies another concrete input for a twisted precursor, without
proving inequivalence to the old one. The new uniform obstruction
explains why that possible change cannot solve R1768 through Morita
equivalence. The exact parity filter and full categorical premises are
recorded in the `r8_1768/` evidence.

## 8. R9\_2\_137: a forced algebra does not supply a new category

In its remaining zero-shift rank-twelve Morita category, let
$S=\sum_qX_q$, $d=4+3\sqrt2$, and $z$ be the central involution of
the pointed $D_8$. The canonical étale subalgebra associated to the
pointed subcategory is forced to be $1+B$, where $B$ is the Galois-unit
simple. Its forgetful algebra has augmentation and splits as

\[
F(1+B)\cong1\times A,\qquad [A]=1+S.
\]

Thus this nonpointed algebra is forced, not merely a speculative
construction. Its induction Gram, however, gives eight modules
underlying $g+S$ and four underlying $X_q$. Each of the latter has
internal end $1+z$. The module category is therefore the one already
obtained from the central-involution algebra. This is a Morita loop,
not a realization of a presently hypothetical category.

The previously established positive second indicators were then
inserted into both remaining TY-sign center systems. Each has an
exact nonnegative rational witness, with support 102 and 97,
respectively. The complete short tests took under four seconds each;
the saved witnesses replay without an optimizer. They show that this
combination of constraints still does not exclude the ring.

The proof, source bindings, matrices, and witnesses are in
`audit_parity/R137_CONTINUATION.md` and its companion files.

## 9. Scope of the remaining problems

No based module, modular-data candidate, precursor category, or
feasible indicator witness has been promoted to a model of a census
ring. The missing ingredients are still actual categorical
constructions or complete obstructions for the surviving cases.
The report separates accepted theorems, inherited premises, and
rejected shortcuts so that the next investigation can start from the
stronger frontier without repeating invalid inferences.

### Primary references used for the new arguments

* Davydov, Müger, Nikshych, Ostrik, *The Witt group of non-degenerate
  braided fusion categories*: <https://arxiv.org/abs/1009.2117>.
* Drinfeld, Gelaki, Nikshych, Ostrik, *On braided fusion categories I*:
  <https://arxiv.org/abs/0906.0620>.
* Schaumann, *Traces on module categories over fusion categories*:
  <https://arxiv.org/abs/1206.5716>.
* Mulevičius, *Condensation inversion and Witt equivalence via
  generalised orbifolds*: <https://arxiv.org/abs/2206.02611>.
* Ng, Schauenburg, *Frobenius-Schur indicators and exponents of
  spherical categories*: <https://arxiv.org/abs/math/0601012>.

