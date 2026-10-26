# R12_1_623 from a cyclic near-group category of order 36

This construction uses the complex spherical near-group existence theorem in
He–Liu–Lu–Palcoux–Ren, arXiv:2610.11652v1 (8 October 2026). It does not assume
the unitarity conjecture in that paper. The resulting fusion category has
exactly the R12_1_623 fusion tensor, as checked independently in
`verify_R623_model.py` against the frozen census tensor.

## 1. The actual precursor

Write N=C36 additively. Theorems 2.3 and 2.10 of
[He–Liu–Lu–Palcoux–Ren](https://arxiv.org/html/2610.11652v1) construct a
complex spherical category with simples N and one object X, with

    gX=Xg=X,       X²=Σ(g∈N)g+36X.

Their Eq. (2.19) has

    χ(g,k)=exp(2πigk/36),
    a(g)=exp(πig(36−g)/36).

The initial categorical dimension is 18−6√10; its Frobenius–Perron dimension
is 18+6√10. Lemma 2.14 gives the dictionary to Izumi's scalar data:

    b(g,k)=χ(g,k)⁻¹,       a_I(g)=a(g)⁻¹.

Theorem 2.3 is algebraic reconstruction, so existence here does not depend
on the later conjecture about a unitary structure at order36.

## 2. Algebraic version of the isotropic orbifold calculation

We use the following version of Izumi's orbifold calculation for this
explicit algebraically reconstructed category. Let H⊂N satisfy b|H×H=1.
The category of modules over the central regular H algebra is a fusion
category. If H=H⊥, its simples are

    {u_g : g∈N/H} and {u_g σ : g∈N/H},

with the free inversion action and pointed part

    σu_g=u_(−g)σ,
    σ²=u_(−g_a)+Σ(g∈N/H)m_g u_g σ,
    a_I(h)=b(h,g_a) for h∈H.                         (1)

The nonnegative integer coefficients m_g are determined in our particular
case in Section3 directly from the fusion axioms.

Here is the needed algebraic justification, including the point which
prevents an unsupported application of a C* theorem.

Evans–Gannon, [arXiv:1208.1500](https://arxiv.org/pdf/1208.1500),
Section4.3, Eqs. (4.48)–(4.50), construct the central lifts of the
invertibles of a multiplicity-|N| near-group category. Their half-braiding
equations are (4.6)–(4.10); on two invertibles the half-braiding is b(g,k).
These are equations between compositions and sums of morphisms, rather
than positivity inequalities. For the present category they hold with
dual bases and inverse mixed vertices: the parameter dictionary above and
the algebraic vertex-transport identities in TPE Section4.7, especially
Lemma4.14, supply precisely these identities without a Hermitian adjoint.
All scalar denominators are nonzero (36, the nonzero categorical dimension,
and roots of unity). Thus the same morphisms are central half-braidings in
the complex category.

The only non-scalar mixed block can be seen directly in the TPE basis
v_x of Hom(X²,X). In the paper's convention its three transports are

    Z(g)v_x=χ(g,x)v_x,
    X(g)v_x=v_(x+g),
    Y(g)v_x=[a(x)/a(x−g)]v_(x−g).

They obey X(g)Y(g)Z(g)=a(g)⁻¹ Id. Indeed their diagonal coefficient is
χ(g,x)a(x)/a(x−g)=a(g)⁻¹ by the even quadratic-refinement identity.
Multiplication by the correcting scalar a(g) makes this block the
identity. The pointed blocks use the same refinement identity and
bicharacter multiplicativity. These are the mixed-block checks in the
central-invertible hexagons; no coefficient of the all-X associator or
positivity condition enters them. The replay verifies the displayed
mixed-block identity exactly for all36² pairs of indices.

Their products give a central lift of N. One can also check coherence
without choosing additional scalar data: this near-group category has
trivial universal grading, since X² contains every simple. Consequently
Aut⊗(Id)=1, so a half-braiding on a fixed invertible is unique. The pointed
associator is trivial: the fixed simple X supplies a rank-one module for
the pointed category. Hence, when b|H×H=1, A=⊕(h∈H)h is a commutative
separable algebra in the center, with ordinary group multiplication. Its
forgetful image is connected. The category C_A is therefore a fusion
category with relative tensor product; no operator-algebra realization is
required.

For completeness, the part of
[Izumi, arXiv:1512.04288v2](https://arxiv.org/pdf/1512.04288v2),
Section12.1 and Theorem12.5, needed to compute this module category is a
finite character-idempotent calculation. The induced X has endomorphism
algebra C[H], with primitive idempotents

    e_λ=|H|⁻¹ Σ(h∈H) λ(h)⁻¹ L_h.

Here L_h are the regular H operators, and λ ranges over Ĥ. Splitting these
idempotents gives pairwise distinct simples σ_λ. Left multiplication by
u_g shifts λ by −b(−,g)|H, whereas right multiplication shifts it by
+b(−,g)|H. Nondegeneracy and H=H⊥ make both actions free and transitive.
Thus σ=σ_0 has the inversion mixed rule in (1).

In σ² the projector on a pointed channel g is the character average

    |H|⁻¹ Σ(h∈H) a_I(h)b(h,g)
      = 1 if g+g_a∈H⊥, and 0 otherwise.

The pointed channels in a common H coset identify under induction, giving
the single summand u_(−g_a). The pointed-channel inclusions and projections
in the proof of Theorem12.5 multiply to Kronecker deltas and sum to the
pointed part of the product idempotent. In a C* realization they are
written as isometries and their adjoints. Here they are mutually dual
inclusion/projection maps; the same identities hold. Thus the pointed
calculation computes the complex module category without unitarity.
The remaining multiplicities will be forced below directly from the
fusion axioms, so no transfer of Izumi's noninvertible-channel projection
calculation is needed.

This is the isotropic theorem, not its stricter Corollary12.7: the latter
also assumes a_I|H=1 and would incorrectly erase the shifted pointed term.

## 3. Specialization to H=6C36

For h=6j and k=6l,

    b(h,k)=exp(−2πijl)=1,
    H⊥=6C36=H,
    a_I(6j)=exp(−πij(6−j))=(−1)^j.

The character a_I|H corresponds to g_a≡3 modulo6, since
b(6j,3)=exp(−πij)=(−1)^j. Thus N/H=C6 and u_(−g_a)=u_3 is its unique
involution z. At this point the free inversion action and the unique
pointed term have been established, so write

    σ²=z+Σ(g∈C6)m_g gσ,       m_g nonnegative integers.

The inversion rule and associativity of σ²u_a=u_aσ² give
m_(g+2a)=m_g. Thus the even coefficients have one value A and the odd
coefficients another value B. The pointed term determines σ*=zσ.
Since z commutes with σ and z²=1, (σ*)²=σ². Taking duals in the displayed
square therefore gives m_(g+3)=m_g, so A=B. Each σ has FP dimension
d=(18+6√10)/6=3+√10. Comparing dimensions with d²=1+6d gives
3(A+B)=6. Consequently A=B=1. The complete rules are

    G=C6,       σg=g⁻¹σ,
    σ²=z+Σ(g∈G)gσ,       σ*=zσ.

These are exactly the requested R623 rules. There are six invertibles
and six noninvertibles of FP dimension

    (18+6√10)/6 = 3+√10.

Every product is multiplicity-free. In coordinates g^i and g^iσ, the
complete multiplication is

    g^i g^j = g^(i+j),
    g^i (g^jσ) = g^(i+j)σ,
    (g^iσ)g^j = g^(i−j)σ,
    (g^iσ)(g^jσ) = g^(i−j+3)+Σ(k=0..5)g^kσ,

with all exponents modulo6. The coordinate-to-census map is

    [0,1,10,11,9,2,3,8,5,4,7,6].

The replay compares all1728 structure constants, including the unit and
duality, and checks the isotropy and shifted-character calculation with
exact modular arithmetic. It checks the application of the cited
existence theorem; it does not numerically approximate an associator or
replace the categorical proof.

## 4. A uniform family

The same construction works for every k≡2 modulo4. Start with the cyclic
near-group category C_(k²)+k² from the same existence theorem and condense
H=kC_(k²). Its bicharacter is trivial on H×H and H=H⊥. The quadratic
refinement restricts as

    a(kj)=exp(πij(k−j))=(−1)^j,

so the pointed square term is z=u_(k/2). The quotient has k invertibles
and k noninvertibles, with inversion mixed action and

    FPdim(σ)=(k+√(k²+4))/2.

Associativity makes the noninvertible coefficients constant on parity
classes. Duality shifts them by k/2, which is odd by hypothesis, and
therefore makes the two values equal. The dimension equation then makes
every coefficient one. Thus these complex fusion categories uniformly
realize

    σg=g⁻¹σ,       σ²=z+Σ(g∈C_k)gσ,
    σ*=zσ,         k≡2 (mod4).

The k=2 fusion rules are those of pseudo-PSU(2)_6; k=6 is the present
R623 model. This corollary does not assert a tensor equivalence to any
particular associator in the k=2 case. No claim for k divisible by4 is
needed: in that case the elementary duality step alone would not force
the two parity coefficients to coincide.

## 5. Scope

This establishes a complex categorification of R12_1_623 by a known
near-group construction combined with the algebraic isotropic quotient.
It supplies no model for the commutative rings R561 or R628: the quotient's
right action is inversion. It does not claim that the order36 precursor,
or this quotient, is unitary. A proof of unitarity is unnecessary for the
Grothendieck-ring categorification claim.

Independent audits are recorded in
`../premises/R623_model_audit.md` and
`../semion_structure/R623_construction_audit.md`. The premises audit has
its own full-tensor verifier, independently discovering the same basis
map. The earlier algebraic-orbifold route review is retained at
`commutative/R623_algebraic_orbifold_audit.md`; the present proof uses the
shorter intrinsic multiplicity argument in Section3.
