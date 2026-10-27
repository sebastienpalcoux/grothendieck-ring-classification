---
title: "Ten unresolved fusion rings: theoretical continuation"
subtitle: "Three general exclusions; seven cases remain unresolved"
date: "27 October 2026"
geometry: margin=25mm
fontsize: 11pt
colorlinks: true
linkcolor: blue
urlcolor: blue
---

## Outcome and scope

This investigation excludes **R9\_2\_1607, R9\_2\_1975, and R9\_2\_1976 from
fusion categorification over the complex numbers**. It supplies **no new model
of a census ring**. The other **seven rings remain unresolved**. Each was considered
individually, with shared arguments used where their categorical structure
permits them.

The work uses the classification repository at commit
`6a426acf6465dd674351be92dcca41b72f371521`. The exact ten source tensors
are in `data/current_remaining_cases.py`. No public repository, website,
classification ledger, or manuscript was modified. The attached evidence
records new proofs, independent checks, short exact verifiers, and the
precise limits of unsuccessful approaches.

| Ring | Status after this investigation | Principal result of this pass |
|:--|:--|:--|
| R6\_4\_155 | Unresolved | A proposed Ising construction cannot reach the rank-nine targets: a central semion survives. |
| R6\_8\_1660 | Unresolved | A categorification cannot admit a real form; two relevant center-representation branches remain. |
| R8\_3\_928 | Unresolved | A short integral-center argument obstructs group extensions and equivariantizations throughout its Morita class. |
| R8\_3\_941 | Unresolved | The corresponding integral-center obstruction is fermionic; ordinary rank-four condensation is unavailable. |
| R8\_3\_1154 | Unresolved | Cancelling the pointed associator with Semion reduces existence to one explicit rank-ten Morita ring. |
| R8\_3\_1768 | Unresolved | The missing separable algebra is constructed, but its actual Morita dual has the wrong invertible objects. |
| R9\_2\_137 | Unresolved | Reflection duality is excluded; zero shift forces all four large second indicators to be $+1$. |
| R9\_2\_1607 | **Excluded over $\mathbb C$** | The symmetric Galois-unit pairing forces a second-indicator sum of four, but at most two is possible. |
| R9\_2\_1975 | **Excluded over $\mathbb C$** | Duality and projective parity contradict the forced Galois-unit central restriction. |
| R9\_2\_1976 | **Excluded over $\mathbb C$** | The same pairing forces a second-indicator sum of four, but its source sum is zero. |

Passing necessary conditions is not counted as a construction. Excluding a
construction route is not counted as excluding its target ring. In
particular, neither of the new rank-eight reductions is a model of its
census target.

## 1. A general-complex exclusion of R9\_2\_1975

### The remaining categorical alternatives

The previous exhaustive Tambara--Yamagami/Morita reduction associates to
any hypothetical categorification a rank-twelve category. After the
previous extreme-branch exclusion, its invertibles form $G=D_8$, with
central subgroup $H=\langle z\rangle\cong C_2$, and its other simples are
$X_q$, indexed by $Q=G/H\cong V_4$. Its rules are

\[
 gX_q=X_qg=X_{q+gH},\qquad
 X_pX_q=\sum_{gH=p+q+\alpha}g+2\sum_{t\in Q}X_t,
 \qquad X_q^*=X_{q+\alpha}.
\]

Here $\alpha$ is either a reflection coset or the rotation coset. Write

\[
 d=4+3\sqrt2,\qquad d^2=2+8d,\qquad
 D=8+4d^2=144+96\sqrt2.
\]

The established sphericalization and Galois reduction allows us to use a
pseudo-unitary representative for the central-dimension argument below.
This is an existence reduction; it imposes no unitarity assumption on an
arbitrary original category. The pointed associator is the complete
TY-origin class, not an unspecified cocycle with selected cyclic values.

### Duality removes reflection shifts

The pointed bimodule stabilizer is
$L=G\times_QG\cong D_8\times C_2$. Use generators $P,S,Z,E$ such that
$Z=[P,S]=(PS)^2$, with $E$ the second central involution. Every allowed
stabilizer cochain has the form $\beta' =\beta\gamma$, where $\beta$ is
the explicit cochain in the evidence and $\gamma$ is an arbitrary
$\mathbb C^*$-valued ordinary two-cocycle.

