# Independent structural audit of the R516 exclusion

**Accepted.** The argument in `../quadratic_s_symmetry/R516_STRUCTURAL.md`
is valid and supplies a theoretical exclusion independent of the large LP
certificate. The exact character data were already independently checked in
`replay516.py`. The new categorical descent steps were checked as follows.

The low dimension spectrum has precisely one 1 and one 2, all others exceeding
4. The simple A of dimension 2 restricts to 1+g and is selfdual by uniqueness.
In A² the unit multiplicity is one, and the restriction has source-unit
multiplicity two. Since the ring is commutative, all distinguished I(1)
multiplicities are one, so exactly one other distinguished summand occurs.
The dimension bound makes it A. The leftover is an invertible z with F(z)=g.
Both zA=A and z²=1 follow from their restrictions and uniqueness of the low
objects of dimensions 2 and 1. The verified character of A has χ_A(g)=1.
The character/S formula and balancing therefore give θ_z=1. Balancing on the
closed subcategory {1,z,A} makes its double braiding trivial. Positive
categorical dimensions identify the symmetric category as Tannakian Rep(S3),
rather than a super-Tannakian alternative with negative canonical dimensions.

The regular algebra B=1+z is connected, separable and commutative in the
center, and its image 1+g is connected in C. Hence right modules E form a
fusion category. Its positive spherical structure can be described by the
normalized module trace: tr_E(T)=tr_C(T)/dim_C(B)=tr_C(T)/2 on an A-linear
endomorphism. The regular Tannakian algebra is symmetric Frobenius and has
trivial twist, so the pivotal dualities descend and this trace is spherical
and compatible with the relative tensor product. All nonzero module
identities have positive dimension. Consequently this structure is the
pseudo-unitary one; no unitarity of the original category is assumed.

The free orbits and fixed points of g give the listed nine module dimensions.
For a fixed simple, the obstruction to its module action is a scalar, which
has two square-root choices over C; hence there are two simple modules with
the same underlying simple, each with half its source dimension. Free pairs
have one simple module, with the dimension of either constituent. This proves
1³,d³,e³ without a presumed action on unknown fusion channels.

The use of the center descent is precise. Since Rep(S3) is symmetric, all its
B-modules are local. Their full subcategory is Rep(C3), the usual restriction
to the kernel of S3→C2. DMNO Theorem 3.20 identifies the entire local-module
category Z(C)^0_B with Z(E), and the forgetful square agrees with ordinary
forgetting of modules. Under this equivalence A⊗B is the sum of the two
nontrivial central invertibles. Its underlying E object is the free module on
F(A)=1+g, namely two copies of the unit. Therefore each summand separately
forgets to the unit. They remain distinct central objects because the center
equivalence is fully faithful.

For completeness, a central structure on the unit is a tensor automorphism
of Id_E. The three distinct central invertibles thus give a faithful C3 of
such automorphisms. Their eigencharacters on simples define a faithful dual
C3 grading. This is exactly ENO Proposition 5.10, and Proposition 8.20 gives
equal component dimensions. Equating rational and sqrt(3) coefficients leaves
only (a,b,c)=(0,3,0) or (1,1,1); the neutral component contains the unit and
therefore has dimensions 1,d,e. Its inherited positive spherical structure
permits the final twist argument.

I independently derived the rank-three multiplication and the final
contradiction: X²=1+X+Y, XY=X+2Y, Y²=1+2X+2Y. The three low restriction
columns are (1,0,0),(1,1,1),(1,2,2), with respective dimensions
1,4+2sqrt(3),7+4sqrt(3). Their twist-one mass in I(X) is M=18+10sqrt(3).
The total dimension is 30+18sqrt(3). Since ν1(X)=0 and every other twist has
modulus one, one needs 2M≤30+18sqrt(3), whereas the difference is
6+2sqrt(3)>0. This final step needs no classification theorem or computation
with a large center.

Primary references were opened and checked afresh:
- https://arxiv.org/pdf/1009.2117 , Theorem 3.20 and its forgetful construction.
- https://arxiv.org/pdf/math/0203060 , Propositions 5.10 and 8.20.
- https://arxiv.org/pdf/1611.04486 , Proposition 2.8 and Section 2.7 for the
  central-character normalization, checked in the preceding independent audit.

The signed Galois-to-pseudo-unitarity gate then gives general complex scope.
No gap or additional hypothesis was found in this structural proof.
