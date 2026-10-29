# R1660 and R941: a common fermionic obstruction and a smaller algebra target

29 October 2026. **Both rings remain unresolved. No categorification or
general nonexistence theorem is claimed.** This report works in the positive
spherical representative supplied by the project's previously proved
spherical/Galois reduction. It does not assert that every original complex
category is pseudo-unitary.

## 1. The fermion centralizer of R1660 is nonsplit and s-simple

Let C categorify R6_8_1660, let

\[
d=3+2\sqrt2+2\sqrt3+\sqrt6,\qquad D=4(1+d^2),
\]

and use source simples \(1,g,X,gX,\sigma,T=\sigma X\).
Let h be the unique nontrivial invertible in Z(C). The established center
analysis gives \(F(h)=g\), \(\theta_h=-1\), and says that these two
invertibles are the only integral central simples. Put
\(E=\langle h\rangle'\subset Z(C)\).

**Theorem.** E has dimension D²/2 and Müger center sVec. It does not split
as M tensor sVec with M nondegenerate. Its only fusion subcategories are
Vec, sVec, and E.

This conclusion was previously known for R941, but the present proof does
not assume a Morita link to R941, an algebra 1+X, or any particular center
rank/allocation. It applies independently to every hypothetical R1660
categorification in the positive representative.

### Exact inherited inputs

The only proper nontrivial fusion subcategories of C have based rings
\(\{1,g\}\) and \(\{1,g,\sigma\}\). Every one of X, gX, T generates C.
The complete central phase-mass theorem says that the central simples
whose forgetful images contain sigma are precisely eight objects, all with
restriction

\[
2X+2gX+\sigma+3T.
\]

Thus no nonintegral central simple forgets entirely inside the source
Ising subcategory. A simple without sigma, X, gX, or T would forget to
copies of 1 and g and would be integral; by the integral-center theorem
it is 1 or h. In particular Z(C) has **no simple of dimension sqrt(2)**.

These premises come from the published manuscript chapters
`frontier_1660.tex` and `frontier_1660_phase_masses.tex`, and the prior
`rank6_pair/INTEGRAL_CENTER_CHECK.md`. The new short checker verifies the
ring, subcategory lattice and dimension arithmetic; it does not replace
the categorical proofs of the inherited central restrictions.

### Dominant-image lemma

Every nonpointed fusion subcategory H of Z(C) forgets dominantly to C.
Indeed H contains a nonintegral simple, and its image contains one of
X, gX, T by the preceding restriction result. Each generates C. Therefore
FPdim(H) >= D.

Moreover equality is impossible: a dominant tensor functor of equal
FP dimensions is an equivalence, so it would give the source simple
sigma a simple preimage of dimension sqrt(2) in H, contradicting the
absence of such a central simple. Hence FPdim(H)>D. This proof does
not require any classification of braided categories.

### Nonsplitting

Suppose E=M tensor sVec with M nondegenerate. M is also nondegenerate
inside Z(C), so modular decomposition gives Z(C)=M tensor K, where
FPdim(K)=4. The centralizer K contains h. It can have no additional
integral simple because Z(C) has none. The two invertibles 1,h contribute
2 to its dimension. Each noninvertible simple has dimension strictly
larger than one, so the remaining dimension 2 must consist of exactly
one simple of dimension sqrt(2). This contradicts the absence just
proved. (There must be a remaining simple, since K has dimension four.)

### s-simplicity

First let H be a proper nonpointed fusion subcategory of E containing
sVec. Its centralizer H' in E contains sVec. If H'=sVec, the centralizer
dimension identity gives H=E. Otherwise H' is nonpointed, since the
integral part of E is exactly sVec. Both H and H' dominate C, so both
dimensions are at least D. But

\[
\operatorname{FPdim}(H)\operatorname{FPdim}(H')
=\operatorname{FPdim}(E)\operatorname{FPdim}(\mathrm{sVec})=D^2.
\]

They would therefore both have dimension D, contrary to the strict
dominant-image bound. No such H exists.

If a nontrivial H does not contain h, it cannot be pointed. Its join with
sVec is E by the preceding case. The Müger center of H is a symmetric
fusion category and is integral over C, so it lies in the integral part
sVec of E. Since H does not contain h, this Müger center is Vec. Hence H
is nondegenerate and E=H tensor sVec, contradicting nonsplitting. QED.

## 2. A uniform alternative proof for R941

The same nonsplitting proof works for R8_3_941 without its previous rank
34/37/40/43 list: its integral center is exactly {1,h}, and every
nonpointed source dimension is larger than sqrt(2). Consequently no
nonintegral central object can have dimension sqrt(2). A hypothetical
split centralizer would again force a four-dimensional factor containing
an additional sqrt(2) simple.

Its existing dominant-image argument then gives s-simplicity as above.
This is a simplification of the previous R941 theorem, not a new
classification decision. It also shows that the nonsplitting result is
independent of completeness of the old center-rank enumeration.

## 3. The algebra 1+X has only two cyclic multiplication directions

The previously proved third rotation on Hom(1,X³) has eigenvalue
multiplicities (2,1,0) or (2,0,1) for (1,omega,omega²). Thus its fixed
subspace has dimension two.

Suppose A=1+X is a connected separable algebra in C. In the positive
module-trace normalization it has a symmetric Frobenius form. The
trilinear functional epsilon composed with multiplication twice is
invariant under pivotal cyclic rotation. Restricting its three inputs
to X gives a vector in the fixed subspace of Hom(X³,1), equivalently
the dual fixed subspace of Hom(1,X³). Via the nondegenerate pairing on
X, this is the X-valued multiplication component X² -> X.

Therefore this component lies in a **two-dimensional** subspace of the
three-dimensional Hom(X²,X), rather than an arbitrary vector in that
space. Together with the scalar component X² -> 1, this leaves at most
three linear coefficients before normalization and gauge. This is only
a necessary reduction: the ambient associator, Frobenius normalization,
and nonlinear associativity equations are still unknown. In particular
it does not construct A and does not improve the unresolved census count.

## 4. All odd indicators in the proposed Morita link obey exact relations

This statement assumes actual Morita equivalence between positive
categorifications of R1660 and R941, for example if the required algebra
1+X has been constructed. It does not apply automatically to every
hypothetical R941 category.

In R941 let a=2+sqrt(2)+sqrt(3)+sqrt(6), b=a+sqrt(2), and retain d above.
There are two selfdual objects of dimension a, one dual pair of dimension
b, and two selfdual objects of dimension d. Write their odd indicators
as u1,u2; v,v; and w1,w2, respectively. If x=nu_n(X) and t=nu_n(T) in
R1660, then

\[
u_1+u_2=t,\qquad v=t/2,\qquad w_1+w_2=2x
\quad(n\ \text{odd}).
\]

Indeed the dimension-weighted indicator is Morita invariant, and
sqrt(2)d=a+b. Thus equality of the weighted totals reads

\[
1+a(u_1+u_2)+2bv+d(w_1+w_2)
=1+(a+b)t+2dx.
\]

The numbers 1,a,b,d form a basis of Q(sqrt(2),sqrt(3)). For odd n that
field is linearly disjoint from Q(zeta_n): each of its three quadratic
subfields has conductor divisible by four, while n is odd. Indicators
belong to Q(zeta_n), so coefficient comparison proves the identities.

For n=3 the four a/b cubic vacuum spaces have dimension one, whereas the
two d spaces have dimension three. The established x=2+omega, t=2
therefore force every a/b third rotation to be identity. The two d
rotations have combined eigenvalue multiplicities (4,2,0) for
(1,omega,omega²); hence their unordered traces are either
\(\{2+\omega,2+\omega\}\) or \(\{3,1+2\omega\}\).
The conjugate branch conjugates these expressions. These constraints
are feasible and yield no contradiction; they narrow the proposed
Morita construction's indicator target.

## 5. A tempting SU(2) level-22 match cannot give a direct condensation

One R941 dimension is
\(a=2+\sqrt2+\sqrt3+\sqrt6=\cot(\pi/24)\). This equals the quantum
dimension of the label-10 simple in SU(2) at level 22. The coincidence
does not give a model. The global dimension of that modular category is

\[
W=\frac{24}{2\sin^2(\pi/24)}
 =192+120\sqrt2+96\sqrt3+72\sqrt6
 =(3-\sqrt3)D.
\]

If its full right-module fusion category for a connected étale algebra
had dimension D, the algebra would have dimension 3-sqrt(3), strictly
between one and two. Every nontrivial connected algebra object has
dimension at least two: it contains the unit once and at least one
additional simple of FP dimension at least one. This rules out the
direct full-module construction. For a local-module construction the
required algebra dimension is sqrt(3-sqrt(3)), also between one and
two, so that route is likewise impossible. The adjoint SU(2) level-22
subcategory has dimension W/2 < D and cannot increase dimension by
condensation. The argument works for both R1660 and R941 because their
global dimensions agree, and covers Galois forms with the same based
ring.

Two more exact dimension matches can also be ruled out. Write
\(W_{10}=24(2+\sqrt3)\) and
\(E_6=\operatorname{FPdim}(\operatorname{Ad}(E_6))=6+2\sqrt3\).
Then

\[
W E_6=12D,\qquad W^2W_{10}=144D^2.
\]

The first identity suggests full modules over a dimension-12 connected
separable central commutative algebra in SU(2)_22 tensor Ad(E6);
the second suggests realizing the center as local
modules over a dimension-12 algebra in
SU(2)_22 tensor SU(2)_22 tensor SU(2)_10. Both are impossible.

Here is an exact positivity argument that avoids searching for algebras.
Put \(r=\sqrt2,s=\sqrt3,c=2\cos(\pi/24)\). In the independent basis
\((1,r,s,rs,c,cr,cs,crs)\), multiplication has nonnegative rational
coefficients because \(r^2=2,s^2=3,c^2=2+(r+rs)/2\). All the simple
dimensions lie in the real cyclotomic field
\(\mathbb Q(\zeta_{48}+\zeta_{48}^{-1})\), of degree eight, while
\(\mathbb Q(r,s)\) has degree four and does not contain c; this proves
the displayed basis is independent. All the simple
FP dimensions in the displayed source categories have nonnegative
coefficients in this basis. Their quantum dimensions follow from
\(q_0=1,q_1=2\cos(\pi/(k+2)),q_{j+1}=q_1q_j-q_{j-1}\).
The explicit lists show that the only tensor-product simples with
rational dimensions are the invertibles: four in the first source,
eight in the second. Since no irrational coefficient can cancel in a
nonnegative sum, every integral-dimensional object in either source
is supported on these invertibles.

A connected separable algebra supported on a pointed fusion subcategory
of rank m has dimension at most m. Indeed A is a simple right A-module;
for invertible g the free module gA is simple as well, and adjunction
gives \([A:g]=\dim\operatorname{Hom}_A(gA,A)\in\{0,1\}\).
The required dimension 12 exceeds respectively 4 and 8, proving both
obstructions. `quantum_routes.py` checks the dimension lists, all
products, and both exact global identities in under a second.

These exclusions concern the three specified direct constructions.
They do not classify arbitrary products, intermediate condensations,
extensions, or unrelated quantum-group constructions.

## 6. Attempts which did not resolve either ring

* The canonical central algebra attached to the source Ising subcategory
  has object 1+B7, with F(B7)=1+3X+3gX+4T=X². Its nontrivial
  augmentation factor therefore has the same underlying object as the
  regular internal end X², not underlying object 1+X. Equality of
  underlying objects does not identify the algebra structures. No
  new Morita category follows from this object calculation alone.
* The signed-permutation involution on the negative charge-conjugation
  space was tested as a possible new congruence obstruction. On that
  space, all odd twist exponents are exactly the spin phases, hence
  N(B7)=-S T^24 S^{-1}. The apparent commutator constraint that a signed
  permutation conjugates diagonal T to a commuting matrix is already
  automatic from the congruence representation of SL(2,Z/48). It cannot
  be counted as a new exclusion.
* The ordinary rank-four classification cannot be applied to the
  fermionic quotient of R941: it has genuine odd fusion channels.
  No pivotal structure on that quotient, or dimension character at
  fermion=-1, was silently assumed.
* Current quadratic-category classification results apply to a single
  orbit under invertible objects. The R1660 nonpointed dimensions are
  sqrt(2), d and sqrt(2)d; it is outside that domain. The regular Ising
  bimodule theorem and rank-eighteen relative-center ring are existing
  reductions, not constructions.

## 7. Precise outcome and sources

No new full-ring exclusion or model was found. R1660 now independently
requires a nonsplit s-simple fermion centralizer, even before constructing
the optional R941 Morita partner. The algebra construction target has
two cyclic X-valued multiplication directions. Both are necessary
conditions. A separate agent checked the nonsplitting and s-simplicity
proof, independently rebuilt the relevant induction Gram entry and
source-generation closures, and retained the stated inherited premises.

The categorical general inputs are DGNO, *On braided fusion categories I*,
Theorems 3.13–3.14 and Appendix B (https://arxiv.org/abs/0906.0620), and
the previously cited positive module-trace/symmetric-Frobenius normalization
in the audited pairing lemma. The connected-algebra normalization must
not be inferred from arbitrary semisimple algebra-object data without
those hypotheses.

