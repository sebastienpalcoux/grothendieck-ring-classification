# Independent audit: subcategory projection and central twists

Status: theorem verified at the categorical level. This audit is independent of
any numerical search or target-specific certificate. It does not itself allocate
an exclusion.

Let D be a full fusion subcategory of a pivotal fusion category C, with the
inherited pivotal structure. Write P for the projection of an object to the sum
of its simple summands belonging to D. If Z=(V,c) is in Z(C), put W=P(V), and
choose its inclusion i:W→V and projection p:V→W. The complement of D is stable
under tensoring on either side by objects of D: if a simple Y outside D had a
D-constituent T in X⊗Y, with X in D, reciprocity would make Y a constituent of
X*⊗T in D, a contradiction. Hence c restricted against D preserves W and its
complement. The maps

    c_W,X = (id_X ⊗ p) c_V,X (i ⊗ id_X),  X in D,

are isomorphisms satisfying the half-braiding identity, so W belongs to Z(D).

The important point is that this operation also preserves the twist on each
summand; this is stronger than merely restricting a half-braiding. Use the
Drinfeld isomorphism in the convention

    u_V = (ev_V ⊗ id_V**) (c_V,V* ⊗ id_V**)
          (id_V ⊗ coev_V*): V → V**.

Postcompose with p** and precompose with i. The duality identity

    (id_V* ⊗ p**) coev_V* = (p* ⊗ id_W**) coev_W*

reduces the coevaluation to W. Naturality of c in its second variable then
moves p* through the crossing. Finally

    ev_V (p* ⊗ id_V) = ev_W (id_W* ⊗ p)

and the definition of c_W give `p** u_V i = u_W` (here `p**` denotes the
double-dual morphism, not multiplication). Also j_V i=i** j_W for the inherited
pivotal isomorphism j. In the convention theta=u^{-1}j this yields

    theta_W = p theta_V i.

In particular, if V is central simple and theta_V=lambda id_V, every simple
constituent of W in Z(D) has twist lambda. The same conclusion holds under the
opposite twist convention provided both centers use it consistently. Sphericality
is only needed to identify these balanced structures with the standard ribbon
structures used by the modular-data tables.

Thus if F_D denotes the known restriction matrix Z(D)→D, the D-part of a
restriction column of a central simple of C belongs to the additive monoid
of columns of F_D having its exact twist. A zero projection imposes no constraint.
This is a necessary criterion; it never constructs a central object or a category.

## Ising table

For the Ising fusion basis (1,g,sigma), choose an Ising ribbon twist theta_sigma=t
with t a primitive sixteenth root and theta_g=-1. The center is Ising × Ising^rev.
Its nine restriction columns, grouped by twist, are:

| Twist | Restriction columns |
|---|---|
| 1 | (1,0,0), (1,0,0), (1,1,0) |
| -1 | (0,1,0), (0,1,0) |
| t, -t, t^-1, -t^-1 | one (0,0,1) for each listed twist |

Therefore a nonzero projected vector (a,b,c) lies in one of the following
monoids: twist 1 has c=0 and a≥b; twist -1 has a=c=0; a primitive-sixteenth
Ising twist has a=b=0. All inherited Ising pivotal/braiding choices must be
included unless positivity fixes them. In particular, an arbitrary braided
subcategory is **not** assumed to extend its braiding to C.

## Fibonacci table

For basis (1,a), a²=1+a, the center has columns (1,0), (0,1), (0,1), (1,1),
with twists 1,t,t^-1,1 respectively, where t is a primitive fifth root determined
by the spherical Fibonacci category and the chosen braiding. The nonzero
projection (a0,a1) therefore satisfies either theta=1 and a0≥a1, or a0=0 and
theta in {t,t^-1}. Include all appropriate Galois choices when applying this to
a general spherical category.

## Half-E6 completeness and positive-dimensional branches

Primary sources consulted:

* Hagge–Hong, *Some non-braided fusion categories of rank 3*,
  https://arxiv.org/pdf/0704.0208 (v2), Theorem 1 and §§4.7–4.8.
* Hong–Rowell–Wang, *On exotic modular tensor categories*,
  https://arxiv.org/pdf/0710.5761, §2.1, especially the ten central objects and T.

For x²=1+g+2x, gx=x, g²=1, Hagge–Hong classify exactly four monoidal categories,
all obtained from one another by Gal(Q(sqrt(3),i)/Q). Pivotal structures on a
fixed one are unique: a tensor automorphism eta of Id satisfies eta_x²=eta_x
because x occurs in x², hence eta_x=1; the occurrence of g then gives eta_g=1.
The source choice has dimensions (1,1,1+sqrt(3)). Two conjugates send sqrt(3)
to -sqrt(3) and have the unique dimension 1-sqrt(3)<0, so are not pseudo-unitary.
The two positive-dimensional choices are exactly the source and its complex
conjugate. This closes the potential gap between uniqueness among *unitary*
categories stated in HRW and the *pseudo-unitary* scope needed here.

For source order (1,Y,X1,X2,X3,X4,X5,U,V,W), the restrictions are
1,g,x,x,x,x,x,1+x,g+x,1+g+x. The twist exponents modulo 12 are
0,6,-3,5,5,2,-4,0,6,0. The second positive-dimensional choice negates all exponents.
No other positive-dimensional half-E6 branch is omitted.

## Twist-resolved masses

The corollary in `papers/chapters/round4_projection.tex` was independently
checked. For X in D, the pivotal rotations defining each positive-degree
indicator are identical in D and C. Projection confines all central twists
contributing to I_C(X) to those of Z(D). Apply the central indicator formula
for degrees 1,...,N-1 and the induction dimension identity for degree zero,
where N is any common multiple of the orders of the twists of Z(D). Fourier
inversion gives the mass identity in the chapter, including its factor
dim(C)/dim(D). This argument does not assume that projection is a tensor
functor or that it maps central induction to central induction.

The Fibonacci masses at the two nontrivial twists are each
dim(C)*phi/(phi+2); the twist-one a-mass is dim(C)*phi²/(phi+2).
The Ising g-masses at 1 and -1 are dim(C)/2 each; the sigma-mass at each
of its four twists is dim(C)*sqrt(2)/4. These constants agree directly with
the center restriction tables above.

## Cyclic order-three pointed subcategory

Write the standard cyclic cocycle as

    omega_s(a,b,c) = exp(2*pi*i*s*a*floor((b+c)/3)/3),  s=0,1,2.

The scalar projective characters of the centralizer of flux a give twists

    theta(a,b) = exp(2*pi*i*(s*a²/9+a*b/3)),  b=0,1,2.

This also follows by solving the scalar half-braiding hexagon for this
cocycle. Cubing gives theta(a,b)^3=zeta_3^(s*a²). Consequently both nonzero
fluxes a=1,2 have the same cube zeta_3^s. The canonical pseudo-unitary
pivotal structure gives dimension one to all invertibles, so no additional
pivotal sign enters this formula. Reversing the cocycle/twist convention
interchanges s=1 and s=2 and leaves the exhaustive list unchanged.

Over Q(zeta_24), the three s=0 twists remain the three exact cube roots of
unity. For s=1 or 2, the three roots of theta³=zeta_3^s have normalized
relative first, second and third moments (0,0,zeta_3^s). This justifies the
three-plus-one-plus-one phase support in the C3 projection branch, with
all three cocycle classes retained.

## Source and chapter audit scope

The projection theorem, its Fourier corollary and all constants in
`papers/chapters/round4_projection.tex` were checked independently after
the dual-map notation was corrected to p*. These are necessary conditions;
their applicability to all categorifications still uses the separate,
case-specific general-to-pseudo-unitary reduction.
