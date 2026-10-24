# Two unitary pullback models from the rank-five dimension-24 seed

## Result and scope

The previously unresolved rings `R9_2_1396` and `R9_2_1397` are realized by
unitary fusion categories of dimension 72. They belong to one construction
from the known unitary non-self-dual rank-five category of dimension 24,
called `LPR-24` in this project's lower-rank registry. The construction
uses its existence, not a conjectural solution of new pentagon equations.

Let `C_-` denote this known category. There is a pointed unitary fusion
category `P_-` of dimension four, with group of invertibles `V4`, and a
genuine categorical action of `S3` such that

\[
\mathcal C_-\simeq\mathcal P_-^{S_3}.
\]

This action, including all coherence data, is obtained by
Tannakian de-equivariantization of `C_-`; it is not inferred from a
permutation of a fusion ring. For either `A=C9` or `A=C3×C3`, fix a
surjection `q:A→C3`. Pull the action back along

\[
\operatorname{Dih}(A)=A\rtimes C_2\longrightarrow C_3\rtimes C_2=S_3,
\qquad (a,\epsilon)\longmapsto(q(a),\epsilon),
\]

where both involutions act by inversion. Then

\[
\begin{split}
K_0(\mathcal P_-^{\operatorname{Dih}(C_9)})&\cong R9\_2\_1396,\\
K_0(\mathcal P_-^{\operatorname{Dih}(C_3\times C_3)})&\cong R9\_2\_1397.
\end{split}
\]

The proof below establishes existence of the action. The accompanying
integer replay establishes the full two based-ring identifications.

## The published seed

Write the simple objects of `C_-` as `1,g,Y,V,W`, of dimensions
`1,1,2,3,3`. The fusion rules are

\[
\begin{gathered}
g^2=1,\quad gY=Y,\quad gV=W,\quad gW=V,\\
Y^2=1+g+Y,\qquad YV=YW=V+W,\\
V^2=W^2=g+Y+V+W,\qquad VW=1+Y+V+W.
\end{gathered}
\]

Thus `V*=W`, whereas `1,g,Y` are self-dual. These are the exact rules of
`LPR-24`. Liu–Palcoux–Ren, *Classification of Grothendieck rings of complex
fusion categories of multiplicity one up to rank six*, arXiv:2010.10264v5,
Section 4.4 gives unitary solutions for this ring (the same ring is listed
in Section 3.5). This is the sole non-elementary positive seed used here.

Its universal grading group is trivial. Indeed, the adjoint subcategory
contains `Y,V,W` because `VW=VV*=1+Y+V+W`, and it then contains `g` by
`Y²=1+g+Y`.

## A useful consequence of solvability

If a nontrivial solvable fusion category `D` has trivial universal grading,
then `D` is a nontrivial cyclic-prime equivariantization. This follows
directly from Etingof–Nikshych–Ostrik, *Weakly group-theoretical and
solvable fusion categories*, arXiv:0809.3031, Proposition 4.4(3): `D` is
obtained from `Vec` by an actual sequence of cyclic-prime extensions and
equivariantizations. The last operation cannot be a faithful nontrivial
extension, since such an extension gives a nontrivial grading. If
`D=B^{C_p}`, the canonical central Tannakian `Rep(C_p)` embeds faithfully
in `D`; consequently `p` divides the number of invertible objects of `D`.
This observation produces actual central Tannakian categories and avoids
any assumption that an arbitrary central invertible object is bosonic.

By Theorem 1.6 of the same paper, every fusion category of dimension
`p^a q^b` is solvable. Applying the observation to `C_-` (dimension 24,
exactly two invertibles) yields

\[
\mathcal C_-\simeq\mathcal B^{C_2},\qquad \operatorname{FPdim}(\mathcal B)=12.
\]

Its central `Rep(C2)` has underlying objects `1,g`. The inverse
construction is the Tannakian de-equivariantization reviewed in that
paper's Section 2.6.

## The dimension-12 category and its canonical central `Rep(C3)`

Let `F:C_-→B` be the forgetful functor from this equivariantization.
The orbit/stabilizer rules for `C2` show:

* `F(1)=F(g)=1`;
* `F(Y)=a+a^{-1}`, where `a,a^{-1}` are distinct invertibles;
* `F(V)=F(W)=X`, where `X` is simple of dimension three.

