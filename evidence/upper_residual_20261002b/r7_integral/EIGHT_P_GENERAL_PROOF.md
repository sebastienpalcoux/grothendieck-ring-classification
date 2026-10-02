# The dimension (8p) family: R7_2_70, R7_2_213, R7_4_358

The source tensors have dimensions (1^4,2,d^2), with

\[
(p,d)=(5,4),\ (5,4),\ (17,8),\qquad \operatorname{FPdim}\mathcal C=8p.
\]

They have trivial universal grading, and every invertible fixes every
noninvertible simple. **The invertible group of R7_2_213 is (C_4); those
of R7_2_70 and R7_4_358 are (V_4).** The earlier retained summary's common

\(V_4\) description was inaccurate. The correction strengthens the
R7_2_213 contradiction below and changes no classification decision.

Assume a categorification 
\(\mathcal C\). It is solvable. Since its universal grading is trivial,
the last prime cyclic step is an equivariantization, and the prime must be
2 because its representation characters embed among the four invertibles.
Write (\mathcal C=\mathcal D^{C_2}). For a cyclic order-two action, a
simple fixed by the sign character comes from a free two-element orbit;
the two simples exchanged by the sign come from a fixed underlying simple.
The sign fixes the dimension-two and the two dimension-
\(d\) objects and pairs the four invertibles. Thus

\[
\operatorname{FPdim}\mathcal D=4p,
\qquad \mathcal D:\ 1^4,(d/2)^4.
\]

## No faithful grading of 
\(\mathcal D\)

If a (C_2) grading existed, the vector space

\(\operatorname{Hom}(U(\mathcal D),C_2)\) would be nonzero and have
dimension at most two, since 
\(|U(\mathcal D)|\mid4p\). An involution acting on a nonzero vector
space of dimension at most two over 
\(\mathbb F_2\) has a nonzero fixed vector. The corresponding grading
of 
\(\mathcal D\) is invariant under the outer 
\(C_2\) action, so degrees of equivariant simples define a faithful

\(C_2\) grading of 
\(\mathcal C\). This contradicts 
\(U(\mathcal C)=1\).

There is no 
\(C_p\) grading either. When 
\(p=17\), the rank of 
\(\mathcal D\) is eight, smaller than the number of nonempty
components. When 
\(p=5\), all four invertibles lie in the neutral component, whose
dimension is four. Its other four components each contain a single
dimension-two simple. A rank-one module over

\(\mathrm{Vec}_A^\omega\), 
\(|A|=4\), has scalar module associativity satisfying

\(\delta\psi=\omega\), so 
\(\omega\) is a coboundary. The grading would give an element of
order five in 
\(\operatorname{BrPic}(\mathrm{Vec}_A)\): the map from the grading
group is injective because an identity bimodule has regular left rank
four, whereas each nonneutral component has rank one. But the hyperbolic
orthogonal groups for 
\(A=C_4,V_4\) have orders four and 72 respectively, as independently
enumerated by the verifier. Neither has an element of order five.

Every nontrivial group of order dividing 
\(4p\) is solvable and has a prime cyclic quotient of order 2 or

\(p\). The preceding arguments therefore imply 
\(U(\mathcal D)=1\).

## The next two equivariantizations

Again solvability forces 
\(\mathcal D=\mathcal E^{C_2}\), with

\(\operatorname{FPdim}\mathcal E=2p\).
The orbit formula leaves the following possibilities.

For 
\(p=5\), the four invertibles in 
\(\mathcal D\) give exactly two fixed invertibles in 
\(\mathcal E\). If 
\(b\) denotes the number of fixed dimension-two simples in

\(\mathcal E\), its possible types are

\[
1^{10},\quad 1^6,2,\quad 1^2,2^2.
\]

Six invertibles cannot form a subcategory of dimension ten. The pointed
case is also impossible: each group of order ten has a unique nontrivial
character to 
\(C_2\), preserved by every automorphism. Its pointed grading would
survive equivariantization and grade 
\(\mathcal D\) by 
\(C_2\), already excluded. Thus 
\(\mathcal E\) has type 
\(1^2,2^2\).

