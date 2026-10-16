# A unitary realization of R7_4_2665 by inversion descent

**Theorem.** The census ring R7_4_2665 has a unitary categorification.
The construction starts with the established near-group category NG(C16,16),
descends its regular-group Morita self-equivalence through an isotropic subgroup,
forms a coherent C2 crossed product, and takes a reflection-algebra Morita dual.
The associator of the pointed part distinguishes this case from R7_4_2603.

Throughout, let t=2+sqrt(5). Groups in the first four sections use additive
notation, while r denotes a generator in a quotient group of order four.

## 1. The known orbifold input

Use Budinski's unitary solution J16^1, with near-group data

    G=C16, chi(g,h)=exp(2*pi*i*3gh/16),
    a(g)=exp(-pi*i*3g²/16), c=exp(pi*i/4).

Its existence is the already used R8_1_12 input: Budinski, Theorem 3.1.1,
Table 3.1, and the exact-certification discussion in Section 3.3.2.
Set H=4C16. Then H=H-perp, chi restricts trivially to H, and a(4)=-1.
Izumi's central lifts of invertibles make the regular H algebra A a
commutative separable algebra in Z(C). Central de-equivariantization gives
the unitary category D=C_A. Theorem 12.5 of Izumi gives its rules

    r⁴=1,  rho r=r^(-1)rho,
    rho²=r²+(1+r+r²+r³)rho.

Thus D has four invertibles and four simples of dimension t. This is the
existing R8_1_12 construction; no new near-group solution is asserted.

Let T generate the canonical dual H-hat=C4 action on D. It fixes r and
cycles the four noninvertibles. The universal grading of D is trivial:
rho² contains rho and all r^j rho, so their degrees, and then those of
all invertibles, are trivial. In particular Aut_tensor(Id_D)=1.

## 2. The parent Morita self-equivalence and its center action

Izumi Theorem 11.3 constructs the dual of the regular C16 algebra and
identifies it with C, preserving the near-group labels. In its factor
model, kappa:M^alpha -> M is the inclusion and

    alpha'_g=Ad U(-g)|_(M^alpha),
    alpha_h kappa=kappa,
    kappa alpha'_g=Ad U(-g) kappa,
    alpha_h(U(g))=chi(h,g)U(g).

Write Mcal for the resulting C--C Morita bimodule. Its simples are one
object a0=kappa of normalized dimension four, fixed by G, and sixteen
objects b_lambda of dimension t on a free G-orbit. The internal end of
a0 is the regular G algebra. H²(C16,C*)=0 makes that algebra structure
unique. The opposite Morita bimodule has the same distinguished fixed
object and internal-end algebra, so it is equivalent to Mcal as a left
module. Consequently Mcal squared is the regular bimodule with a tensor
autoequivalence G0 on the right. This is the argument of
Grossman--Jordan--Snyder, Lemma 4.7 and Remark 4.8: only uniqueness of the
regular algebra is needed here, not their prime-order assumption.

The center action is **inversion**. To see the sign explicitly, the
commutant of rho kappa is spanned by U(h). Since Ad U(h) rho=rho alpha_h,

    Ad rho(U(g))(U(h))=chi(h,g)^(-1)U(h).

For p_lambda=(1/16) sum_h lambda(h)^(-1)U(h), the left alpha_g action
sends p_lambda to p_(lambda chi_g^(-1)). The right alpha'_g action,
transported through rho(U(g)), sends it to p_(lambda chi_g).
Thus left g and right -g act alike on the free b-orbit. Every invertible
of C has a central lift (Izumi Theorem 13.4), and that lift is unique
because C has trivial universal grading. The faithful free-orbit action
therefore identifies the Morita center permutation as g -> -g.

The square fixes all central-invertible labels. Izumi Corollary 13.5
identifies Aut_tensor(C) faithfully with a subgroup of Aut(G), so G0 is
tensor-isomorphic to Id. Hence Mcal squared is the regular bimodule.
Inversion preserves H and the central algebra A, including its
multiplication.

## 3. Central base change and an actual inversion autoequivalence

We use the following base-change fact, with its necessary choice included.
For an invertible C--C bimodule whose center equivalence preserves A,
choose an algebra isomorphism from the transported A to A. Its category
of left A-module objects is an invertible C_A--C_A bimodule; the chosen
isomorphism balances the right action. Central base change commutes
with relative tensor product. Indeed the two sides classify the same
balanced functors with a compatible A-action: centrality moves A
through the balancing variable, and separability splits the coequalizer.
This also verifies compatibility with associators and with inverse
bimodules. If two choices of the algebra identification differ, their
descendants differ by the corresponding algebra automorphism of A.