For completeness, tensoring by the nontrivial character `g` interchanges
the two lifts of a fixed simple and fixes the induced simple from a
two-element orbit. Since `gY=Y`, `Y` is induced from a two-element orbit
of one-dimensional objects; since `gV=W`, `V,W` are the two lifts of a
fixed dimension-three object. This lists every orbit. The dimension sum
`1+1+1+9=12` confirms completeness. The three invertibles form `C3`, and
applying `F` to the rules above gives

\[
a^3=1,\qquad aX=X,\qquad X^2=1+a+a^{-1}+2X.
\]

In particular `B_ad=B`. Applying the solvability observation again to
`B` gives a central Tannakian `Rep(C3)` whose forgetful functor into `B`
is fully faithful and whose underlying objects are precisely its three
invertibles.

We need the following elementary uniqueness fact. In a fusion category
with trivial universal grading, an invertible object has at most one
half-braiding up to isomorphism. To see this, compare two half-braidings
on an invertible `a`. For every simple `Z`, the object `a⊗Z` is simple,
so the two half-braidings differ by a scalar `λ_Z`. The half-braiding
identity implies `λ_T=λ_Z λ_W` whenever `T` is a constituent of `Z⊗W`.
Such scalar systems are exactly characters of the universal grading
group. When the grading group is trivial all scalars equal one.

The canonical `C2` action on `B` therefore preserves the central
`Rep(C3)`: a tensor autoequivalence transports a half-braiding to a
half-braiding on the transported invertible, and that lift is unique.
All coherence is inherited from the already existing categorical
`C2` action. On the two nontrivial invertibles this action is inversion,
as is already forced by `F(Y)=a+a^{-1}`.

## Combining the two Tannakian stages

Equivariantizing the preserved central subcategory gives a full central
Tannakian subcategory

\[
\operatorname{Rep}(C_3)^{C_2}\ \subset\
\mathcal Z(\mathcal B^{C_2})=\mathcal Z(\mathcal C_-),
\]

whose forgetful image in `C_-` is full. Here the displayed inclusion is
the canonical central-lift construction for equivariant objects of a
`C2`-stable central subcategory; it does not assert equality between the
whole equivariantized center and the center of the equivariantization.
The subcategory is Tannakian: forgetting equivariance and then taking
the usual symmetric fiber functor on `Rep(C3)` is a symmetric fiber
functor. Its associated finite group is an extension of `C2` by `C3`
with nontrivial conjugation on `C3`, hence is `S3`. Equivalently, its
underlying simples in `C_-` are `1,g,Y`, with the usual `Rep(S3)` fusion
rules. We have therefore obtained a full central Tannakian
`Rep(S3)` with fully faithful forgetful image.

De-equivariantization by it gives a dimension-four category `P_-` and
a genuine `S3` action, with `C_-=P_-^{S3}`. Equivariantization in stages
identifies `B=P_-^{C3}`. The latter category has exactly three
invertibles and one object of dimension three. The unit orbit in `P_-`
provides the three invertibles of `B`. The remaining object of dimension
three must arise from a size-three orbit of invertible objects: a fixed
simple would give three distinct simple lifts because the projective
Schur multiplier of `C3` is zero. Thus `P_-` is pointed with four
invertibles. The `C3` action cyclically permutes its three nontrivial
invertibles, so its invertible group is `V4`, not `C4`. Consequently
`P_-≅Vec_{V4}^ω` for some unitary associator `ω`. Its particular cocycle
representative is unnecessary: de-equivariantization has already
constructed the pointed category and the coherent `S3` action.

The resulting categories are unitary. One route is to use unitary
central Tannakian condensation throughout. Alternatively, no choice of
unitary descent data needs to be tracked: an equivariantization of a
pointed category is Morita equivalent to its crossed product, which is
pointed (ENO, Proposition 2.2). It is consequently group-theoretical.
Galindo–Hong–Rowell, *Generalized and quasi-localizations of braid group
representations*, Theorem 5.20, establishes complete unitarity of
group-theoretical categories. This applies to both constructed
72-dimensional categories directly.

## Fusion rules of the pullbacks

