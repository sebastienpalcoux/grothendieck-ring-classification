# A unitary model for R9_2_1254 by descent of an order-four cover functor

## Result and outline

The ring R9_2_1254 is realized by a coherent C2 equivariantization of a
unitary generalized Moore–Read category of dimension16. The new action
comes from a mixed order-four tensor functor on the dimension32 covering
category. Its square becomes tensor-isomorphic to the identity only after
central boson condensation. Requiring the cover functor to have square
identity would incorrectly discard this construction.

The certificate is `mr_order4_descent_2_3_1_4.json`: it gives every
root-of-unity tensorator scalar and every component of the square
isomorphism. `mr_order4_descent.py` checks all required equations. The
categorical argument below explains why those equations suffice.

## 1. The existing unitary cover and its central algebra

Use a unitary Ising category I with simples1,psi,sigma, and P=Vec(C16,Omega),

    Omega(a,b,c)=zeta^(2a floor((b+c)/16)), zeta=exp(2 pi i/16).

Let B be the parity subcategory of I boxtimes P: its simples are(i,a),
with i=0,1,2 for1,psi,sigma, and a even for i=0,1 and odd for i=2.
There are24 simples and FPdim(B)=32. The invertible

    g=(psi,8)

has right half-braiding g tensor(i,a)->(i,a)tensor g of scalar

    beta(i,a)=zeta^(7a+e_i),  (e_0,e_1,e_2)=(0,8,12).

It has order2 in Z(B), self-braiding1, and trivial associator on its powers.
Indeed the pointed square correction is zeta^(2a), giving
beta_pointed(a)^2*zeta^(2a)=1; the Ising central fermion squares to1.
The regular algebra A=1+g is commutative, separable and central. Its
multiplication g tensor g->1 is the identity in the chosen skeletal basis.
Thus D=B_A is a unitary fusion category of dimension16.

These are precisely the explicitly verified cover and central algebra in
`phase2/weak_integral/mr_orbifold.md`, with the right-half-braiding
orientation made explicit.

## 2. The order-four mixed tensor functor

On simple objects define

    F(i,a)=(i xor (a/2 mod2),3a mod16),   i=0,1;
    F(2,a)=(2,3a mod16).

This preserves every fusion coefficient and the unit. The file lists the
scalar J_F(a,b;c) in mu_16 on every multiplicity-one fusion channel,
with tensorator orientation F(a)tensor F(b)->F(a tensor b).
F is linear on each chosen elementary morphism and permutes channel
labels in the obvious way. Its tensor-functor equations are verified
entry by entry against the cover's actual F-symbols, not only the fusion
rules. All nonzero Ising F-symbol magnitudes are preserved: the only
nontrivial magnitude1/sqrt2 occurs for three sigma inputs, and F fixes
the Ising type of those inputs. Consequently checking the phase of every
nonzero entry checks the entire tensor-functor diagram.

The actual F-symbol exponent is the standard Ising sign times8, plus
`2 a floor((b+c)/16)` from the charge factor. The script checks all18432
nonzero associator entries and the unit constraints. Since J is unitary
and the object map is a permutation, F is a unitary tensor autoequivalence.

F(g)=g. The certificate additionally verifies every central transport
identity

    J_F(g,a;ga)/J_F(a,g;ga)=beta(Fa)/beta(a).

Choose an algebra isomorphism phi:F(A)->A which is identity on1 and has
scalar c=zeta32^2 on g (equivalently c=zeta16). Here the saved value is
J_F(g,g;1)=zeta16^2, so c^2=J_F(g,g;1). This is exactly the algebra
multiplication compatibility. The central transport equations make phi
an isomorphism of central algebras. Therefore F descends to a unitary
tensor autoequivalence f of D.

## 3. Squaring before and after condensation

On B, F^2 is not the identity object map. It is

    K(a)=g^p(a) tensor a,

where p(a)=0 for an even Ising object and1 for a sigma object. Equip K
with its canonical tensorator: move the central g factors to the left
using the right half-braiding, and multiply g^2=1. More explicitly,
reassociate

    (g^p a)(g^q b) -> g^p(a(g^q b))
      -> g^p((a g^q)b) -> g^p((g^q a)b)
      -> g^p(g^q(ab)) -> (g^p g^q)(ab) -> g^(p+q)(ab).

The middle interchange contributes beta(a)^(-q). All other contributions
are specified cover associators. The script independently verifies the
resulting J_K against all18432 tensor-functor equations.

The certificate supplies a natural isomorphism d:F^2->K on the common
underlying simple objects. Its phases satisfy for every channel a b->c

    d(a)d(b)/d(c)
      =J_F(a,b;c) J_F(Fa,Fb;Fc)/J_K(a,b;c).