Here Aut_alg(A)=Hom(H,C*)=C4, since A has distinct simple summands and
multiplication forces the component scalars to be a character. These
automorphisms give precisely T^j. Since the parent bimodule squares to
the regular bimodule, the descended bimodule L satisfies

    L tensor_D L = D_(T^j)

for some j modulo four. The assertion is at the bimodule level.

The fixed a0 object has four left A-module structures, all of normalized
dimension one, since H²(C4,C*)=0. The sixteen free b-objects give four
induced simples of dimension t. The left D-invertibles act freely on
the four dimension-one simples. Moreover rho a0 is the sum of all
sixteen b-objects before descent. After descent, Q(rho) is the sum of
the four dimension-t simples of D, each acting nontrivially, and their
images exhaust the four dimension-t module simples once each. Thus
tensoring with any chosen dimension-one module simple is an equivalence
of left D-modules D -> L. The right action gives a tensor autoequivalence F.

Its effect on r is determined by a scalar calculation. Represent a left
A-action on kappa by scalars lambda_h:alpha_h kappa -> kappa. The central
crossing from Izumi Theorem 13.4 shows that left alpha_g multiplies
lambda_h by chi(h,g). Right alpha'_g is identified with kappa through
U(g), and transports the action to

    U(g) lambda_h alpha_h(U(g)*)=chi(h,g)^(-1)lambda_h.

The right action on left A-modules extends the original right C-action;
the chosen identification of the H algebras supplies its balancing and
does not change this computation on free descended objects. Thus
F(r)=r^(-1). It sends rho to some r^k rho. Changing the A-identification
by a character composes with T, so choose it such that

    F(r)=r^(-1),  F(rho)=r^(-1)rho.                    (1)

This choice aligns the crossed-product labels used below.

## 4. Coherence of the C2 action

Choosing a regular left-module generator introduces an inner ambiguity.
The base-change statement above gives, at the tensor-functor level,

    F² = Inn(r^ell) composed with T^j.

The central lift of the original generator alpha_1 computes T² exactly.
For a central invertible p of C, its crossing with an A-module descends
with defect equal to its monodromy with the summands h of A. If that
defect is the character lambda(h), checking A-linearity on each h gives
a monoidal natural identification Inn(Q(p))=T_lambda (or its inverse,
depending on the left-module convention). Tensor compatibility is the
half-braiding axiom, so this is an identity of tensor functors.

For p=1, the monodromy is chi(1,h)², the order-two character of H. Thus

    T² = Inn(r).

For p=2 it is trivial. Hence r² has a central lift in D and
Inn(r²)=Id as a tensor functor.

Formula (1) makes F² fix every simple label. Conjugation by r^ell shifts
the noninvertible labels by 2ell, while T^j shifts them by j. Therefore
2ell+j=0 modulo four, so j is even and

    F² = Inn(r^(ell+j/2)) = Id.

The last exponent is even. Finally Aut_tensor(Id_D)=1, proved in
Section 1, makes the two coherence composites for F³ -> F agree.
Thus F supplies a genuine coherent C2 action. All equivalences and
separable-algebra operations can be chosen unitary.

## 5. The dihedral extension and its reflection dual

Form E=D semidirect_F C2. Write s for its odd invertible. Then

    r⁴=s²=1,  srs=r^(-1),
    rho r=r^(-1)rho,  rho s=rs rho,
    rho²=r²+(1+r+r²+r³)rho.

The eight invertibles form D8 and the other eight simples form a free
orbit of dimension t. The chosen crossed product has the regular
reflection algebra B=1+s. Its Morita dual K=Bimod_E(B) is unitary.

On the integral support there are two invertibles above each double
coset L and r²L, where L={1,s}, and one dimension-two simple X above
LrL. The stabilizers are C2 on the two size-two double cosets and
trivial on the size-four double coset. Cyclic stabilizers have no
nontrivial projective representation class. The irrational support has
two size-four double orbits, each with trivial stabilizer:

    U rho,  r²U rho,  U={1,s,rs,r^(-1)}.

Call their simples Y and Z; both have dimension 2t. Duality interchanges
these orbits because rho*=r²rho, so Y*=Z. The two integral invertibles
supported on L fix Y and Z, while the two supported on r²L interchange
them. Thus K has precisely the dimension type 1^4,2,(2t)^2.

## 6. The pointed associator forces C4, not V4

It remains essential to determine the group of the four invertibles in
K; it cannot be read from the D8 based ring alone.

In Izumi's crossed-product model for D, alpha_1^4=Ad lambda_4 and

    alpha_1(lambda_4)=chi(1,4)lambda_4=-i lambda_4.