For 
\(p=17\), dimensions two cannot occur in 
\(\mathcal D\). It follows that 
\(\mathcal E\) has two invertibles, paired dimension-two objects,
and possibly fixed dimension-four objects. Its possible types are

\[
1^2,2^{8-4b},4^b,\qquad b=0,1,2.
\]

The Frobenius property rules out a dimension-four simple in global
dimension 34. Hence 
\(\mathcal E\) has type 
\(1^2,2^8\).

In either case 
\(U(\mathcal E)=1\). A 
\(C_p\) grading is excluded by rank smaller than 
\(p\). A 
\(C_2\) grading would have a neutral fusion subcategory of prime
dimension 
\(p\), hence would be pointed with 
\(p\) invertibles, while the entire category has only two.
Solvability now yields

\[
\mathcal E=(\mathrm{Vec}_{C_p}^\omega)^{C_2}.
\]

The action on 
\(C_p\) is inversion: its only fixed point is the identity, since
the two identity equivariants exhaust the two invertibles of

\(\mathcal E\).

## Combine the three steps

The central lift of the unique nontrivial invertible of 
\(\mathcal E\) is unique because its universal grading is trivial.
Consequently the outer action on 
\(\mathcal E\) preserves the central 
\(\operatorname{Rep}(C_2)\), and 
\(\mathcal D=(\mathrm{Vec}_{C_p}^\omega)^K\) for an order-four
group 
\(K\). Its embedded 
\(\operatorname{Rep}(K)\) consists of invertibles and accounts for
all four invertibles of 
\(\mathcal D\). Since 
\(U(\mathcal D)=1\), all of their central lifts are unique. The
outer action preserves this entire central Tannakian subcategory.
Equivariantization in stages therefore gives

\[
\mathcal C=(\mathrm{Vec}_{C_p}^\omega)^H,\qquad |H|=8.
\]

The embedded 
\(\operatorname{Rep}(H)\) has exactly four one-dimensional simples
and one dimension-two simple, since the only other available dimensions
are 
\(4\) or 
\(8\). Hence 
\(H\) is nonabelian, and its abelianization is 
\(V_4\) (the two nonabelian groups of order eight are

\(D_8,Q_8\)). This immediately contradicts the 
\(C_4\) group of invertibles in R7_2_213.

For the other two rings, the action 
\(H\to\operatorname{Aut}(C_p)\) has cyclic image, so it factors
through a quotient of 
\(V_4\) of order at most two. Orbits therefore have size at most
two. Irreducible projective representations of an order-eight
stabilizer have degree at most two; for an order-four stabilizer their
degree is also at most two. Thus all dimensions are at most four,
excluding R7_4_358, whose two remaining simples have dimension eight.

For R7_2_70, remove the possible projective stabilizer ambiguity as
follows. 
\(H^2(C_5,\mathbb C^\times)=0\), and

\(H^2(H,\widehat C_5)=0\) because the coefficient group is
5-primary and 
\(|H|=8\). Represent 
\([\omega]\) by a 
\(\mu_5\)-valued cocycle. Averaging over 
\(H\), using the inverse of eight modulo five, supplies an invariant
representative of the same invariant cohomology class. On this model
the object permutation action is strict. The first vanishing makes
each other lift of an object permutation tensor-isomorphic to this
one; the second removes its coherence two-cocycle. Therefore all
stabilizer multipliers are coboundaries. For a two-element orbit its
stabilizer is an abelian group of order four, so its irreducible
degrees are one and the corresponding simples have dimension two.
For a fixed orbit the ordinary representations of 
\(H\) have dimensions at most two. No dimension-four simple occurs.
This excludes R7_2_70.

See `STRUCTURAL_INPUTS.md` for the cited category-theoretic results and
`verify_general_families.py` for exact source binding, ring premises and
the two small orthogonal-group enumerations. The averaging argument
is finite coprime cohomology, not an enumeration of centers or modular
data.
