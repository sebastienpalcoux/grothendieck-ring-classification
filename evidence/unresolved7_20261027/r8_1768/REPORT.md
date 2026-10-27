# R8_3_1768: audit, stronger route obstruction, and a different arithmetic input

Date: 27 October 2026. This is offline research against repository snapshot
`6a426acf6465dd674351be92dcca41b72f371521`.

## Outcome

**R8_3_1768 remains unresolved.** This pass proves a substantially
stronger restriction: every nonregular Morita representative has no
quaternionic invertible simple. In particular **no category with the
GH(C6,2) fusion rules can be Morita equivalent to R1768**, for any
associator or algebra object. The proof combines a new pivotal
Frobenius pairing-parity criterion with a subsecond exact check of all
21 previously retained module factors. It is recorded in
`MORITA_QUATERNIONIC_RIGIDITY.md` and has an independent categorical
and exact-profile audit in the companion `r8_928_941` folder.

The simpler initial version, already excluding every `1+sigma` algebra
route without a module-factor enumeration, is in
`UNIVERSAL_GH6_ROUTE_OBSTRUCTION.md`. These are restrictions on possible
constructions, not a general categorification exclusion.

The old RW wrong-dual result withstands the audit below. A different
arithmetic input is also constructed explicitly in section 3; it does
not evade the new universal Morita obstruction. Equivalence or
inequivalence of the two actual precursors has not been established.

## 1. Audit of the previous wrong-dual argument

The previous proof is
`../../unresolved10_20261027/r8_quadratic/R1768_DUAL_OBSTRUCTION.md`.
Its conclusion is about the particular actual RW category, not all
categories with the same fusion rules. That restriction is essential.

I checked the following logical steps separately.

* The two maps `t'_0,t'_1` are independent: they are paired with the
  two displayed unprimed intertwiners by the identity matrix. Thus their
  lines cannot be identified by a change of scalar on the simple
  summand.
* Transport by the pointed involution takes the first parent algebra
  line to the second. The transport uses the tensor-square intertwiner
  `Z tau(Z)`, not `Z^2`. Replacing the former by the latter would erase
  the crucial distinction.
* The finiteness argument proving that the mixed coefficient is nonzero
  uses only finiteness of module categories of **fixed rank**. The
  hypothetical conic has rank eight throughout, by its fixed induction
  Gram matrix. A connected algebra is the internal end of its simple
  regular module; therefore one cannot evade the argument by having
  infinitely many algebras in finitely many module categories.
* An invertible bimodule sends the simple regular right module to a
  simple right module of the same FP dimension. The six modules `g^j A`
  are exactly the modules with that dimension. The remaining two have
  dimension `6u`, where `u=6+sqrt(37)`, and are too large.
* For `g^j A` to acquire an invertible left action, there must be an
  algebra isomorphism `A -> g^j A g^(-j)`. Only `j=0,3` can even preserve
  its underlying object. At `j=3` the two algebra classes are exchanged;
  at `j=0` the nonzero trivalent product kills the possible nontrivial
  scalar automorphism. Thus the dual has exactly one invertible simple.

There is no missing unitarity hypothesis in these steps. There is also
no implication from the two earlier commuting based actions to an
actual invertible bimodule category. The proof correctly refuses that
implication. Its conclusion continues to prevent declaring R1768
modelized by the algebra already constructed.

The rigidity input is ENO, *On fusion categories*, Corollary 2.35:
<https://annals.math.princeton.edu/wp-content/uploads/annals-v162-n2-p01.pdf>.

## 2. Strengthening: changing Galois form, opposite, or gauge does not repair it

Let `H` be that actual precursor. For every algebraic Galois transport
of `H`, all translated objects `1+g^j sigma` still have exactly the two
algebra classes described in the previous proof, and both corresponding
duals still have only the tensor unit as an invertible object.