Let `A=C9` or `C3×C3`, and let `K=ker(q)` (order three). First form
`E_A=P_-^A` by pulling back the `C3` action along `q`. Its invertibles
are the nine characters `Â` of `A`. The three other simples `X_j`
(`j∈C3=K̂`) have dimension three. Write
`p:Â→K̂` for character restriction. Then

\[
\begin{gathered}
gh=g+h,\qquad gX_j=X_{j+p(g)},\\
X_jX_k=\sum_{p(g)=j+k}g+2X_{j+k}.
\end{gathered}
\]

These identities follow without additional coherence choices. The
kernel `K` acts trivially through the pulled-back action; the full
subcategory with trivial `K` character is the inflated `B`. Every
`X_j` is an invertible character twist of `X_0`. Therefore the displayed
products follow by twisting the already established formula for `X_0²`
in `B`. In the cyclic presentation use `Â=Z/9` and `p(g)=g mod3`; in the
split presentation use `Â=(Z/3)²` and `p(g)=g_2`.

The remaining involution acts by `g↦−g` and `X_j↦X_{−j}`. The only fixed
simples are `1` and `X_0`. Thus its equivariantization has two objects
of dimension one, four of dimension two, two of dimension three, and
one of dimension six.

The fixed-channel traces are inherited exactly from the original seed
`C_-`, which is the same involution equivariantization on the inflated
`B` subcategory. In the standard choices of the two equivariant lifts:

\[
\operatorname{tr}(s\mid\operatorname{Hom}(1,X_0^2))=-1,
\qquad
\operatorname{tr}(s\mid\operatorname{Hom}(X_0,X_0^2))=0.
\]

Indeed `V²` contains `g` and not `1`, while it contains one copy each
of `V,W`. All unit-channel traces are `1`. Every fusion multiplicity
is now obtained by projecting to the `±1` eigenspace: for fixed output
and two fixed inputs it is `(dimension + sign_product × trace)/2`;
when either input lies in a size-two orbit the corresponding trace is
zero; for an orbit output it is the underlying multiplicity of one
chosen orbit representative. This is exactly what the replay computes.

As independent positive controls, replace the seed by `Rep(S4)`. Its
analogous fixed-channel trace is `+1`, and the same construction gives
the two explicit representation-category models `R9_2_812` and
`R9_2_813` proved independently in `MODELS.md`.

## Exact certificates

Run from any directory:

```
python /workspace/scratch/90f37cc83103/rank9_m2_research/phase2/group_models/pullback_equivariant_models.py
```

The script builds every integer structure constant, verifies
associativity, and verifies all 729 tensor entries under a unit-preserving
based isomorphism to each source tensor. Output records, full tensors,
parameters, and hashes are in `pullback_models.json`. The duplicate-free
new-pair manifest is `pullback_new_models.json`; it contains only
`R9_2_1396` and `R9_2_1397`. Both the categorical proof and the exact
tensor formulas have received independent internal review.

| Source ring | `A` | Fixed-channel trace | Source-to-model basis map |
|---|---|---:|---|
| `R9_2_812` | `C9` | `+1` | `[0,1,6,7,2,5,3,8,4]` |
| `R9_2_813` | `C3×C3` | `+1` | `[0,1,6,7,2,4,5,8,3]` |
| `R9_2_1396` | `C9` | `−1` | `[0,6,7,2,5,3,8,1,4]` |
| `R9_2_1397` | `C3×C3` | `−1` | `[0,6,7,2,4,5,8,1,3]` |

## Primary references

* Z. Liu, S. Palcoux, Y. Ren, arXiv:2010.10264v5, Sections 3.5 and 4.4:
  https://arxiv.org/html/2010.10264v5 .
* P. Etingof, D. Nikshych, V. Ostrik, *Weakly group-theoretical and
  solvable fusion categories*, arXiv:0809.3031, Theorem 1.6,
  Proposition 4.4(3), and Section 2.6:
  https://arxiv.org/abs/0809.3031 .

* C. Galindo, S.-M. Hong, E. C. Rowell, *Generalized and
  quasi-localizations of braid group representations*, Theorem 5.20:
  https://people.tamu.edu/~rowell/GHRarx1.pdf .

The uniqueness-of-central-lifts argument and the resulting two pullback
models are deductions given here. They are not attributed as explicit
claims of the cited papers.
