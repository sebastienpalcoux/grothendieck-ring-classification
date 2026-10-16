# R9 has trivial pointed associator: removal of the class-two branch

**Current status: generally excluded.** The final theorem is `R9_CENTER_TRACE_PROOF.md`, verified by `verify_r9_center_trace.py`. The text below records an intermediate necessary reduction; its former remaining class-zero alternative is now excluded by the cyclic induction Fourier bound. Historical scoped receipts remain valid.


**Proposition.** Every complex categorification of R8_1_9 has trivial associator class on its pointed C4 subcategory. In particular the class-two self-Morita alternative in `R9_MORITA_FRONTIER.md` is impossible. At this intermediate stage the class-zero alternative remained; the final general exclusion is proved in the superseding note above.

## Categorical reduction and pointed indicators

The ring has exactly two FP dimensions, 1 and d=2+sqrt(5), so Schopieray's two-dimension Galois pseudo-unitarity theorem applies. We use the canonical positive spherical structure of a pseudo-unitary Galois conjugate. In source order the pointed labels are 0,1,2,7, with generator a=1, a^2=7, a^3=2. The nonpointed labels are3,4,5,6, with duality3*=4 and5*=5,6*=6. Odd multiplicities in the cubes of5 and6 force

    nu2=(1,0,0,0,0,1,1,1).

The pointed associator is a class k in H^3(C4,C^*)=Z/4. The canonical spherical indicators of Vec_(C4)^omega_k give

    nu2(a^2)=(-1)^k,  nu4(a)=nu4(a^-1)=exp(2 pi i k/4).

These follow directly by multiplying the standard cyclic cocycle in the pivotal rotation formula. The first identity and nu2(a^2)=1 leave k=0 or2. Suppose k=2. Then nu4(a)=nu4(a^-1)=-1.

For any invertible x of ordern, the induction trace formula gives

    Tr(theta^n I(x))=D nu_n(x),  dim I(x)=D.

Equality in the triangle inequality with positive central dimensions forces every constituent Z of I(x) to have theta_Z^n=nu_n(x). Thus every constituent occurring over source1 or2 has theta^4=-1, and every constituent over7 has theta^2=1. Relative to K=Q(sqrt(5)), a primitive eighth root and its square both have normalized trace zero. The possible first/second pairs on source7 are (1,1),(-1,1).

## Complete character labels and Galois pairing

The global dimension is D=8+16d=40+16sqrt(5), with norm320. The complete ordinary codegrees are D,D',8,8,8,8,8,8. Order the basis as

    (1,a,a^2,a^3,rho,a rho,a^2 rho,a^3 rho)
       -> source (0,1,7,2,5,3,6,4).

The six remaining characters have a=-1,i,-i, each with rho=+1 or-1. Their other values are multiplicative. They are defined over Q(i), which is disjoint from K.

For a center simple let v be its nonnegative integral forgetful row, and put

    a(v)=v0+v1+v2+v7,  b(v)=v3+v4+v5+v6,
    dim(Z)=a(v)+b(v)d.

Choose a cyclotomic automorphism sigma flipping K and fixing Q(i). The actual character-labelled correspondence of Ostrik, Example2.9 and Theorem2.13, together with modular Galois symmetry, gives

    T(v)=v+(0,0,0,1,1,1,1,0)*(a(v)-b(v)/2).

An actual row has partner T(v) or -T(v), with the sign making it nonnegative. Its entries are integral, so b(v) is even. Different partner row types have equal multiplicities.

The normalized relative moments of partner rows agree, even though their actual twists need not agree. Indeed theta_(pi_sigma Z)=sigma^2(theta_Z). Since K is quadratic, sigma^2 fixes K, and normalized relative trace from a common cyclotomic field is invariant under sigma^2. This works for arbitrary root orders and requires no conductor saturation.

## Eight exhaustive low frames

The canonical central unit has forgetful row e0, and its Galois image has row

    (1,0,0,1,1,1,1,0).

Each of the other six constituents of I(1) has dimension D/8=1+2d and restriction1 plus two nonpointed objects. Their sum is fixed by

    F I(1)=(8,0,0,4,4,4,4,0).

