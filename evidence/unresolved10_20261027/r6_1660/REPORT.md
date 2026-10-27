# R6_8_1660: theoretical investigation, 27 October 2026

**Classification verdict: unresolved. No complex categorification was excluded or constructed.**

This investigation found a short additional obstruction to model constructions:
every categorification must fail real descent, even when descent is allowed to
permute simple objects. In the positive spherical representative its entire
Morita class also fails real descent. These statements are weaker than
nonexistence over the complex numbers.

The source snapshot is `6a426acf6465dd674351be92dcca41b72f371521`. The
source tensor has SHA-256
`697ec27fe203356199bfcf674587be9c71455dbb681f2e086a076f726b03d267`.
The short verifier `verify.py` binds the source data and verifies the exact
arithmetic below. It runs in well under one second; no pentagon search or
long numerical computation was used.

## 1. Starting point and hypotheses

Write the simples as `1,g,X,gX,σ,T`, with `T=σX`. The ring is determined by

\[
g^2=1,\quad g\sigma=\sigma,\quad \sigma^2=1+g,\qquad
X^2=1+\bigl(3(1+g)+4\sigma\bigr)X.
\]

Its FP dimensions are `1,1,d,d,√2,√2d`, where

\[
d=3+2\sqrt2+2\sqrt3+\sqrt6.
\]

The published spherical/Galois reduction and complete higher-indicator
argument are inputs here, not newly proved classification theorems. In a
positive spherical Galois representative they give

\[
\nu_3(X)=\nu_3(gX)=2+\omega^{\epsilon},\qquad
\nu_3(T)=2,\qquad \epsilon\in\{1,2\},\quad \omega=e^{2\pi i/3}.
\]

The two signs are complex conjugates. Relevant source files are
`manuscripts/rank6/papers/chapters/frontier_spherical_reduction.tex`,
`frontier_1660_phase_masses.tex` in the same directory, and
`evidence/unified_20261016/rank6/higher_indicators/R1660_HIGHER_INDICATOR_PROOF.md`.

The universal grading is trivial: the terms `1,X,gX,T` in `X²` force
all their degrees to be the identity; `gX` and `σX=T` then force the
degrees of `g` and `σ` to be the identity. Hence `Aut⊗(Id_C)=1` and,
when a pivotal structure exists, it is unique up to the usual equivalence.
The earlier spherical reduction establishes existence for every complex
categorification of this ring.

## 2. A real-descent obstruction

**Proposition.** No complex categorification of `R6_8_1660` is tensor
equivalent to its complex-conjugate category. In particular it has no
real form, split or nonsplit, and cannot be presented by entirely real
associativity and rigidity data.

**Proof.** First work in the positive representative. A tensor equivalence
to its conjugate preserves the FP dimension of every object. The complete
FP-dimension class of `X` is `{X,gX}`. It also preserves the unique pivotal
structure, so it preserves third indicators. But the indicator of either
possible image is `2+ω^{-ε}`, whereas the source indicator is `2+ω^ε`.
These numbers are different.

For an arbitrary original complex categorification, transport its unique
pivotal structure along the Galois equivalence used in the published
positive reduction. Pivotal rotations, being defined by finite compositions
of structural maps, and their traces commute with change of scalar field.
Every field automorphism sends a primitive cube root to a primitive cube
root. Thus the original common indicator is still one of `2+ω` and
`2+ω²`, and is still nonreal. The FP-dimension class remains `{X,gX}`
because it is a property of the unchanged fusion ring. The same argument
therefore applies before taking a positive Galois representative.

A real form would give a coherent conjugate-linear tensor equivalence,
or equivalently a linear tensor equivalence to the conjugate category.
The argument already rules out such an equivalence without requiring its
coherence square, and allows arbitrary permutations of simple objects.
This proves the statement also for nonsplit real forms. ∎

This use of Galois transport is specific to the displayed indicator values:
all their Galois conjugates are nonreal. It is **not** an assertion that
arbitrary real algebraic coefficients remain real under every embedding.

## 3. The positive Morita class also cannot have a real form

For a positive spherical fusion category set

\[
W_3(\mathcal C)=\sum_{Z\in\operatorname{Irr}(\mathcal C)}
  \operatorname{FPdim}(Z)\nu_3(Z).
\]

**Proposition.** A pseudo-unitary categorification of this ring is not
Morita equivalent to its conjugate. Consequently no member of its Morita
class admits a real form.

**Proof.** Here `ν3(1)=1` and `ν3(g)=ν3(σ)=0`, so

\[
W_3=1+2d(2+\omega^\epsilon)+2\sqrt2\,d,
\qquad \operatorname{Im}(W_3)=\pm\sqrt3\,d\ne0.
\]

The center indicator formula gives

\[
\tau_3(Z(\mathcal C))=\operatorname{FPdim}(\mathcal C)\,W_3(\mathcal C).
\]

