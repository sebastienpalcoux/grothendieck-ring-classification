# A forced group-theoretical result for R12_1_513

This is a general-complex categorical reduction, with no unitarity assumption.
It is not itself an exclusion; a separate complete group-theoretical search
can be applied after this theorem.

## Ring and neutral associator

The frozen full tensor and `verify_R513_GT.py` establish that the adjoint
subcategory of any categorification is pointed with group G=C4 x C2. The
category has a faithful C3 grading, with two dimension-two simples in each
nontrivial grade. For a noninvertible X, its left and right stabilizers are
the two distinct cyclic subgroups of order four. Choose coordinates
G=<a> x <b>, with these subgroups <a> and <ab>.

Write the neutral category as Vec_G^omega. The isomorphisms hX -> X for a
left stabilizer provide an actual two-cochain trivializing omega on that
stabilizer, by the module associativity pentagon. The right stabilizer gives
the same conclusion (with inverse associator, which does not change
triviality). Thus omega restricts trivially to both <a> and <ab>.

The integral cohomology Kunneth calculation is

    H^3(G,C*) = H^4(BG,Z)
               = C4{x^2} + C2{y^2} + C2{xy},

where x,y are the degree-two first Chern classes of the coordinate
characters of orders four and two. On <a>, x maps to the cyclic generator t
and y maps to zero. On <ab>, x maps to t and y maps to 2t. Consequently the
first restriction makes the x^2 coefficient zero, and the second makes the
xy coefficient zero: x y maps to 2t^2 whereas y^2 maps to 4t^2=0. Only the
zero class and the nonzero class y^2 remain. The latter is inflated from the
second C2 factor. The exact replay also constructs sixteen normalized
fourth-root cocycles, checks their full cocycle equations, distinguishes all
sixteen by cyclic cycle evaluations, and recovers these same two classes.

## Lagrangian counts for the two possibilities

Use the normal-abelian-subgroup and invariant alternating omega-bicharacter
classification of Lagrangian subcategories of Z(Vec_G^omega)
(Naidu--Nikshych, Theorem 4.12, https://arxiv.org/pdf/0705.0665).

For omega=1, G is abelian and there are no twisting corrections. Every
subgroup contributes |H^2(H,C*)| Lagrangians. The subgroup list consists of
the trivial group, three cyclic groups of order two, two cyclic groups of
order four, one V4, and G itself. Their contributions are respectively

    1 + 3 + 2 + 2 + 2 = 10.

For omega the inflation of y^2, a subgroup has trivial restriction precisely
when it is one of

    1, <a^2>, <a>, <ab>.

Indeed the two other involutions have nonzero y coordinate and already
detect the nontrivial restriction. V4 and G contain such involutions. The
two cyclic-four subgroups have trivial restriction by the preceding
calculation. Each admissible subgroup is cyclic, so its H^2 is zero. The
space of alternating omega-bicharacters is therefore a singleton. It is
automatically G-invariant: conjugation acts on this space, and G preserves
the subgroup. Thus these four subgroups contribute exactly four Lagrangians.
The subgroup lattice and both counts are independently replayed in the
certificate script.

## Extension conclusion

The homomorphism C3 -> BrPic(Vec_G^omega) associated with the faithful
extension acts on these Lagrangian subcategories. A C3 action on a finite
set whose cardinality is not divisible by three has a fixed point. Both
10 and 4 are congruent to one modulo three. The center therefore contains
a C3-stable Lagrangian.

The group-theoretical extension criterion now applies: a group extension of
a fusion category is group-theoretical exactly when the center of its
neutral category has a stable Lagrangian subcategory (Gelaki--Naidu--Nikshych,
*Centers of graded fusion categories*, Corollary 3.10,
https://msp.org/ant/2009/3-8/ant-v3-n8-p05-s.pdf).
Hence every complex categorification of R12_1_513 is group-theoretical.

No claim that all integral dimension-24 categories are group-theoretical is
used. The decisive input is the pair of distinct cyclic-four stabilizers.