Here is the reason, without a positivity premise. Choose a number field
containing the structural coefficients of the fusion category and the
displayed algebra products. Algebra associativity, the unit equations,
and the displayed splitting of multiplication are polynomial identities
over that field. Extending a field embedding to an automorphism of an
algebraically closed field transports these identities and their
solutions bijectively. Transport in the reverse direction would turn
any purported additional separable algebra into an additional one in
`H`, contradicting the previous classification on this object.

Equivalently, one can transport the entire proof: nonzero coefficients
remain nonzero, the two lines remain independent and exchanged, and
the based fusion rules and number of invertible objects are unchanged.
No new spherical or unitary structure is needed for this reasoning.

Passing to the opposite category sends an algebra to its opposite and
the bimodule category to the corresponding opposite. This preserves
invertibility and its number of isomorphism classes. Tensor equivalences,
changes of bases, choices of square roots in the same gauge orbit, and
cohomologous changes of the pointed cocycle do likewise.

Therefore none of these operations rescues the existing `1+sigma`
construction. This statement still does not rule out a different
associator orbit, a different algebra object in the old category, or a
different construction of R1768.

## 3. A second exact RW arithmetic input

The old construction used

\[
 A_0=\begin{pmatrix}12&1\\1&0\end{pmatrix},\qquad
 \gamma_0=A_0^2=\begin{pmatrix}145&12\\12&1\end{pmatrix}.
\]

Consider instead

\[
 A_1=\begin{pmatrix}7&12\\3&5\end{pmatrix},\qquad
 \gamma_1=A_1^2=I+12A_1
 =\begin{pmatrix}85&144\\36&61\end{pmatrix}.
\]

Both matrices `A_i` have determinant minus one and trace twelve. The
new `gamma_1` has determinant one and trace 146. Since `A_1` is
unimodular, the row lattice of `gamma_1-I` is exactly `12 Z^2`, so the
RW group is again `G=C12 x C12`. Its positive fixed point is
`tau=(1+sqrt(37))/3`, and

\[
 36\tau+61=73+12\sqrt{37}=(6+\sqrt{37})^2.
\]

Substitution into RW's definitions gives, for `u=(x,y),v=(a,b)`,

\[
 B_1(u,v)=\exp\!\left(\frac{2\pi i}{12}
 [7xb+7ya+3yb]\right),
\]

\[
 q_1(x,y)=\exp\!\left(\frac{2\pi i}{24}
 [14xy+3y^2+12y]\right).
\]

These formulas are exact on the group. The term eliminated from the
Gaussian is `12(x-x^2)`, which is divisible by 24.

The eta multiplier is one. The exact Dedekind sum is
`s(61,36)=19/216`, and its exponent is

\[
 \frac{146}{432}-\frac{19}{216}-\frac14=0.
\]

In particular RW supplies an actual finite quantum dilogarithm `E_1`
and an actual complex near-group category for this input. This uses the
construction theorem for the specified solution, not a classification
of every spherical near-group category.

### The required twisted quotient still exists

Set

\[
 L_1=\{(x,0)\},\quad
 H_1=\{(x,6t):x\in C_{12},t\in C_2\},\quad
 K_1=\{(2x,0):x\in C_6\}.
\]

Then `L_1=L_1^perp`, `q_1|L_1=1`, and `H_1^perp=K_1`. On `H_1`,

\[
 B_1((x,6t),(a,6s))=(-1)^{xs+at},\qquad
 q_1(x,6t)=(-1)^{xt+t}.
\]

The cocycle `omega((x,6t),(a,6s))=(-1)^(ta)` has commutator `B_1|H_1`.
Thus every hypothesis used in the previously audited twisted
crossed-product construction holds again: `q^2|H=1`, the required
commutator identity, complete twisted-group-algebra blocks, and the
rank-one/rank-two projector calculations. Repeating that construction
gives an actual twisted `GH(C6,2)` precursor.