Duality with shift $qH$ requires a particular two-cocycle $c_q$ to be a
coboundary. It includes both the opposite-bimodule operation and the
normalizer correction. For commuting arguments put
$C_c(A,B)=c(A,B)/c(B,A)$. The new invariant is

\[
 C_{c_q}(P,E)C_{c_q}(S,E)=(-1)^{x+y+n},\qquad q=(x,y,n).
\]

The right side is $-1$ exactly on the reflection cosets. The invariant
does not change under any choice of $\gamma$: commutation with a central
element is a character, hence kills $Z=[P,S]$, and the remaining factor
is $C_\gamma(PS,(PS)^2)=1$. A coboundary has commutator one, so all
reflection shifts are impossible.

The rotation shift genuinely passes this test alone. Its trivializing
one-cochain needs eighth roots of unity; a search limited to fourth roots
would give an incorrect exclusion. The proof below addresses the
surviving rotation shift without imposing any finite root bound.

### Rotation forces even central multiplicity

For either lift of the rotation coset, the explicit base cochain satisfies

\[
 C_{c_q}(P,E)=1,\qquad C_\beta(P,Z)=-1.
\]

Replacing $\beta$ by $\beta\gamma$ changes the first expression by
$C_\gamma(P,Z)$. Duality therefore forces $C_\gamma(P,Z)=1$, and hence
$C_{\beta'}(P,Z)=-1$ for every permitted cochain.

Crucially, the pointed associator is identically one on the even subgroup
$A=\langle p,z\rangle\cong V_4$. The relative-center argument can be
performed entirely within this strict pointed subcategory, avoiding any
assumption about a global diagonal $D_8$ normalization. For a central
object $W$, the multiplicity space
$V=\operatorname{Hom}(X_0,F(W))$ carries two invertible operators satisfying

\[
 U_pU_z=-U_zU_p.
\]

Taking determinants shows that $\dim V$ is even. Thus every central
restriction has even multiplicity at $X_0$.

### The required Galois-unit object has multiplicity one

Let $\sigma(\sqrt2)=-\sqrt2$. The complexified rank-twelve ring has eight
one-dimensional irreducible representations and one of degree two. Its
formal codegrees are

\[
 D,\quad \sigma(D),\quad 16\ \text{(six times)},\quad 4.
\]

For nontrivial $\psi\in\widehat Q$, the scalar representations are
$g\mapsto\psi(gH)$ and $X_q\mapsto t\psi(q)$, with
$t^2=2\psi(\alpha)$. The degree-two representation is the usual $D_8$
representation, with all $X_q$ acting by zero. These exhaust the algebra
because $8\cdot1^2+2^2=12$.

The central element $v=1+\sum_qX_q$ acts on every irreducible $E$ by
$f_E/\sigma(f_E)$. The distinguished central simple
$B=A_{\sigma(\mathrm{FP})}$ must have the same action. Indeed, writing
$\lambda_E=\chi_E/\dim E$ on central elements, the distinguished-object
theorem and symmetry of the unnormalized modular $S$ matrix give

\[
 \frac{D}{f_E}\lambda_E(F(B))
 =S_{A_E,B}=S_{B,A_E}
 =\frac{D}{\sigma(D)}\sigma\!\left(\frac D{f_E}\right)
 =\frac D{\sigma(f_E)}.
\]

Central elements of a semisimple algebra are determined by these scalars.
Consequently

\[
 \boxed{F(B)=1+X_0+X_1+X_2+X_3.}
\]

Its multiplicity at $X_0$ is one, contradicting the even-multiplicity
condition. Rotation is impossible as well. Together with the previous
exhaustive reductions, this proves the general-complex exclusion.

The full cochain formulas, source bindings, scope dependencies, and three
separate reviews are in `r9_noncommutative/GALOIS_PARITY_EXCLUSION.md`,
`r6_155/R1975_INDEPENDENT_AUDIT.md`, and
`r6_1660/R1975_GALOIS_AUDIT.md`. The reflection part also removes one
Morita branch of each of the three commutative rank-nine cases; their
zero-shift branches avoid the parity contradiction. A different use of
the same central object settles two of those zero-shift branches.

## 2. Two more exclusions from the symmetric Galois-unit pairing

For the zero-shift rank-twelve category, the same complete character
calculation gives $F(B)=1+\sum_q X_q$, now with every $X_q$ selfdual.
There is additional categorical information about $B$ that a feasible
central restriction vector alone does not capture.

The canonical algebra $I(1)$ is connected étale, has trivial twist, and
has a nondegenerate Frobenius pairing. A commutative Frobenius algebra
with trivial twist in a ribbon category is symmetric in the pivotal
sense. The distinguished summand $B$ occurs once in $I(1)$, and its
dimension $D/\sigma(D)$ is unique among the summands. Because the
Frobenius pairing makes $I(1)$ selfdual, $B$ is selfdual and inherits a
nondegenerate symmetric pairing.

The forgetful functor is pivotal and strong monoidal. It transports that
pairing to $F(B)$. Each of the four distinct selfdual $X_q$ occurs once,
so restricting the pairing to it is again nondegenerate and symmetric.
Consequently

\[
 \nu_2(X_q)=+1\quad\text{for every }q.
\]

This reasoning transports a particular pairing. It does **not** assert
that a tensor functor preserves numerical Frobenius--Schur indicators.

The dimension-weighted total second indicator is Morita invariant in
the canonical positive spherical structures, because

\[
 \sum_V\dim(V)\nu_2(V)
 =\frac1D\sum_{Z\in\operatorname{Irr}Z(\mathcal C)}
       \dim(Z)^2\theta_Z^2.
\]

If the TY sign is $\varepsilon$, the integral contribution on the
rank-nine side is $4+2\varepsilon$. The pointed contribution on the
rank-twelve side is also $4+2\varepsilon$: the even Klein four contributes
four, the two odd reflections contribute $2\varepsilon$, and the
order-four rotations contribute zero. Cancelling these equal terms gives

\[
 \sum_{\text{four large source simples }V}\nu_2(V)=4.
\]

In R9\_2\_1607 only two large simples are selfdual, so this sum is at
most two. In R9\_2\_1976 none is selfdual, so it is zero. Both contradict
the required value four. The inherited general-complex Galois gates
therefore yield general-complex exclusions of both rings.

In R9\_2\_137 all four large source simples are selfdual. The conclusion
forces their four indicators to be $+1$ and gives no contradiction.
The earlier proposed quadratic-refinement shortcut remains unproved and
is not used. The accepted proof is
`r9_commutative/GALOIS_FS2_EXCLUSION.md`, with a separate rank-six audit.

## 3. R8\_3\_1768: an algebra exists, but the model does not follow

This case received a separate construction attempt rather than another
necessary-condition search. The actual Radchenko--Wheeler precursor is
obtained from the finite quantum dilogarithm associated with

\[
 \gamma=\begin{pmatrix}145&12\\12&1\end{pmatrix},\quad
 \tau=6+\sqrt{37},\quad G=C_{12}\times C_{12}.
\]

In the parent $\mathrm{GH}(C_{12},1)$ category, a direct algebraic
calculation reduces associativity of $1+\rho_0$ to

\[
 E(l,l)=1\qquad (l=1,\ldots,11).
\]

These identities are now proved. Conjugating $\gamma$ by
$\left(\begin{smallmatrix}1&1\\0&1\end{smallmatrix}\right)$ gives the
Hirzebruch--Jung cycle $(14,2,\ldots,2)$ of length twelve. The associated
double-sine product has modulus one because the norm-minus-one unit
$\tau$ preserves both the lattice $\mathbb Z[\sqrt{37}]$ and every
relevant coset. A signed Barnes-cone proof establishes this directly;
it does not incorrectly treat that lattice as an ideal of the maximal
order. The Gaussian phase is exactly zero for all eleven cosets, as
verified with rational arithmetic in $\mathbb Q(\sqrt{37})$. Thus the
values are $+1$, not merely real numbers or numbers of modulus one.

The resulting multiplication is separable without unitarity. Put
$c=6-\sqrt{37}$ and normalize its non-unit coefficient by
$b^2=(c-1)/\sqrt c$. Its invariant pairing has inverse copairing
$1+cr$; the associated Frobenius comultiplication satisfies
$m\Delta=(1+c)\operatorname{id}$. Since $1+c\ne0$, this explicitly
splits multiplication. The audited tensor functor to the twisted
$\mathrm{GH}(C_6,2)$ precursor transports it to a connected separable
algebra $1+\sigma$.

However, completing the categorical check reveals a further obstruction.
The two trivalent multiplication lines are exchanged by conjugation by
the pointed involution $g^3$. They are not isomorphic as normalized
algebras. The two-channel associativity equations reduce, on a
nondegenerate conic, to $abQ_{01}=0$. If $Q_{01}=0$, the conic would
give infinitely many connected separable algebra-isomorphism classes
with the same finite module rank, contradicting module-category rigidity.
Thus only the two pure lines occur, and neither is fixed by $g^3$.

An invertible bimodule must underlie one of the six simple right modules
$g^jA$: the other right modules have underlying FP dimension $6\tau$,
instead of $1+\tau$. Such a bimodule requires an algebra isomorphism
$A\cong g^jAg^{-j}$. Only $j=0,3$ can even preserve the underlying
object. The $j=3$ possibility has just been ruled out; $j=0$ gives only
the unit because the algebra has no nonidentity automorphism.

Therefore the constructed Morita dual has **only one invertible simple**.
R8\_3\_1768 has **two**. This particular construction does not model the
census ring. It is a route obstruction, not a general exclusion of
R8\_3\_1768. The same obstruction has been checked for all six translates
$1+g^j\sigma$ in this precursor. Other precursor associators and other
algebra objects are not eliminated.

The evidence bundle contains the full R1768 construction report, the
separate phase and lattice proofs, and the independent algebra audit.

## 4. Individual progress on the other cases

**R6\_4\_155.** A conditional product with Ising, followed by condensation
of the diagonal fermion, has the same global dimension as the rank-nine
targets. It nevertheless retains the central semion factor, which those
targets cannot have. This disposes of the proposed model route. A short
exact zero-spectrum check of the entire forced rank-26 center factor
finds no obstruction. The required associators, or a realization of that
center together with its algebra, remain missing.

**R6\_8\_1660.** The unique pivotal structure has third indicators
$2+\zeta_3$ or $2+\zeta_3^2$ on both simples of the relevant common FP
dimension. Every Galois conjugate remains nonreal. A complex-linear
equivalence with the conjugate category cannot match those two objects,
so a categorification admits no real form. In its positive representative,
the weighted total third indicator also obstructs Morita equivalence with
the conjugate. This is a restriction on models, not a complex
categorification obstruction. Two pertinent center-representation
branches still pass.

**R8\_3\_928.** A short lemma shows that its integral center is exactly
Semion. The hypotheses are: full adjoint subcategory, integral objects
supported on $1,g$, free action of $g$ on simples, and a central lift of
$g$. Pointed-isotypic projections are then central, and a central object
forgetting to copies of the unit is controlled by the trivial universal
grading. Consequently there is no nontrivial Tannakian subcategory of the
center. No Morita representative can be a nontrivial group extension or
equivariantization. The four remaining center phase patterns do not
construct a category.

**R8\_3\_941.** The same lemma gives integral center $\mathrm{sVec}$.
It yields the analogous Morita obstruction. The algebra $1+g$ exists,
but fermionic condensation cannot be treated as an ordinary rank-four
fusion-category quotient. The possible connection with R6\_8\_1660
still needs its nonpointed algebra; fourteen center allocations remain
necessary data only.

**R8\_3\_1154.** Let $a=6+3\sqrt5$. Adjoining Semion cancels the
nontrivial pointed $C_2$ associator, so the diagonal algebra $1+(g,s)$
really exists. Its Morita dual has dimensions
$1^{\times4},a^{\times4},(2a+2)^{\times2}$. Formal codegrees reduce
ten small candidate based rings to two. The known center's duality and
twist data remove the all-selfdual candidate: it would require five
selfdual twist-one simples of a particular dimension where only two
exist. The single surviving ring has generators $u,v,x,y$ satisfying

\[
 \begin{gathered}
 u^2=v^2=1,\quad uy=y,\quad x^*=ux,\quad y^*=y,\\
 x^2=u+(1+u+v+uv)x+2(1+v)y,\\
 xy=2(1+u)(1+v)x+(4+5v)y,\\
 y^2=1+u+(4+5v)(1+u)x+(8+11v)y.
 \end{gathered}
\]

Here $u,v$ are central. The remaining second-indicator signs and their
palindromic parity constraints are consistent, so the reduction stops
short of an exclusion or a construction. The full derivation is
`r8_quartic/R1154_NOTES.md`.

**R9\_2\_137.** Reflection duality is now impossible in the necessary
$D_8$ Morita category. Zero shift remains, for both previously surviving
TY signs. In the positive-sign branch the third-indicator constraint
requires ninth roots in the twist spectrum. A new divisibility and Galois
orbit argument restricts the possible central dimensions in this sector
to $Bd$, with $B\in\{1,2,3,4,6,8,12\}$, but leaves consistent possibilities.

**R9\_2\_1607.** The zero-shift branch passes pointed-module cochain
checks, but the symmetric Galois-unit pairing excludes it as shown in
Section 2. Its two nonselfdual large objects make the required sum four
impossible. The reflection branch is excluded independently by duality.

**R9\_2\_1976.** Its four large source objects are nonselfdual, forcing
the source large-object second-indicator sum to be zero. The earlier
quadratic-refinement shortcut is not justified: pointed-module cochains
admit zero-sum patterns. However, the new symmetric Galois-unit pairing
requires sum four in any actual category. This categorical contradiction
settles the zero-shift branch, and hence the entire ring.

## 5. Verification and reproducibility

The calculations used here are short exact checks, not a large pentagon
search. They include finite group/cochain identities, source-tensor
bindings, complete small character tables, rational matrix identities,
and the eleven finite Gaussian-phase calculations. The phase audit also
checks all 132 intermediate cocycle arguments and all 143 integral
cocycle indices. The bounded rank-26 zero-spectrum scan takes about half
a second. The all-complex cochain-independence and categorical existence
or nonexistence claims rest on the written proofs, not on finite searches
over arbitrarily restricted scalars.

The evidence bundle preserves the source snapshot, inherited dependencies,
new proof files, exact scripts and receipts. Historical discovery files
are marked as such. Read the final reports for accepted conclusions;
experimental cochains or feasible rings alone carry no classification
claim. The inherited spherical/Galois and exhaustive Morita reductions
remain explicit dependencies rather than being silently assumed away.

The inherited signed Galois gates for all four rank-nine inputs were
freshly replayed against the current source tensors. Their complete
branch checks passed in about nine seconds in total. The new symmetric
pairing criterion was also checked against the rank-six and other
rank-eight survivors; it yields no additional contradiction there.

These results have been cross-checked within this investigation. They
have not undergone external mathematical peer review.

## Primary references

1. L. Vainerman and J.-M. Vallin, *On $\mathbb Z/2\mathbb Z$-extensions
   of pointed fusion categories*, [arXiv:1210.1732](https://arxiv.org/abs/1210.1732),
   §§2.2.1, 2.2.2, 3.1.1.
2. V. Ostrik, *Pivotal fusion categories of rank 3*,
   [arXiv:1309.4822](https://arxiv.org/abs/1309.4822), Theorem 2.13.
3. T. Deshpande, *On centers of bimodule categories and induction-restriction
   functors*, [arXiv:1611.04486](https://arxiv.org/abs/1611.04486), §2.7 and §4.3.
4. C. Goff, G. Mason and S.-H. Ng, *On the gauge equivalence of twisted quantum
   doubles of elementary abelian and extra-special 2-groups*,
   [arXiv:math/0603191](https://arxiv.org/abs/math/0603191), Lemmas 4.4–4.5.
5. D. Radchenko and C. Wheeler, *Real quadratic fields and finite quantum
   dilogarithms I*, [arXiv:2609.21892v2](https://arxiv.org/abs/2609.21892v2).
6. S. Yamamoto, *On Shintani's ray class invariant for totally real number
   fields*, [arXiv:0805.4282](https://arxiv.org/abs/0805.4282), especially §5.2.
7. J. Fröhlich, J. Fuchs, I. Runkel and C. Schweigert,
   *Correspondences of ribbon categories*,
   [arXiv:math/0309465](https://arxiv.org/abs/math/0309465), Proposition 2.25(ii).
8. P. Etingof, D. Nikshych and V. Ostrik, *On fusion categories*,
   [arXiv:math/0203060](https://arxiv.org/abs/math/0203060), Corollary 2.35.

The individual evidence reports give the additional case-specific primary
sources and the exact paths of inherited project proofs.
