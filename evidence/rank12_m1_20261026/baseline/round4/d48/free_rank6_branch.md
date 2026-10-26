# The free rank-six quotient branch

Let C be an integral complex fusion category of dimension48 with one of
the twenty frozen source rings. Suppose the central Rep(C2) supplied by
solvability acts freely on its simple objects. Then C=E^C2, where E has
simple dimensions (1,1,1,1,2,4), and the outer C2 action fixes every simple
of E. The frozen source tensor determines E's entire based ring by
identifying each pair {X,bX}; this is verified in quotient_reconstruct.py.
If X,Y have dimensions2,4, respectively, the resulting equation is

    Y Y* = Y² = sum(g in G(E)) g + 2X + 2Y.

Thus E_ad=E and U(E)=1. Since FPdim(E)=24=2³·3, the ENO solvability
theorem applies to arbitrary complex categories. The last nontrivial
step in a solvable construction cannot be an extension, since U(E)=1;
it is an equivariantization by a prime cyclic group. Its representation
ring embeds into G(E), of order4, so the prime is2. Write E=T^C2 with
FPdim(T)=12.

The simple-orbit formula for equivariantization determines the type of
T without any classification assumption. Each fixed simple of T gives
two simples of equal dimension in E, because H²(C2,C*)=0. Each free
orbit gives one simple of twice the original dimension. E has just one
simple in each of dimensions2 and4, so neither can come from a fixed
simple. The four invertibles of E come from two fixed invertibles of T;
its dimension2 simple comes from an orbit of two additional invertibles,
and its dimension4 simple from an orbit of two dimension2 simples.
Consequently T has type (1^4,2²), and its actual order-two tensor action
swaps its two noninvertible simples.

The finite ring lemma in rank6_swap_rings.py exhausts all rings of this
type admitting such a swap. For G=C4 and V4, it enumerates every left
and right action on the two noninvertibles and every possible duality.
Frobenius reciprocity fixes the invertible product coefficients; the
remaining dimension budget gives only100 and456 candidate tables.
After full associativity and reciprocity, exactly one swappable table
per G remains: the Jordan–Larson ring R(3,G). Their Theorem1.4 excludes
G=C4 categorically, leaving R(3,V4). This finite lemma was independently
replayed and audited in ../audit_exclusions/audit_d48_followup.md.

Let h be the canonical order-two object of Rep(C2) inside E. Its central
lift is unique: the kernel of Inv(Z(E))->Inv(E) is Aut_tensor(Id_E),
which is Hom(U(E),C*)=1. The outer action on E fixes its basis, and
therefore fixes h and its unique central lift. Thus it preserves this
central Tannakian Rep(C2). Equivariantizing it gives a central Tannakian
Rep(P) inside C, with |P|=4. Iterated de-equivariantization identifies
C with T^P; this allows both P=C4 and P=V4 and all categorical action
coherences.

The two audited triality lemmas now apply. If T is group-theoretical,
triality_gt_branch.md proves that every 2-group equivariantization is
group-theoretical, using the three Lagrangians in its center. If T is
non-group-theoretical, triality_soft_automorphisms.md proves that every
order-four equivariantization has a fusion coefficient2. The latter
contradicts the multiplicity-one source tensor. Therefore C is
group-theoretical in this entire free rank-six branch.

No closure of arbitrary group-theoretical categories under arbitrary
equivariantizations is assumed. The specific triality lemmas supply the
necessary additional premise.
