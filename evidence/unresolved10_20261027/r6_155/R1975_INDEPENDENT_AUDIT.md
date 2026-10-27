# Independent audit: the rotation branch of R9_2_1975 is impossible

Date: 2026-10-27.

**Accepted**, conditional on the previously archived general-complex,
Tambara--Yamagami and Morita-completion reductions cited in the developing
agent's report. The new argument is categorical and uses only tiny exact
cochain evaluations. It does not assume unitarity, a faithful Z2 grading,
or existence from modular data.

The reflection duality shift was excluded by the independently audited
commutator invariant. The present argument excludes the remaining rotation
shift. Together they exclude the source R9_2_1975, subject to the archived
reduction's stated exhaustive scope.

## 1. The surviving ring and its scalar spectrum

Write G=D8, H=<z>=Z(G), Q=G/H=V4. The ring has eight invertibles g and four
large simples X_q, with

    g X_q = X_q g = X_{q+gH},
    X_p X_q = sum_{gH=p+q+alpha} g + 2 sum_t X_t,
    X_q^* = X_{q+alpha}.

Here alpha is the coset of an order-four rotation. Put
d=4+3 sqrt(2), d'=4-3 sqrt(2), D=8+4d^2=144+96 sqrt(2), and D'=sigma(D).

All irreducible representations of the complexified based algebra are as
follows. A scalar representation restricts on G to a character t of Q and
has X_q=t(q)x. For t=1, the equation x^2=2+8x gives x=d,d'. For each of the
three nontrivial t, the equation is x^2=2t(alpha), giving two scalar
representations. Their formal codegrees are respectively

    D, D', 16,16,16,16,16,16.

Indeed, for t nontrivial the contribution of the invertibles is 8 and that
of the large objects is 4t(alpha)x^2=8. There is also the usual degree-two
irreducible representation of D8, extended by X_q=0: z acts as -I, whereas
zX_q=X_q forces the latter assignment. Its formal codegree is |G|/2=4.
These are all representations, since 8*1^2+1*2^2=12, the ring rank.

The element

    v = 1 + sum_q X_q

is central. It acts by 1+4d=D/D' on the FP representation, by
1+4d'=D'/D on its conjugate, and by 1 on each other simple block. Thus its
scalar action on every irreducible E is f_E/sigma(f_E).

## 2. The distinguished central object really has restriction v

This step is valid for noncommutative source rings. In a hypothetical
pseudo-unitary categorification C, let A_E be the distinguished simple of
Z(C) associated with an irreducible E of K_0(C), and let lambda_E denote
the scalar by which a central ring element acts on E. Ostrik's central
character construction and Theorem 2.13 give

    dim(A_E)=D/f_E,
    S_{A_E,Z}=dim(A_E) lambda_E(F(Z)).

Here S is unnormalized; lambda_E is chi_E/dim(E), not the unnormalized
character trace. This removes the potential factor-of-two error in the
degree-two block.

