# Two rank-nine exclusions from a symmetric Galois-unit pairing

## Result and scope

**R9_2_1607 and R9_2_1976 have no fusion categorification over the
complex numbers.** R9_2_137 remains unresolved; this argument forces all
four of its large simple objects to have second Frobenius–Schur indicator
$+1$ in the positive representative.

The argument combines the new reflection-duality obstruction in
`../r9_noncommutative/REPORT.md`, the Galois-unit calculation in
`../r9_noncommutative/GALOIS_PARITY_EXCLUSION.md`, and the symmetric
pairing observation below. It uses the previously audited categorical
TY/Morita reductions and the general-complex-to-pseudo-unitary existence
gate. There is no unitarity assumption and no search over associators.

## 1. Exact source bindings

Inputs are the tensors in `data/current_remaining_cases.py` at the frozen
source commit `6a426acf6465dd674351be92dcca41b72f371521`.

| Ring | Tensor SHA-256 | TY object | Large objects | Selfdual large objects |
|---|---|---:|---|---|
| R9_2_137 | `c509d23c9a638aaea8a624a6c5186ad3f0c1b6e6f432576b45300f6e630c56e6` | 8 | 3,4,5,6 | all four |
| R9_2_1607 | `16b023a44f69bb516b8a8c9933a2b360b44219a07de2f1599e8f216eb74dbfa2` | 3 | 1,2,7,8 | 7,8; 1 and 2 are dual |
| R9_2_1976 | `2280410fa5b33121f9b5d9cfdea15f90bf56933f9b26c0ccdbe047c153d08d30` | 5 | 1,2,3,4 | none; 1↔2 and 3↔4 |

Every source has four invertibles, one TY object $Y$ of dimension 2,
and four large objects of dimension

\[
d=4+3\sqrt2,\qquad d^2=2+8d,\qquad
D=144+96\sqrt2=8+4d^2.
\]

The short verifier `verify_source_checks.py` independently checks these
dimensions, dualities, and hashes. Its receipt is `source_checks.json`.

The prior reductions establish a connected subgroup algebra and a
rank-twelve Morita dual with invertible group $G=D_8$, central
stabilizer $H=C_2$, quotient $Q=G/H=V_4$, and four other simples
$X_q$. The earlier possibilities for these three sources had zero or
reflection duality shift. The new all-complex commuting-pair obstruction
excludes the reflection shifts. Thus a remaining categorification must
have the uniform zero-shift rules

\[
gX_q=X_qg=X_{q+gH},\qquad
X_pX_q=\sum_{gH=p+q}g+2\sum_{t\in Q}X_t,
\qquad X_q^*=X_q.
\]

The existing spherical/Galois existence gate allows us to work with a
pseudo-unitary representative of this Morita pair. This does not assert
that the original hypothetical category was unitary. Pseudo-unitarity
is preserved under categorical Morita equivalence, so both sides have
their canonical positive spherical structures.

## 2. A multiplicity-one Galois object is symmetrically selfdual

Let $\mathcal D$ be the hypothetical positive rank-twelve category,
$F:Z(\mathcal D)\to\mathcal D$ the forgetful functor, and $I$ its
right adjoint. Its canonical algebra $L=I(\mathbf1)$ is connected
étale and has trivial twist. It has a nondegenerate Frobenius pairing.
A commutative Frobenius algebra with trivial twist in a ribbon category
is symmetric in the **pivotal** sense: see Fröhlich–Fuchs–Runkel–Schweigert,
*Correspondences of ribbon categories*, Proposition 2.25(ii),
https://arxiv.org/pdf/math/0309465 or the author copy
https://www.math.uni-hamburg.de/home/runkel/PDF/corr.pdf.

In explicit duality notation, its pairing gives an isomorphism
$\phi_L:L\to L^*$ satisfying

\[
\phi_L=\phi_L^*j_L,
\]

where $j$ is the pivotal structure. This is stronger than merely
braided commutativity of the multiplication; it is the property used here.

Let $B=A_{\sigma\mathrm{FP}}$ be the distinguished summand of $L$
for the conjugate dimension character, where
$\sigma(\sqrt2)=-\sqrt2$. For the zero-shift uniform ring the complete
list of irreducibles consists of eight one-dimensional representations
and one two-dimensional representation. Their formal codegrees are

\[
D,\quad D'=\sigma(D),\quad 16\text{ (six times)},\quad4.
\]

The distinguished central objects therefore have dimensions

\[
1,\quad D/D',\quad D/16\text{ (six times)},\quad D/4.
\]

Their multiplicities in $L$ are respectively 1 for the scalar
representations and 2 for the two-dimensional representation.
In particular $B$ occurs once and its dimension $D/D'$ is unique
among these constituents. Since $L\cong L^*$, duality must preserve
this unique dimension and consequently $B^*\cong B$.

The pairing of $L$ cannot pair this summand with any other simple
summand. Its restriction to $B$ is therefore nondegenerate and still
pivotally symmetric. Thus $B$ is symmetrically selfdual.

The normalized central-character calculation, with the factor
$\dim(E)$ retained for the two-dimensional representation, gives

\[
F(B)=\mathbf1+\sum_{q\in Q}X_q.
\tag{1}
\]

