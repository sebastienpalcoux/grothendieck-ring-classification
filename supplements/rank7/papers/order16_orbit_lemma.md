# A theoretical order16 orbit obstruction

**Lemma.** Let S3 act by automorphisms on a group H of order16. If the normal C3 acts without fixed points outside the identity, then no S3-orbit decomposition can have sizes (1,3,6,6).

First H is abelian. Its center is characteristic, and its cardinality is congruent to1 modulo3 because only the identity is fixed by C3. A nontrivial finite 2-group has nontrivial center, so |Z(H)| is4 or16. If it is4 and H is nonabelian, H/Z(H) cannot be cyclic, so it is V4. The commutator is then an alternating, C3-equivariant bilinear map

    ∧² V4 → Z(H).

The exterior square is C2 and has trivial C3 action, whereas Z(H) has no nonidentity C3-fixed element. The map must vanish. This makes H abelian, a contradiction to |Z(H)|=4.

The abelian groups of order16 are C16, C8×C2, C4×C4, C4×C2×C2, and C2^4. Every characteristic subgroup must have cardinality1 modulo3. The subgroup 2H eliminates C16 (order8) and C4×C2×C2 (order2); the subgroup 4H eliminates C8×C2 (order2). Therefore H is C4×C4 or C2^4.

A transposition in S3 would fix exactly two elements in an orbit decomposition (1,3,6,6): the identity, and one element of the unique orbit of length3. It fixes no element of a free orbit of length6. We show that any involution on either possible H fixes at least four elements.

For H=C2^4, an involution S satisfies (S−I)²=0 over F2. Its image lies in its kernel, so the kernel has dimension at least2, giving at least four fixed points.

For H=C4×C4, view S as a matrix over Z/4. If its reduction modulo2 is the identity, it fixes every element of 2H, a subgroup of order4. Otherwise its reduction is the unique nonidentity unipotent conjugacy class in GL2(F2). Lift a basis in which that reduction is [[1,1],[0,1]]. Then

    S = [[a,b],[c,d]],  a,b,d odd, c even.

The upper-right equation in S²=I gives b(a+d)=0. Since b is a unit, d=−a. The upper-left equation gives a²+bc=1; since every odd square is1 modulo4, this forces c=0. For each of the four choices of x, the first fixed-vector equation

    (a−1)x+b y=0

has one solution y. The second equation follows automatically from a²=1. Thus there are exactly four fixed vectors. In all cases there are at least four, contradicting the required two. This proves the lemma without enumerating automorphisms or computing associators.

## Exact corroboration

`verify_orbits.py` independently enumerates all96 automorphisms of C4², all8 fixed-point-free order-three elements, and their48 compatible reversing involutions. All give orbit sizes (1,3,3,3,6). For C2^4 it checks all65536 matrices for involutive reversers of a representative fixed-point-free C3 action, finding30, with the same orbit sizes. Every fixed-point-free C3 action on F2^4 is conjugate to this representative: its minimal polynomial divides x²+x+1, making it a two-dimensional F4 vector space.

The verifier also checks all28 involutions (including the identity) on C4²: eighteen have four fixed points, nine have eight, and one has sixteen. No enumeration is needed for the theoretical proof.

This lemma supplies the final contradiction in the general exclusions of R7_2_252 and R7_2_315 once their forced equivariantization chain has been established. The source tensor certificate and categorical reduction are supplied in the accompanying rank-seven package.