Morita equivalence induces a braided equivalence of centers, and an
equivalence between pseudo-unitary centers preserves their canonical
positive spherical structures. It therefore preserves this number.
Complex conjugation fixes the positive dimensions and conjugates the
indicator and twist traces. An equivalence of `C` and its conjugate at
the level of Morita classes would make `W3` real, a contradiction.

If a Morita partner `D` had a real form, `D ≃ conjugate(D)` would imply
`C ~ D ~ conjugate(D) ~ conjugate(C)`, giving the same contradiction. ∎

**Scope.** This Morita argument is stated for the positive representative.
It is not transported to arbitrary original non-positive forms by an
unstated compatibility of real structures with Galois conjugation.
The preceding direct obstruction to a real form does apply to every
original complex categorification.

The result rules out a Morita construction from a category with a real
form. More concretely, a category of bimodules over a real separable
algebra in a real tensor category has a real form and cannot give the
positive target. For full right-module fusion categories in a braided
category, descent of the underlying algebra alone is insufficient: the
central structure used for the tensor product must also descend.
Thus this is not an exclusion of every conformal-embedding construction.

The established conditional relation to `R8_3_941` is retained: the
required nonpointed module category would give that Morita dual, but its
existence is not forced by the ring. The new obstruction applies to any
such positive Morita partner; it does not construct the algebra.

## 4. A compact center-representation reduction

The published phase-mass theorem gives exact phase support

`{0,8,9,12,14,15,20,24,26,30,32,33,36,39,42,44}` modulo 48,

and exactly two dual simple objects at each phase `9,15,33,39`.
Hence charge conjugation has a one-dimensional negative eigenspace at
each of these four phases.

The exact character tables of `SL(2,Z/16) × SL(2,Z/3)` have 76×7
irreducibles. Of the 42 irreducibles whose entire twist support lies in
the displayed set, only three have central sign −1 and meet those four
phases. In the existing table numbering they are

| Irreducible | Dimension | Twist phases |
|---|---:|---|
| `(16,2)` | 3 | 15,30,39 |
| `(20,2)` | 3 | 9,33,42 |
| `(44,2)` | 6 | 9,12,15,33,36,39 |

If their multiplicities are `a,b,c`, the four spin fibers impose
`a+c=b+c=1`. Thus the part of the negative charge-conjugation
representation meeting the spin fibers is exactly one of

\[
V_{16,2}\oplus V_{20,2},\qquad V_{44,2}.
\]

This follows from the full source-bound character tables, without
selecting the previously rejected rank-37 witness. It is an explicit
two-branch reformulation of necessary center data, not a categorical
model or a claim that all earlier modular tests gain a new exclusion.
The conjugate phase convention gives the conjugate alternatives.

The attempt to extend the known half-integral Verlinde contradiction
does not presently close these branches. In particular, the spin-fiber
alternatives are not forced to use the one-dimensional hidden summand
responsible for the old rank-37 obstruction. Reusing that contradiction
for every profile would be invalid.

## 5. Other attempts and the unresolved gap

The regular Ising-bimodule description, the rank-eighteen relative-center
ring, the three possible Morita-dual rings, and the exceptional WZW
dimension/index obstructions were reread. They were already established
and are not counted as new progress here.

Short exact checks of ordinary cyclic rotation-character compatibility
at all orders dividing 48 found no obstruction. An exploratory odd-order
spin-character factorization check through order 31 also passed; no
categorical existence conclusion or new general Clifford theorem is
inferred from that diagnostic calculation.

The missing step remains either a categorical obstruction valid in every
surviving center branch, or an actual Ising-enriched associator / separable
algebra construction. The two-branch reduction and the real-descent
obstruction narrow what such a construction can be, but neither decides
general complex categorifiability.

The subsequently proposed symmetric-pairing parity criterion was also
checked against this case. Its only simple of second indicator `−1` is
`σ`, while the exact source tensor gives
`F(I(1))=(6,2,12,12,0,16)` in the order `1,g,X,gX,σ,T`.
Thus `σ` occurs in no distinguished central restriction at all, and this
criterion supplies no additional contradiction. For comparison, in
`R6_4_155` the corresponding vector is `(6,8,8,2,0,0)` in source order;
again its two negative-indicator invertibles occupy the absent coordinates.

## Primary references

- S.-H. Ng and P. Schauenburg, *Higher Frobenius–Schur indicators for pivotal
  categories*, https://arxiv.org/abs/math/0503167 : pivotal equivalence
  invariance and the rotation-trace definition.
- S.-H. Ng and P. Schauenburg, *Frobenius–Schur indicators and exponents of
  spherical categories*, https://arxiv.org/abs/math/0601012 , Theorem 4.1:
  the center indicator formula.
- C. Galindo, *On split forms of fusion categories*,
  https://arxiv.org/abs/2608.23743 , Sections 2.1–2.4: the distinction
  between forms and split forms and conjugate-linear descent. The present
  indicator argument rules out even the underlying equivalence, so needs
  no additional descent-obstruction theorem from that paper.

These conclusions inherit the hypotheses of the project's published
indicator and spherical-reduction proofs. They do not represent an
independent human verification or formalization of those inputs.