In the ordered four nonpointed coordinates, each profile is a nonnegative integer vector of sum2. Duality sends (u0,u1,u2,u3) to (u0,u3,u2,u1). The two real characters have self-dual profiles; the i and-i rows pair by this involution. There are1600 such assignments. The aggregate multiplicities leave76; actual character-labelled S-symmetry leaves8; all8 have nonnegative positive semidefinite residual Gram matrix. These counts are reconstructed exactly by the verifier, with no saved profile list trusted.

Here S-symmetry is chi_i(v_j)=chi_j(v_i), since all six codegrees are8. The character labels are canonical, not freely interchangeable because the codegrees repeat.

## A universal moment domain and finite integer inequality

The complete arbitrary-root domain is the17-vertex hull in `Q5_ALL_ROOT_TWO_MOMENT_HULL.md`. In brief, put u_+=(-1+sqrt(5))/4 and u_-=(-1-sqrt(5))/4. The nine base pairs are

    (1,1),(-1,1),(0,-1),
    (u_+,u_-),(u_-,u_+),(-u_+,u_-),(-u_-,u_+),
    (0,-u_+),(0,-u_-).

Add the negative halves of the first two and the six irrational pairs. The negative half of(0,-1) and zero already lie in the rational triangle. For arbitrary root order2^a5^b m with gcd(m,10)=1, the extra odd factor scales both moments by mu(m)/phi(m), a number in[-1/2,1]. Higher shared prime powers give zero. Thus the hull is valid without a prime-support or root-order assumption. Its coordinates in the basis1,d have denominators dividing8.

For each of the eight low frames let R be the residual induction Gram matrix. Every high row has v0=0, entries between0 and floor(sqrt(R_ii)), and a dimension z=a+bd such that D/z is an algebraic integer. The latter follows from the modular formal-codegree identity (D/z)^2 integral and transitivity of integrality. Writing

    n=a^2+4ab-b^2,
    D/z=x+yd,
    x=(8a+16b)/n,  y=(16a-8b)/n,

the exact condition is that both 2x+4y and x^2+4xy-y^2 are integers. This is the trace/norm criterion for integrality in the quadratic ring of integers.

Impose the integral Galois partner and the entrywise and positive semidefinite bound

    R-sum_(partner orbit) vv^t >=0.

Each frame has exactly92 allowed partner row orbits. Use the universal17-vertex moment hull, except that source1 or2 support requires the single pair(0,0) and source7 support requires the two pairs(1,1),(-1,1). This gives389 moment columns per frame.

Each column consists of28 upper-triangular Gram entries,14 coefficient entries of8 sum v_i z t(theta), and14 entries of8 sum v_i z t(theta^2), with i=1,...,7. The target is the residual Gram matrix together with the two induction identities

    Tr(theta I(X_i))=0,
    Tr(theta^2 I(X_i))=D nu2(X_i),

after subtracting the known twist-one I(1) constituents. Every actual center supplies a nonnegative real combination of the reconstructed columns equal to this target.

The SINGLE integer covector in `r9_pointed_class2_certificate.json` satisfies

    y.column >=0 for every column in every frame,
    y.target=-6432 for all eight frames.

The minimum column pairing is0. This excludes every possible center under k=2. The verifier reconstructs all bounded domains and all positive semidefinite conditions in exact rational arithmetic. No numerical pruning, optimizer, or assumed integer Gram factorization enters the proof.

Thus k=0 is necessary. Returning along Galois conjugation preserves the zero class; class2 is also fixed by every cyclotomic Galois automorphism, so it cannot be hidden by the initial reduction. The prior Morita frontier consequently retains only the class-zero branch, with pointed dual V4 and the prospective R477 dual having one negative pointed indicator and three positive/one negative nonpointed indicators. That branch is not resolved here.

## Reproduction and scope

    python verify_r9_pointed_class2.py --repo PATH_TO_REPOSITORY

The immutable source hash is `1718ab13b6969ed751b621f7303b9e2bb29bb8280f692315499b130a420538f6`. The proof uses the already audited Galois forgetful-row and relative-moment lemma, the spherical induction trace formulas of Ostrik and Ng–Schauenburg, the pivotal odd-isotypic lemma, and the explicit arbitrary-root hull. Its output is a scoped necessary restriction only and does not change the classification count.
