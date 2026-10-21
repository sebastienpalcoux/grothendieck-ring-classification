# Dimension84 adjoint rigidity

**Theorem (general complex scope).** No fusion category has FP dimension type
`1^4,2^2,6^2` and full adjoint subcategory. The source witnesses apply this to
R8_3_76, R8_3_735, R8_3_738, R8_3_1422 and R8_3_1805.

This is a new application and unification of the cited structural theorems,
not a new classification theorem for all dimension84 categories.

Dong, *Weakly integral fusion categories of low dimensions*, arXiv:2103.04553,
Theorem1.2 says dimension84 categories are solvable or group-theoretical.
Every group of order84 is solvable: its Sylow7 subgroup is normal (the number
of Sylow7 subgroups divides12 and is1 modulo7), and its quotient has order12.
Solvability is Morita invariant. Thus either alternative is solvable.
By ENO, *Weakly group-theoretical and solvable fusion categories*,
arXiv:0809.3031, Definition1.2 and Proposition4.4, its last construction step
is extension or equivariantization by a prime cyclic group. Full adjoint
excludes a nontrivial extension. For an equivariantization the canonical
Rep(C_p) subgroup injects into the four invertibles, so p=2. Write C=D^{C2}.
The orbit formula for FP dimensions makes every base dimension rational,
hence integral. The base D has dimension42. **Integral** pqr categories are
group-theoretical by ENO Theorem9.2; integrality here is essential.

Exactly two base invertibles must be fixed by the C2 action. A fixed
invertible contributes two invertibles after equivariantization, whereas a
free orbit contributes one dimension2 simple. For the sign object g in C,
let n2,n6 be its numbers of fixed dimension2,6 simples. Each lies in{0,2},
and the base type is
`1^(2+2*n2),2^((2-n2)/2),3^(2*n6),6^((2-n6)/2)`.
The four possibilities are `[1,1,2,6]`, `[1^6,6]`, `[1,1,2,3^4]` and
`[1^6,3^4]`.

All groups of order42 have normal Sylow7 subgroup. Their complements have
order6, so they are C7 semidirect C6 with action image order1,2,3,6, or C7
semidirect S3 with action image order1,2. The exact script
`dimension42_group_types.py` constructs all six multiplication tables,
checks associativity, exhausts all122 actual subgroups, and computes every
relevant double-coset stabilizer. For a subgroup H and representative g,
the simple dimensions are `[H:H intersect gHg^-1]` times the projective
irreducible degrees of the intersection. Every stabilizer is squarefree
and has trivial Schur multiplier: its primary H² classes restrict
injectively to the Sylow subgroup by restriction/corestriction, and cyclic
Sylow groups have H²(-,C*)=0. Consequently arbitrary allowed ambient and
subgroup cocycles give the same dimension lists.

For transparency, every subgroup lies in C7 semidirect a subgroup of C6 or
S3. Clifford theory permits only irreducible degrees1,2,3,6. Its number of
linear characters is the order of the abelianization and its number of
irreducibles is the number of conjugacy classes. The script checks that
these numbers and the sum-of-degree-squares identity determine a unique
nonnegative degree list in every encountered stabilizer. Thus no numeric
character-table inference enters the finite enumeration.

The first and third proposed types never occur. Put F21=C7 semidirect C3
and F42=C7 semidirect C6, with faithful action. Type `[1^6,6]` only occurs for
(G,H)=(F42,C6) or(F42,F42), up to conjugacy. Type `[1^6,3^4]` only occurs
for G=F21 times C2 with |H|=3,6,21,42, or G=F42 with |H|=3,21.

For `[1^6,6]`, the resulting category is Rep(F42). If H=G, its cocycle is
trivialized by definition. For H=C6, restriction H³(F42,C*)→H³(C6,C*) is
an isomorphism: in the coprime extension spectral sequence the additional
term H³(C7,C*)^{C6} vanishes, since the faithful multiplier acts by its
square. The trivial restriction required by H therefore kills the ambient
associator. The split exact factorization then gives Rep(F42); compare
Etingof–Gelaki–Ostrik, *Classification of fusion categories of dimension pq*,
arXiv:math/0304194, Corollary7.4.

For `[1^6,3^4]`, the canonical adjoint is Rep(F21). If H=C3 or F21, support
in the normal index2 F21 gives a faithful C2 grading whose neutral category
has type `1^3,3^2`; EGO Theorem6.3 identifies it with Rep(F21). F21 is
centerless, so this neutral category is its own adjoint. Since D_ad is
contained in the neutral category while its adjoint is contained in D_ad,
these are equal. For G=F21 times C2 and H=C6 orG, coprime cohomology instead
gives Rep(F21) Deligne Rep(C2), with the same adjoint. These reductions
allow arbitrary ambient associators subject to the subgroup restriction.

A representation category of a squarefree group has a unique fiber functor.
Indeed, the classification of module categories/fiber functors by
central-type subgroups requires a subgroup of square order; in a squarefree
group only the trivial subgroup qualifies. See Ostrik, *Module categories,
weak Hopf algebras and modular invariants*, arXiv:math/0111139, Section3.4,
Theorem2 and Example(i). A tensor autoequivalence therefore preserves the
standard fiber functor up to monoidal isomorphism and is induced by a group
automorphism. In F21 orF42 write a^7=b^m=1 and bab^-1=a^lambda, with
lambda of orderm=3 or6. An automorphism sends a→a^u and b→a^v b^w;
compatibility forces lambda^w=lambda, hence w=1 modm. It fixes the
abelianization and every linear character.

The second base type therefore has six fixed invertibles. In the fourth,
the canonical adjoint contributes at least three fixed invertibles. Both
contradict the required number two. This proves the general theorem,
without a unitarity or pivotality hypothesis.

`dimension84_obstruction.py` independently reconstructs each positive
integral dimension character, checks all64 dimension equations, computes
full adjoint closure, and verifies the orbit pattern for every possible
central sign object in the supplied tensor. The finite group audit is
recomputed as part of its CLI. Normal and optimized invocations use explicit
exceptions; optimized Python does not remove proof checks.

Recovery note: after the transient workspace loss, these source files and
witnesses were reconstructed and freshly replayed. Earlier replay receipts
were not copied or represented as surviving artifacts.