This is exactly monoidality of d. It also satisfies

    d(g)=J_F(g,g;1)=c^2.

Thus d intertwines the algebra map phi F(phi):F^2(A)->A with the
identity algebra map K(A)->A. It descends to the module categories.

On D, K is canonically tensor-isomorphic to the identity. On a free
module q(a), use q(g)^p tensor q(a)->q(a), where q(g)->1_D is supplied by
the regular algebra multiplication. The tensorator of K was defined
by precisely the central movements appearing in this map. Its
monoidality uses beta(g)=1 and the group-algebra relation g^2=1. Hence
f^2 is tensor-isomorphic to Id_D.

## 4. Coherent C2 action, with no unresolved obstruction

For completeness there are two ways to finish coherence.

First, the canonical universal grading of D is C8: writing its simples
as u^a(a in C8) and X_r(r in C4), their degrees are2a and2r+1 modulo8.
Its adjoint subcategory has basis1,u^4, as follows from
X_r X_r^*=1+u^4. Therefore Aut_tensor(Id_D)=Hom(C8,C*)=C8. The functor f
acts on this group by multiplication3. The obstruction to upgrading an
order-two tensor-equivalence class to a C2 action lies in

    H^3(C2,C8_3)=ker(1+3)/(3-1)C8=2C8/2C8=0.

Thus the action coherence can always be corrected. This is the standard
monoidal-action obstruction (a direct cyclic coherence calculation), not
an assertion that H4 alone supplies an extension.

Second, for the displayed certificate the correction is explicit. If
phases are written as exponents mod16, replace d(a) by

    d_new(i,a)=d(i,a)-4a modulo16.

This multiplies d by the universal-grading character with parameter-2.
Before correction the C2 coherence defect is the parity character;
after correction it is identically1. In the saved bases the defect,
written as an exponent mod32, is

    2d(Fa)-2d(a)-p(a)(J_F(g,g;1)-2J_F(g,a;ga)).

The script `mr_1254_model.py` checks that it is16 on odd objects and0 on
even objects before correction, and0 everywhere afterwards; the final
phases still satisfy all monoidality and algebra compatibility equations.
Every correction is unitary. This produces an actual coherent unitary
C2 action on D.

## 5. Fusion tensor and census identification

In D use representatives(1,2a) for u^a, and(sigma,1+2r) for X_r. Then

    u^a u^b=u^(a+b),     u^a X_r=X_r u^a=X_(r+a),
    X_r X_s=u^(r+s+1)+u^(r+s+5).

The descended involution acts by

    u^a ->u^(-a),    X_r ->X_(3r+1).

It fixes1,u^4; it has three two-element pointed orbits, and two
two-element odd orbits. The equivariantization E=D^C2 therefore has
rank9 and dimensions1^4,2^3,(2sqrt2)^2. The odd orbits are exchanged by
duality, giving the feature missing from the earlier model389.

For the fixed object u^4, the certificate has d_new(u^4)=14 and
J_F(u^4,u^4;1)=14 modulo16. Thus its equivariant lifts have square1,
and the invertible group is V4. A later action-coherence correction by a
universal-grading character cannot change this, because deg(u^4)=0.

The full tensor is computed by the invariant-subspace formula. For a
fixed output the multiplicity is(dim+trace)/2; only fixed input objects
contribute to the trace. These inputs are1 andu^4, whose representatives
are literally fixed in the cover, so the relevant phases are exactly the
saved J_F and d_new entries. For a free output orbit use the dimension at
one representative. This determines every fusion coefficient.

`mr_1254_model.py` verifies all ring axioms and matches all729 coefficients
of R9_2_1254 with source-to-model basis permutation

    [0,8,7,5,6,1,2,4,3].

`mr_1254_model.json` includes the full rank9 tensor, rank12 quotient
tensor, action, corrected coherence phases and equivariant orbit labels.
The model is unitary by construction from unitary categories, a central
unitary separable algebra, and a coherent unitary finite-group action.

## Scope and references

The proof establishes categorical existence for this fusion ring. It
does not classify all its categorifications or assert tensor-equivalence
novelty of the resulting category.

- S.Gelaki,D.Naidu,D.Nikshych, Centers of graded fusion categories,
  arXiv:0905.3117, Sections2.4–2.5, for actions and central condensation.
- J.Dong,S.Natale,H.Sun, A class of prime fusion categories of dimension2^N,
  New York J.Math.27(2021),141–163,
  https://nyjm.albany.edu/j/2021/27-5p.pdf, for the generalized Moore–Read
  setting. Existence and the required action here are specified directly.
- P.Etingof,D.Nikshych,V.Ostrik, Fusion categories and homotopy theory,
  arXiv:0909.3140, for the obstruction-theoretic formulation of tensor
  actions; the relevant cyclic H3 calculation is supplied above.
