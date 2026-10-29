# Further restrictions for R6_8_1660 and R8_3_941

29 October 2026. **Neither ring is resolved by this continuation.** The results
below exclude construction routes; they do not establish general
noncategorifiability or supply an associator.

## 1. A nonreal Morita invariant for R6_8_1660

Work in a hypothetical pseudo-unitary categorification C of R6_8_1660,
with its canonical positive spherical structure. This is the positive
representative supplied by the inherited existence reduction, not an
assertion that an arbitrary original category is positive.

Use simples `(1,g,X,gX,sigma,T)` with T=sigma X, and put

\[
d=3+2\sqrt2+2\sqrt3+\sqrt6,\qquad D=4(1+d^2).
\]

The already established complete-indicator theorem forces, in one of its
two conjugate branches,

\[
\nu_3(1)=1,\quad \nu_3(g)=\nu_3(\sigma)=0,\quad
\nu_3(X)=\nu_3(gX)=2+\omega,\quad \nu_3(T)=2,
\qquad \omega=e^{2\pi i/3}.
\]

The other branch conjugates these values. The positive source dimensions
are `(1,1,d,d,sqrt(2),sqrt(2)d)`. Consequently

\[
W_3(C):=\sum_V d_V\nu_3(V)
=1+(3+2\sqrt2)d\ \mathbin{\pm}\ i\sqrt3d.
\tag{1}
\]

In particular Im(W3) is nonzero.

This is consistent with Z(C) being the Drinfeld center of a spherical
fusion category. Its first multiplicative central charge is one, but no
reality requirement for the third Gauss sum follows here:
3 is not coprime to the already forced exponent 48.

**Theorem.** C is not categorically Morita equivalent to its complex
conjugate or to its tensor-opposite category. No category in its Morita
class has a real form. In particular C admits neither a tensor equivalence
to its tensor opposite nor an antilinear tensor autoequivalence.

**Proof.** For a positive spherical category A, the Ng--Schauenburg center
formula gives

\[
W_n(A)=\frac{1}{\operatorname{FPdim}(A)}
       \sum_{Z\in\operatorname{Irr}Z(A)}d_Z^2\theta_Z^n.
\tag{2}
\]

To derive (2), multiply the formula for nu_n(V) by d_V and sum over V;
the coefficient sum is dim(FZ)=d_Z. A Morita equivalence gives a braided
equivalence of centers. Their canonical positive spherical structures are
preserved, by uniqueness, so their twists and dimensions are preserved.
Thus W_n is a Morita invariant for pseudo-unitary categories.

Under complex conjugation, the positive dimensions are unchanged and the
twists are conjugated. Under tensor opposition the center has reversed
braiding and inverse twist, with the same dimensions. Roots of unity have
inverse equal to complex conjugate, so either operation conjugates (2).
Equation (1) prevents Morita equivalence to either resulting category.

A real form of any category in this Morita class would supply an
equivalence to its complex conjugate. The preceding contradiction rules
it out. Here “real form” means descent of that complex tensor category to
R, not a statement about whether some subset of its numerical data is
real. No unitarity assumption is used. QED.

The notation “tensor opposite” reverses the order of tensor factors; it
does not mean reversing the braiding on the original C, which is not
braided. At the level of its modular center, reversal means replacing the
braiding by its inverse transpose, and the twist by its inverse.

**Corollary.** The Morita class of this positive C contains no braided
fusion category. Indeed a braiding gives a tensor equivalence from that
category to its tensor opposite. Its W3 would therefore equal its complex
conjugate, contradicting (1). This argument avoids a case-by-case
reconstruction of all possible Morita-dual based rings.

**Conditional consequence for R8_3_941.** If a positive categorification
of R941 is actually Morita equivalent to a positive categorification of
R1660, then it has the same nonreal invariant (1) and obeys the same
conclusions. Equality of global FP dimensions alone does not prove that
hypothesis. This is therefore not an unconditional restriction on every
possible R941 category.

**Construction consequence.** Searching for a real-form positive
categorification or a tensor-self-opposite Morita representative of this
positive R1660 category cannot work.
This does not exclude unitary categories: unitary associators need not
admit a simultaneous real gauge, and a category need not be Morita
equivalent to its reversal.

The real-form assertion is deliberately limited to the positive category
and its Morita class. The inherited existence reduction supplies a positive
Galois representative, but an arbitrary field automorphism need not
commute with complex conjugation on the associator field. We do not infer
that every possible original nonpositive categorification lacks real
descent from this calculation alone.

## 2. A uniform consequence for direct modular-source constructions

For either positive target category C, retain the previously proved
center restrictions: its integral center consists of the unit and a
fermion h, and every nonpointed fusion subcategory H of Z(C) forgets
dominantly to C with FPdim(H)>D. For R1660, strictness follows from the
absence of a central simple of dimension sqrt(2); for R941, equality
would transport a braiding to its noncommutative source ring. These are
the inherited categorical hypotheses; they are not consequences of FP
dimension coincidence alone.

**Proposition.** Z(C) has no proper nontrivial nondegenerate fusion
subcategory. Consequently, if B is nondegenerate braided and A is a
connected etale algebra such that B_A is tensor equivalent to C, then
B is braided equivalent to Z(C), A is Lagrangian, and FPdim(B)=D^2.