The scalar in this cyclic kernel obstruction represents the restricted
associator in H³(C4,C*). It has order four. The integral reflection
dual is the group-theoretical category
K_int=C(D8,L,Omega,psi). Ng--Schauenburg Theorem 9.2 gives

    FSexp(C(G,L,omega,psi))=lcm_(g in G) |g| ord([omega]|_<g>).

The cyclic subgroup <r> therefore makes FSexp(K_int) divisible by
4*4=16. Its fusion rules are Tambara--
Yamagami on a group of order four: X is the unique noninvertible,
X*=X, every invertible fixes X, and X² is the sum of all invertibles.
Every TY(V4,chi,tau) has FS exponent four or eight, for either sign of
tau and either symmetric nondegenerate bicharacter (Liu--Ng,
Proposition 5.3). Thus the invertible group of K must be C4.

Write it as <g>, with h=g² the nontrivial invertible above L.
The two invertibles above r²L are g and g³. They interchange Y and Z,
while h fixes them. This rules out the V4 source R7_4_2603 for this
construction, without making a nonexistence claim about that source.

## 7. Complete tensor and source identification

The full tensor, in basis (1,g,h,g³,X,Y,Z), is determined by

    g⁴=1,  gX=X,  gY=Z,  gZ=Y,
    X²=1+g+h+g³,  XY=YX=XZ=ZX=Y+Z,
    Y²=Z²=g+g³+X+4Y+4Z,
    YZ=ZY=1+h+X+4Y+4Z.

These coefficients follow directly from free induction, rather than
from identifying dimensions alone. In E, Y=B rho B and
Z=B r²rho B are simple B-bimodules, and X=B r B. For any such induced
objects there is an actual bimodule isomorphism

    (B u B) tensor_B (B v B) = B u B v B.

Expanding the right side with the displayed E rules gives the mixed
products X Y=X Z=Y+Z and all four irrational products. For Y², its
integral underlying support is 2r²L plus LrL. Frobenius reciprocity
gives each of g,g³ once, and the remaining summand is X. Its
nonintegral underlying support contains every one of the eight
noninvertibles four times, giving 4Y+4Z. For YZ the integral support is
2L plus LrL, with 1 and h once each. The Z² and ZY products follow by
the same expansion. The pointed TY rules give all remaining products.

The standalone constructor `verify_R2665_inversion_model.py` takes no
census tensor as input to its model. It checks all 343 coefficients
against the pinned rank-seven source using

    model -> census: [0,1,6,2,5,3,4].

It also checks all fusion axioms in ranks seven and sixteen, all eight
free-induction identities just used, the neutral R8_1_12 identification,
and the exact order of the cyclic associator scalar. Its receipt binds
the tensors and compressed source files by SHA-256. The proof of the
categorical action and associators is Sections 1--6, not the finite
associativity check. Normal and optimized-Python runs give the same
certificate. A compatible model-catalog entry is supplied separately.

## Primary sources

1. Andrew Budinski, *Exotic Fusion Categories and Their Modular Data*,
   University of Alberta thesis (2021), Theorem 3.1.1, Table 3.1,
   Section 3.3.2. Public institutional copy:
   https://ualberta.scholaris.ca/bitstreams/3f73f320-a2a2-4184-ad81-d8708764f725/download
2. Masaki Izumi, *The classification of near-group categories*,
   arXiv:1512.04288v2, Theorems 11.3, 12.5, 13.4 and Corollary 13.5.
   The extension formula alpha_g(lambda_h)=chi(g,h)lambda_h occurs
   at the start of Section 12.1. Remark 12.4 also records self-duality
   of the orbifold subfactor.
   https://arxiv.org/abs/1512.04288
3. Pinhas Grossman, David Jordan and Noah Snyder, *Cyclic extensions of
   fusion categories via the Brauer--Picard groupoid*, arXiv:1211.6414v2,
   Lemma 4.7 and Remark 4.8.
   https://arxiv.org/abs/1211.6414
4. Gongxiang Liu and Siu-Hung Ng, *On total Frobenius--Schur indicators*,
   Contemporary Mathematics 623 (2014), 193--213,
   arXiv:1212.1435, Proposition 5.3.
   https://arxiv.org/abs/1212.1435
5. Siu-Hung Ng and Peter Schauenburg, *Frobenius--Schur indicators and
   exponents of spherical categories*, Advances in Mathematics 211
   (2007), 34--71, Theorem 9.2 (the group-theoretical exponent formula),
   arXiv:math/0601012v3.
   https://arxiv.org/abs/math/0601012

## Scope

This proves one new unitary realization, R7_4_2665. The four-case
dihedral reduction remains valid for R7_4_35, R7_4_2053,
R7_4_2603 and this now-realized case. It does not settle the other
three cases or R7_4_2591.