Take B=A_{sigma(FP)}. Since sigma(FP) is a one-dimensional representation,
dim(B)=D/D'. Symmetry of S implies

    (D/f_E) lambda_E(F(B))
      = (D/D') sigma(dim(A_E))
      = D/sigma(f_E).

Consequently lambda_E(F(B))=f_E/sigma(f_E) for every E. Both F(B) and v
are central, and a semisimple algebra's central elements are determined by
their scalars on all simple blocks. Therefore

    F(B) = 1 + X_00 + X_10 + X_01 + X_11.             (1)

This is stronger than its dimension alone. The dimension 1+4d would not
exclude multiplicities 2,2,0,0; the complete central-character calculation
is essential. No claim that modular data alone constructs B is made:
B is supplied by induction of the unit in an assumed category.

Primary sources freshly checked:

- V. Ostrik, *Pivotal fusion categories of rank 3*, arXiv:1309.4822,
  Section 2.3 immediately before Theorem 2.13 and Theorem 2.13 itself.
  https://arxiv.org/pdf/1309.4822
- T. Deshpande, *On centers of bimodule categories and
  induction-restriction functors*, arXiv:1611.04486, Section 2.7,
  Corollary 2.18 and Section 4.3. https://arxiv.org/pdf/1611.04486

## 3. Rigidity fixes the relevant stabilizer commutator

Use the coordinates and cochains of the companion
`r9_noncommutative/verify_duality_obstruction.py`. Thus

    P=(1,0,0,0), S=(0,0,1,0), Z=(1,1,0,0), E=(0,0,0,1)

in L=D8 x C2, with Z=[P,S]=(PS)^2. The coordinates of G are the first
three entries. The specified base stabilizer cochain is beta_0. Every
other allowed stabilizer cochain is beta=beta_0 gamma, where gamma is an
arbitrary C*-valued ordinary two-cocycle on L.

For a rotation lift r, the duality-equivalence obstruction is

    c_r = phi_r^*(beta) * kappa_r * T^*(beta),

in multiplicative notation. Rigidity requires it to be a coboundary.
The same direct evaluation for both rotation lifts gives

    C_{c_r(beta_0)}(P,E)=1,
    C_{beta_0}(P,Z)=-1,                              (2)

where C_eta(a,b)=eta(a,b)/eta(b,a) for commuting a,b. Independently
replaying the developing script's definitions yielded exponents 0 and 2
modulo 4 respectively, for r=(0,1,1) and r=(1,0,1).

The change of the first commutator under beta_0 -> beta_0 gamma is exactly
C_gamma(P,Z). Here is the all-complex proof. The normalizer sends
P to P(ZE)^a and E to E for a in {0,1}; swapping the two projections
fixes P and sends E to ZE. Since E is central, C_gamma(-,E) is a character
which kills Z=[P,S]. Since P^2=1, its value on P has square one. Thus

    C_gamma(phi_r P,phi_r E) C_gamma(TP,TE)
      = C_gamma(P,E)^2 C_gamma(P,Z)
      = C_gamma(P,Z).

A coboundary has commuting-pair commutator 1. Hence (2) and rigidity force
C_gamma(P,Z)=1. It follows that every actual allowed beta has

    C_beta(P,Z)=-1.                                  (3)

This is not a finite-root search over gamma. The argument works for every
complex two-cocycle, including all coboundary modifications.

## 4. Why (3) contradicts (1), including the normalization check

Let p=(1,0,0), z=(1,1,0) in G and K=<p,z>=V4. Both elements have n=0 in
the pointed cocycle displayed in the companion report. That cocycle is
identically 1 on K^3. Thus the restriction of the pointed category to K
is Vec_K in the displayed gauge, and its regular bimodule has diagonal
stabilizer cochain 1. No hidden inverse-dual tensorator or nontrivial
pointed associator on K can cancel (3).

Equivalently, any remaining change of trivialization is a coboundary and
has trivial commutator on p,z. This restriction to the strict even V4
avoids needing a stronger assertion about the entire D8 diagonal
normalization.

For an object of the relative center with respect to Vec_K, the X_00
isotypic multiplicity space carries a projective diagonal K-action with
multiplier beta|_{diag K}, or its inverse depending on orientation.
Equation (3) says that the operators representing p and z anticommute.
They are invertible, so this multiplicity must be even: taking determinants
in AB=-BA yields (-1)^m=1. In particular it cannot be one.

For clarity, a central object with restriction (1) actually gives a relative
halfbraiding on each individual X_q. The halfbraiding with g maps
g tensor X_q to X_q tensor g; both are X_{q+gH}, and no other X_r has
that source/target label. The multiplicity-one isotypic components are
therefore preserved, and the halfbraiding coherence restricts to them.
Its X_00 component would supply a one-dimensional projective K-action,
contradicting (3).

## 5. Scope of acceptance

The new rotation obstruction is accepted independently. Combined with the
separate reflection-shift obstruction, no listed D8 Morita completion of
R9_2_1975 remains. To conclude a general complex exclusion, retain the
archived dependencies establishing the original spherical/Galois-positive
gate, the exhaustive TY possibilities, and the exhaustive Morita-completion
list. Those dependencies must remain explicit in the final manuscript.

The argument uses only pointed-module rigidity and an obligatory central
object; it never treats the noninvertible component as a faithful graded
component. No claim is made here about the still-surviving zero-shift
branches of the three commutative rank-nine source rings.