**Proof.** If H were a proper nontrivial nondegenerate subcategory of
Z(C), its centralizer H' would also be nontrivial nondegenerate. Neither
can be pointed: the entire pointed part is sVec, which has no nontrivial
nondegenerate subcategory. The strict bound gives FPdim(H)>D and
FPdim(H')>D, contradicting the modular centralizer identity
FPdim(H) FPdim(H')=D^2. This proves primeness.

For B and A as stated, DMNO Corollary 3.30 gives

\[
Z(B_A)\simeq B\boxtimes(B_A^0)^{\mathrm{rev}}.
\]

B is nontrivial because B_A has dimension D>1. Primeness forces
B_A^0=Vec, and the formula identifies B with Z(C). The local-module
dimension formula then gives FPdim(A)^2=FPdim(B), the Lagrangian
condition. QED.

Thus a direct full-module construction from a modular quantum-group
source of dimension different from D^2 cannot realize either positive
target. This conclusion does not require listing algebras in that
source. It does not exclude local-module constructions of the center,
nonmodular sources, or noncentral module constructions.

## 3. A coefficient-cone obstruction for the level-(6,10) source

The common dimension of the two target rings is

\[
D=144+96\sqrt2+80\sqrt3+56\sqrt6.
\]

Consider the natural quantum-group source

\[
B=SU(2)_6\boxtimes SU(2)_{10}.
\]

The standard quantum dimensions give

\[
W:=\operatorname{FPdim}(B)
=(16+8\sqrt2)(48+24\sqrt3),\qquad
\frac WD=24-8\sqrt6.
\tag{3}
\]

**Theorem.** Neither target ring can be obtained as the full module fusion
category B_A of a connected etale algebra A in B. Neither can its center
be obtained as the local module category of a connected etale algebra in
B boxtimes B with either braiding reversed. The same statement holds for
Galois forms with the same based source rings and these FP dimensions.

**Proof.** Put r=sqrt(2), s=sqrt(3), c=sqrt(2+r). The eight elements

\[
1,r,s,rs,c,cr,cs,crs
\tag{4}
\]

are linearly independent over Q. Indeed K=Q(r,s) is biquadratic. If c
were in K=L+sqrt(3)L, L=Q(r), the equality c^2 in L would force either
c in L or c in sqrt(3)L. It would follow that 2+r or (2+r)/3 is a square
in L. Their norms to Q are 2 and 2/9, respectively; neither is a rational
square, whereas the norm of a square in L is a rational square.

The rational cone spanned by (4) is closed under multiplication: its
relations are r^2=2, s^2=3 and c^2=2+r, all with nonnegative coefficients.
Every simple dimension of SU(2)_6 lies in this cone, from the list

\[
1,c,1+r,rc,1+r,c,1.
\]

The list for SU(2)_10 is

\[
1,\tfrac{r+rs}{2},1+s,\tfrac{3r+rs}{2},2+s,r+rs,
2+s,\tfrac{3r+rs}{2},1+s,\tfrac{r+rs}{2},1.
\]

Hence every object dimension of B, or of B boxtimes B, has nonnegative
coordinates in (4). But (3) has coefficient -8 on rs and so cannot be
the dimension of any object in either source.

For full modules, the dimension formula requires FPdim(A)=W/D. For
local modules with target the center, it requires

\[
D^2=W^2/\operatorname{FPdim}(A)^2,
\]

again forcing FPdim(A)=W/D by positivity. Both are impossible. Reversing
braidings or taking Galois forms does not change the relevant based FP
dimension lists. QED.

This excludes these particular sources. It is not a classification of
all quantum-group constructions, products, extensions, intermediate
condensations, or algebras in unrelated categories.

## 4. What was checked and what is still missing

The finite checker `verify.py` uses exact rational arithmetic. It checks
the two complete tensor dimension characters, their common global
dimension, the cubic vacuum dimensions, equation (1), the cone's 64
basis products, both SU(2) recursions and global dimensions, all 77
product simple dimensions, and equation (3). It performs no optimizer,
associator search, or long enumeration. It records inherited indicators
as hypotheses rather than pretending to re-prove the complete center
domain from the tensor alone.

The following approaches were examined and give no further valid
exclusion:

* The relative-center's central copy of Z(Ising) does not by itself split
  its underlying fusion category as a tensor product. A central embedding
  into the center is weaker than a braiding on the whole source.
* The fermionic rank-four quotient of R941 cannot be treated as an
  ordinary pivotal fusion category. Its odd fusion channels are genuine;
  no pivotal dimension character at fermion=-1 is supplied.
* Nonreal third indicators of a self-dual object are not an obstruction
  to a general fusion category, or even by themselves to unitarity.
* The two-dimensional cyclic fixed space for the multiplication on 1+X
  in R1660 does not provide an associative separable algebra. The ambient
  associator remains unknown.

Thus **0 new whole-ring exclusions, 0 new models; both cases remain
unresolved** in this sub-investigation. The Morita link remains conditional.

## Sources and inherited inputs

* S.-H. Ng and P. Schauenburg, *Frobenius--Schur indicators and exponents
  of spherical categories*, Theorem 4.1,
  https://arxiv.org/abs/math/0601012.
* A. Davydov, M. Mueger, D. Nikshych and V. Ostrik, *The Witt group of
  non-degenerate braided fusion categories*, Section 2.1 (uniqueness of
  the positive spherical structure), Lemma 3.11 and Corollary 3.32
  (module dimensions), https://arxiv.org/abs/1009.2117.
* Morita invariance of the center: P. Schauenburg, *The monoidal center
  construction and bimodules*, J. Pure Appl. Algebra 158 (2001), 325--346;
  M. Mueger, *From subfactors to categories and topology II*,
  https://arxiv.org/abs/math/0111204.
* The project's existing `frontier_1660_phase_masses.tex`, Theorem
  `thm:1660-all-indicators`, and `frontier_1660.tex`/the forced third
  indicator theorem supply the indicator values used in (1).
* Tensor source: public `data/current_remaining_cases.py` recovered on
  29 October 2026; the checker verifies its two recorded SHA256 hashes.
