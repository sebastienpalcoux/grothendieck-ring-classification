# Exact connected-algebra and Morita-profile closure for four quadratic rings

This is a **new necessary-condition calculation**, dated 2026-10-21. It does
not alter the frozen frontier or center-addendum evidence, and it makes no new
ring-exclusion or categorification claim. The conditions apply to fusion
categories over the complex numbers; they do not require a braiding, pivotal
structure, pseudo-unitarity, or unitarity.

The subsequent reviewed theorem in [POINTED_COCYCLE.md](POINTED_COCYCLE.md)
proves that R65 cannot have a trivial pointed associator. It excludes its two
rank-two categorical module actions and four further algebra objects. The
combined totals are **144 algebra objects, 178 induction factors, and 30
fully determined action classes**. The table below preserves the arithmetic
closure stage before that categorical refinement.

The saved complete finite domains of connected separable algebra **underlying
objects** are refined by integral induction Gram factorization, compatibility
with module action, and closure under internal endomorphism algebras. A
surviving object has not been supplied with a multiplication or associator.

| Ring | Previous algebra objects | Objects after exact Gram factorization | Objects after arithmetic closure | Arithmetic induction factors | Canonical module dimension profiles | Fully determined action classes |
|---|---:|---:|---:|---:|---:|---:|
| `R8_3_65` | 30 | 30 | 12 | 12 | 6 | 6 |
| `R8_3_1768` | 115 | 99 | 49 | 61 | 18 | 9 |
| `R8_3_1795` | 87 | 81 | 55 | 67 | 18 | 12 |
| `R8_3_3472` | 70 | 70 | 32 | 42 | 9 | 5 |
| Total | 302 | 280 | 148 | 182 | 51 | 32 |

Thus **154 previously necessary algebra-object candidates are now impossible**.
The 4,284 complete integral induction factorizations reduce to 182. Of the
remaining factors, 75 determine the full module action uniquely. Modulo
permuting module simples, these give the 32 based-module actions in
`action_classes.json`. The other 107 factors remain necessary candidates:
full action completion has not been proved or disproved for them.

For `R8_3_65` the result is stronger: all twelve surviving factors have full row
rank. Consequently every indecomposable semisimple module category over any
categorification would have one of **exactly six possible based-module actions**,
with ranks `2, 2, 4, 4, 8, 8`. Every listed action satisfies all fusion identities
and transpose duality. This is a complete list of possible actions, **not** a
classification or existence theorem for categorical module structures.

The six R65 actions admit a uniform description. The invertible generator of
C4 has exactly two equally sized orbits, of size t=1,2,4. On their
orbit-constant vectors, the self-dual noninvertible generator has one of

`[[0,1],[1,11]]` or `[[3,5],[5,8]]`.

For each of these two quotient matrices and each of the three orbit sizes,
there is exactly one action in the complete list, up to module-basis
permutation. Thus both previously known rank-two patterns extend uniquely at
the level of based-module actions to ranks four and eight. The exact orbit
decompositions and all action matrices are saved in `action_classes.json`.
This statement does not provide categorical lifts of these actions.

For the other rings the fully determined action ranks are:

- `R8_3_1768`: `2, 3, 3, 4, 4, 4, 6, 6, 8`.
- `R8_3_1795`: `2, 2, 4, 4, 4, 4, 6, 6, 6, 6, 8, 8`.
- `R8_3_3472`: `2, 2, 5, 5, 8`.

## Mathematical basis

Write the fusion tensor as `R[i][j][k]=[X_i X_j:X_k]`, with unit `X_0`,
Frobenius–Perron dimensions `d_i`, and right-multiplication matrix
`N_A[i,j]=[X_i A:X_j]`. Let `A=sum a_i X_i` be a connected separable algebra.
The category of right A-modules is an indecomposable semisimple module category.
The regular module A is simple because `dim Hom_A(A,A)=dim Hom(1,A)=1`.
Moreover `a_i=a_(i*)`: the diagonal coefficient of the action of X_i on A
equals that for its transpose-dual X_i*. Thus A is self-dual as an object,
and `N_A=N_A^t`, fixing the Gram orientation.

Let `B[r,i]=[X_i tensor A:M_r]`, taking `M_0=A`. Frobenius reciprocity gives

`B^t B=N_A`, and `B[0,:]=a`.

Every module simple occurs in some induced object, so no row is zero. Removing
the distinguished row gives a nonnegative integral Gram factorization of

`G=N_A-a a^t`.

**Complete finite Gram enumeration.** Every remaining row v lies in the row
space of G and satisfies `v v^t <= G`. Choose a full-rank principal block
`H=G[P,P]`. Then

`v=v_P H^{-1}G[P,:]`, and `v_P H^{-1}v_P^t <= 1`.

In particular `0 <= v_i <= floor(sqrt(G[i,i]))`. The program enumerates every
integer pivot vector in this finite box, reconstructs v exactly, and checks
nonnegativity, integrality, and the ellipsoid bound. A type v can occur at most
`min_i floor(G[i,i]/v_i^2)` times, over its nonzero coordinates. All
factorizations are therefore exactly the bounded nonnegative integer solutions
of `sum_v n_v v_i v_j=G[i,j]`. Rational row reduction followed by complete finite
integer enumeration finds **all** solutions. Branches are pruned only by exact
remaining linear-contribution bounds. There is no time or node cutoff.

The numerical solver in `gram_discovery.py` was used only during discovery.
Its infeasibility reports are never accepted as mathematical obstructions.
`integral_gram.py` and the certificate verifier use exact arithmetic.

**Necessary action rows.** If `M_i` is the matrix for left tensoring by X_i,
then