For a full proof see the sibling `GALOIS_PARITY_EXCLUSION.md`, §4.
The same proof applies with zero shift: the rational codegrees remain
16 and 4. More explicitly, $1+\sum X_q$ acts on every irreducible
$E$ by $f_E/\sigma(f_E)$, and the modular $S$-symmetry formula
gives exactly the same scalar for $F(B)$. Equality follows from
semisimplicity of the complexified based algebra.

The functor $F$ is pivotal and strong monoidal. It therefore carries
the nondegenerate symmetric pairing of $B$ to one on $F(B)$.
Every $X_q$ is selfdual and appears once in (1). Restricting the
pairing to each of these pairwise nonisomorphic simple summands is
again nondegenerate and symmetric. Hence

\[
\boxed{\nu_2^{\mathcal D}(X_q)=+1\quad\text{for every }q\in Q.}
\tag{2}
\]

We are **not** claiming that numerical Frobenius–Schur indicators
are preserved by arbitrary tensor functors. The transported object is
a particular symmetric pairing, and multiplicity one is essential.

## 3. Exact Morita-invariant second-indicator comparison

For a pseudo-unitary fusion category define

\[
T_2(\mathcal C)=\sum_{V\in\mathrm{Irr}(\mathcal C)}
\dim(V)\nu_2(V).
\]

The center-induction indicator formula gives

\[
T_2(\mathcal C)=\frac1{\dim\mathcal C}
\sum_{Z\in\mathrm{Irr}(Z(\mathcal C))}\theta_Z^2\dim(Z)^2.
\tag{3}
\]

Indeed, multiply
$\nu_2(V)=\operatorname{Tr}(\theta_{I(V)}^2)/\dim\mathcal C$
by $\dim V$, sum over $V$, and use Frobenius reciprocity:
$\sum_V\dim(V)[I(V):Z]=\dim F(Z)=\dim Z$.
Formula (3) is invariant under Morita equivalence because the centers
are braided equivalent and their canonical positive ribbon structures
agree. The indicator formula is Ng–Schauenburg,
*Frobenius–Schur indicators and exponents of spherical categories*,
https://arxiv.org/pdf/math/0601012.

Write the TY sign in the source as $\varepsilon\in\{+1,-1\}$,
so $\nu_2(Y)=\varepsilon$. Its four invertibles have trivial
associator and second indicator 1. Thus its integral contribution is

\[
T_{2,\mathrm{integral}}(\mathcal C)=4+2\varepsilon.
\]

In the rank-twelve dual, the forced pointed associator is trivial on
the even Klein four subgroup, while the two odd reflections have
second indicator $\varepsilon$. The two order-four rotations are
not selfdual and have second indicator zero. Thus its pointed
contribution is also exactly

\[
T_{2,\mathrm{pointed}}(\mathcal D)=4+2\varepsilon.
\]

These signs are part of the earlier TY-origin associator calculation;
Galois conjugation does not change them because they are $+1,-1$.
Using (2) and cancelling these equal integral contributions in (3) gives

\[
\boxed{\sum_{\text{four large }V\text{ in }\mathcal C}\nu_2(V)=4.}
\tag{4}
\]

Now a nonselfdual simple has second indicator zero, whereas a
selfdual simple has second indicator $+1$ or $-1$:

* **R9_2_1607:** only two large simples are selfdual. Their total is
  at most 2, contradicting (4).
* **R9_2_1976:** none of the four large simples is selfdual. Their
  total is zero, contradicting (4).
* **R9_2_137:** all four are selfdual. Equation (4) forces all four
  indicators to be $+1$, but supplies no contradiction.

This completes the two exclusions over $\mathbb C$, using the
stated general-complex existence gate. No numerical indicator
optimization, bounded root search, or unitarity classification enters
the new argument.

## 4. Dependency and verification record

The existing categorical gates are in
`evidence/rank9_m2_20261024/proofs/phase5/quadratic_comm/ty_module_subtask/`
(`THEOREM.md`, `DUAL_COMPLETION.md`, `FORCED_D8_ASSOCIATOR.md`) and
`evidence/unresolved_retry_20261024/proofs/unresolved11_retry_20261024/rank9/POINTED_BIMODULE.md`.
The independent new reflection proof and all-complex cochain audit are
in `../r9_noncommutative/REPORT.md` and its exact checker.

The source binding verifier is short and exact. The categorical
symmetric-pairing lemma was independently discussed and checked by the
root, rank-six and rank-nine investigators. Its decisive point is
pivotal symmetry and multiplicity one, rather than preservation of
indicators by the forgetful functor.

`verify_galois_fs2.py` checks all products in the eight scalar and one
two-dimensional representations of the zero-shift ring, all formal
codegrees including the degree-two normalization, the Galois restriction
vector, both TY-sign cancellations in the pointed cocycle, and the exact
source indicator bounds. Its receipt is `galois_fs2_receipt.json`.

The prior signed-dimension existence gates were freshly replayed from
the tracked archive by the independent rank-six investigator: R137 has
six signed branches and twelve orbit tables, R1607 ten and fourteen,
and R1976 eight and fifteen. Each finite completeness run returned
UNSAT, and source tensor hashes match the archived certificates. See
`../r6_1660/rank9_signed_gates_replay_receipt.json` and
`../r6_1660/rank9_signed_gate_provenance.json`.

This result is offline research. No public classification files or
website records have been changed.