The quotient generator is represented by `(0,1)`, and
`B_1((0,1),(0,6))=-1`. Its pointed associator is class 3 in
`H^3(C6,C*)=Z/6`, exactly the anomaly required by the old R1768 based
Morita data.

The metric datum itself is isometric to the old one. An explicit map
from old to new coordinates is

\[
 (x,y)\longmapsto(2x+11y,5x+7y)\pmod {12}.
\]

It preserves both `B` and `q`, not just their underlying groups, and
takes the old diagonal isotropic subgroup to `L_1`. The exact verifier
checks the quadratic identity at all 144 points and the bicharacter
identity at all 20,736 pairs.

### Why this does not already supply the desired algebra

The old norm-minus-one matrix acts trivially on its diagonal subgroup.
The new matrix acts on `L_1` as

\[
             (x,0)\longmapsto(7x,0)\pmod {12}.
\]

Consequently the previous fixed-coset proof of `E(l)=1` for every
nonzero isotropic `l` does not transfer. It cannot be used to manufacture
the old two pure algebra lines in this precursor. Conversely, this
difference is not a proof that a mixed multiplication exists.

There is no established equivalence or inequivalence of `E_1` and the
old solution under metric automorphisms and Galois action. If they belong
to the same transported categorical orbit, section 2 applies. If they
do not, a separate algebra check would be necessary for an algebra
construction. The alternative input is an actual precursor with exact
prerequisites, not a categorification claim. The new theorem in
`MORITA_QUATERNIONIC_RIGIDITY.md` now rules out obtaining R1768 from
this precursor by **any** Morita duality, even if a different algebra
could be constructed in it.

## 4. The earlier two-line condition and its limit

The pointed-involution argument has a converse necessary form that is
independent of the chosen arithmetic solution. In a category with these
`GH(C6,2)` rules, let `A=1+sigma` be a connected separable algebra, with
the right-module induction factor from the previous proof. If its dual
has a nonidentity invertible object, then

\[
                A\cong g^3 A g^{-3}\quad\text{as algebras}.
\]

Indeed the FP dimensions and conjugation rule leave only `g^3 A` as
the possible underlying nontrivial invertible bimodule; the internal-end
argument in section 1 then gives the displayed algebra isomorphism.

In the explicit crossed-product presentation, conjugation acts
nontrivially on the projective line
`P Hom(sigma^2,sigma)`: the transport of the first basis line is the
second, independently of the values of `E`. Its square is projectively
the identity by the coherence for the order-two pointed object. Over
the complex numbers a nontrivial projective involution has exactly two
fixed points. Thus a successful multiplication must lie on **one of
two fixed projective lines**, rather than at an arbitrary point of the
two-channel coefficient space.

This is only a projective necessary condition: the normalized action
on multiplication coefficients also depends on the transport of the
unit-output pairing. No conclusion about its scalar square is drawn
from the one-direction line transport. The new Frobenius-parity proof
bypasses that normalization issue and rules out the desired R1768 dual
in all cases. Thus the existence of projective fixed lines must not be
advertised as a surviving construction route.

## 5. Reproduction and source scope

Run `python verify_alternative_precursor.py` and its `python -O`
variant from this directory. Both complete in well under one second
and use explicit exceptions. They verify the integral matrices, the
full metric isometry, the cocycle, its commutator, all subgroup
orthogonality claims, the eta exponent, and the cyclic anomaly. They
do not purport to verify a new algebra or its dual.

Primary source for the finite quantum dilogarithm and complex
near-group reconstruction: Radchenko--Wheeler, *Real quadratic fields
and finite quantum dilogarithms I*, arXiv:2609.21892v2, equation (3),
Theorem 2, and Theorem 12:
<https://arxiv.org/html/2609.21892v2>.

The remaining categorical steps are the project's explicitly audited
twisted crossed-product proof, applied with the checked new metric
data. Neither that theorem nor RW parameterizes every categorification
of the target. No online data, manuscripts, or case status were changed.