`M_i B=B R_i^t`, `M_i[r,0]=B[r,i]`, `M_{i*}=M_i^t`.

Each entry of M_i is at most `floor(d_i)`: the nonnegative matrix
`M_i M_i^t=M_i M_{i*}` has spectral radius `d_i^2`, because it has the positive
module dimension vector as eigenvector. Its diagonal entries are row square
norms. This argument is about the integral based module and does not assume
unitarity.

Rows of B of the same type are aggregated. For an active type u and a simple i,
the residual action must express

`u R_i^t-u_i a`

as a nonnegative integer combination of the other row types v. The coefficient
of a type repeated n_v times is at most `n_v floor(d_i)`, and is also bounded
coordinatewise by the target vector. Every rejected system is enumerated
exactly. A successful row decomposition is only a necessary condition: it
does not establish a common set of matrices satisfying multiplication.

This step leaves respectively 30/280, 97/933, 81/1137, and 69/1303
objects/factors for R65, R1768, R1795, and R3472.

**Internal-end closure.** Every simple module M_r has a connected separable
internal endomorphism algebra `A_r=internalHom(M_r,M_r)` in the original
category. Canonically normalized module dimensions satisfy

`FPdim(internalHom(M,N))=FPdim(M) FPdim(N)`.

Since `internalHom(A,M_r)` has underlying dimension `B[r,:] dot d` and
`internalHom(A,A)=A`, one obtains the exact necessary identity

`FPdim(A_r)=(B[r,:] dot d)^2 / FPdim(A)`.

The right hand side must be the dimension of one of the surviving algebra
objects. Iterating removals is sound: if the actual A exists, all its actual
internal-end algebras remain in every sound preceding stage. The formula and
canonical normalization are given in Etingof–Nikshych–Ostrik,
[Fusion categories and homotopy theory, Section 2.5 and Proposition 2.2](https://ems.press/content/serial-article-files/36746)
([arXiv:0909.3140](https://arxiv.org/abs/0909.3140)).

There is a stronger closure condition. The entire multiset

`{ (B[r,:] dot d)^2 / FPdim(A) : r }`

is independent of the distinguished simple chosen to present the same module
category. Every member of this multiset must occur as the root algebra dimension
of another surviving induction factor **with exactly the same multiset**.
`profile_closure.py` performs this test. It removes ten more factors after
individual dimension closure, without removing further objects.

**Trace consistency.** For each surviving profile, the diagonal object at each
module simple must be among the compatible rebased algebra candidates. All
multisets of such diagonal objects are enumerated. Their coefficient sum is
the character `Tr(M_i)` of the integral representation of the fusion ring.
Rational primitive central idempotents are computed exactly from a separating
linear combination of fusion matrices. Their traces must be nonnegative
integer multiples of their field degrees; the Frobenius–Perron orbit has
multiplicity one. Every character supported on the image of B must occur.
All remaining profiles pass this complete trace test; no additional exclusion
is claimed.

**Full row rank.** When B has independent rows, the action is forced:

`M_i=B R_i^t B^t (B B^t)^{-1}`.

The program checks exact nonnegative integrality, the unit, transpose duality,
and all 64 fusion products. All 75 full-row-rank surviving factors pass. Their
module dimension profiles restrict the basis permutations needed for exact
isomorphism comparison in `action_classes.py`.

## Scope, controls, and reproduction

The input tensor file and both old complete candidate domains are bound by
SHA-256 in `source_verification.json`. Exact dimension homomorphisms are checked
against every product. For each of the four rings and each of its eight simple
objects X, the mandatory canonical algebra `X tensor X*` and its regular-module
induction factor are verified to survive every closure and trace test: **32
positive controls**. In particular, no canonical algebra is accidentally
removed by normalization or a basis convention.

The objects `1+X` are not assumed to be algebras; the pointed associator is not
assumed trivial. No surviving induction factor, based-module action, or trace
assignment is declared to have a categorical realization. No new associator,
fusion category, or Morita equivalence is constructed here. General
categorifiability of all four rings remains unresolved.

Run from the repository root:

```sh
python evidence/rank8_next_20261021/quadratic/verify_certificates.py
python -O evidence/rank8_next_20261021/quadratic/verify_certificates.py
```

This re-enumerates every Gram factor domain, verifies every rejected action-row
system exactly, rebuilds both closure stages and trace compatibility, checks all
forced full actions and their classes, and verifies the canonical controls.
The negative certificates are sufficient for the exclusions; a row system
conservatively retained as possible does not need a feasibility certificate.
The stronger full discovery replay, including every retained action-row
system, is `verify_final.py`.

`verification_normal.txt` and `verification_optimized.txt` record the targeted
runs. Every mathematical check uses explicit exceptions, not Python `assert`,
so optimization does not remove the checks. `verification.json` summarizes the
final verified counts. No ledger or manuscript is modified by these scripts.

## Independent R721 reviews

Two separate reviews in this folder support the new R721 construction in the
adjacent research package. They do not change the unresolved status of the four
quadratic rings studied above.

- [R721_BOUND_REVIEW.md](R721_BOUND_REVIEW.md) reconstructs the exact linear
  equations for all four possible dualities and checks rational certificates
  bounding every one of the 512 fusion coefficients by three.
- [R721_CENSUS_REVIEW.md](R721_CENSUS_REVIEW.md) independently covers all 4,500
  supplied rank-eight tensors and identifies R721 as the unique ring with the
  constructed dimension multiset.

Both reviewers import no producer modules, bind their inputs by SHA-256, and
pass in normal and optimized Python with byte-identical outputs. Their scope
and separate categorical inputs are stated in the review notes.
