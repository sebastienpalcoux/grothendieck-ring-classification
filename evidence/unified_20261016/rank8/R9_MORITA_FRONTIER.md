# R8_1_9: an actual involution algebra and the remaining Morita alternative

**Current status: generally excluded.** The final theorem is `R9_CENTER_TRACE_PROOF.md`, verified by `verify_r9_center_trace.py`. The text below records an intermediate necessary reduction; its former remaining class-zero alternative is now excluded by the cyclic induction Fourier bound. Historical scoped receipts remain valid.


**Scope:** necessary reductions only. At this intermediate stage R8_1_9 had not yet been resolved. The exact finite enumeration below does not supply associators for any candidate dual.

**Updated frontier.** The separately verified center-trace theorem in `R9_POINTED_CLASS2_OBSTRUCTION.md` rules out pointed associator class two. Hence the pointed C4 associator is trivial, and the only surviving Morita alternative is R8_2_477 with exactly one negative nonidentity pointed indicator and three positive/one negative nonpointed indicators. The two-branch reduction below is retained as the finite intermediate step; its class-two branch is subsequently eliminated by that theorem.

Put d=2+sqrt(5). The source is commutative, with pointed C4 on labels (0,1,7,2), and noninvertible orbit (5,3,6,4). The self-dual noninvertibles are 5 and 6. Each has every invertible appearing once in its cube. After the published two-dimension Galois pseudo-unitarity reduction, the pivotal odd-isotypic lemma therefore forces

    nu_2(5)=nu_2(6)=nu_2(7)=+1.

Thus A=1+7 is an actual connected separable algebra. If k in Z/4 is the pointed C4 associator class, k is even.

## The exact module and quadratic dual enumeration

The four simple A-modules have underlying supports

    [0,7], [1,2], [3,4], [5,6].

Their action matrices are duplicated pairs of I,P,R,PR, where

    P = [[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],
    R = [[0,0,1,0],[0,0,0,1],[1,0,2,2],[0,1,2,2]].

These obey P^2=I, PR=RP and R^2=I+2R+2PR. Their first columns are the four standard basis vectors, so this is the regular representation of the rank-four 2D2 based ring. In particular, a commuting matrix is determined by its first column.

Every H-by-H support orbit has size two and stabilizer C2. Each contributes two simple A-bimodules, with one-dimensional stabilizer representations. Consequently the dual has four invertibles and four noninvertibles of dimension d. The nontrivial dual character beta swaps the two simples over each support orbit. An invertible over [1,2] swaps the two noninvertible support orbits. Thus the pointed group G', of order four, acts freely and transitively on the four noninvertibles.

Choose a noninvertible r. Every possible dual tensor consequently has the quadratic form

    r g = tau(g) r,
    r^2 = g0 + sum_(g in G') m_g g r,

where tau is an involutive automorphism of the abelian group G', g0 is tau-fixed, and the nonnegative integers m_g sum to four. No multiplicity bound from the original census is assumed: m_g ranges through 0,...,4.

The module representation imposes

    tau(beta)=beta, tau(g)=g modulo <beta>,
    g0 in <beta>,
    sum_(g in each beta-coset) m_g = 2.

The elementary enumeration in `verify_r9_morita_frontier.py` exhausts both groups of order four, all automorphisms, all g0, and every composition of four into four nonnegative entries. It tests full associativity and both Frobenius reciprocity identities, then quotients by every based relabelling (group automorphism and choice of r). There are 22 abstract quadratic tensors before the module condition. Exactly nine admit an appropriate beta:

| Pointed group | Possible census tensors |
| --- | --- |
| C4 | R8_2_25, R8_1_9, R8_1_15, R8_1_12 |
| V4 | R8_2_477, R8_2_478, R8_1_69, R8_1_53, R8_1_49 |

The source-bound published decisions already exclude R8_2_25, R8_2_478, and R8_1_49. This leaves six tensors before indicator restrictions.

## Morita-invariant indicator restriction

For a positive spherical fusion category, its total second indicator

    T_2(C)=sum_(X simple) FPdim(X) nu_2(X)

is Morita invariant. Indeed, the Ng--Schauenburg induction formula rewrites it as

    (1/Dim(C)) sum_(Z simple in Z(C)) theta_Z^2 dim(Z)^2.

R8_1_9 has T_2=2+2d. In R8_1_15 and R8_1_69, every noninvertible is self-dual and its odd cube forces its second indicator to be +1. Their d-coefficient in T_2 is therefore four, which cannot match two. R8_1_12 and R8_1_53 have no self-dual noninvertible, hence d-coefficient zero. The only remaining dual-ring possibilities are therefore

    R8_1_9 itself, or R8_2_477.

In the second possibility exactly three noninvertibles have second indicator +1 and one has indicator -1.

The pointed part further separates these alternatives. If k=0, the pointed dual along C2 is V4 with representative cocycle

    omega((q,chi),(q',chi'),(q'',chi''))=(-1)^(chi*q'*q''),

so precisely one of its three nonidentity invertibles has indicator -1. Thus the dual must have the R8_2_477 tensor with this one-anomaly pointed class and the three-positive/one-negative noninvertible pattern. If k=2, the pointed category has FS exponent eight. Its pointed Morita dual has the same exponent, whereas every pointed V4 category has exponent dividing four. Thus the dual pointed group is C4 (again class two), and its fusion tensor must be R8_1_9.

The independent exact center-trace obstruction in `R9_POINTED_CLASS2_OBSTRUCTION.md` eliminates the k=2 branch: all eight character-labelled low-center frames contradict one integer separating covector after Galois pairing and the phase constraint theta^4=-1 over the order-four invertibles. Thus k=0 and the R8_2_477 branch are the sole surviving alternative. The R8_2_477 tensor alone does not classify its possible associators.

## Why the immediate known-2D2 construction does not solve R9

In Grossman's standard realization P=M rtimes_(alpha2) C2, let lambda implement the crossed product and let phi fix M and send lambda to -lambda. The known 2D2 category Q1 has generators g=tilde alpha1 and r=tilde rho. They commute with phi as factor endomorphisms. The actual extension generated by Q1 and phi has the R8_2_477 tensor and a one-anomaly pointed V4 class.

However phi is exactly the dual action of the de-equivariantization from the standard C4 Haagerup--Izumi category P1. Consequently this crossed extension is Morita equivalent to P1, whose total second indicator is 2+4d. Its four noninvertibles all have positive second indicator. Condensing 1+phi recovers P1, not R8_1_9. Choosing the other positive pointed involution cannot change the Morita-invariant total indicator.

Twisting this extension by the nontrivial three-cocycle on its faithful C2 grading changes the four noninvertible signs to two positive and two negative; all three nontrivial pointed indicators become negative. Its total second indicator is then -2, still incompatible with R8_1_9. Thus neither this canonical action nor its grading-cocycle twist supplies the required construction.

## Portable exact replay

Run `python verify_r9_morita_frontier.py --repo /absolute/path/to/repo` for the finite Morita reduction, and `python verify_r9_pointed_class2.py --repo /absolute/path/to/repo` for the subsequent elimination of its class-two branch.
The standard-library verifier binds the source and all nine candidate tensors to their archived digests, rechecks the source fusion axioms and exact dimension character, reconstructs its module action, enumerates every quadratic tensor described above without assuming the census multiplicity bound, and tests the module quotient. It checks the finite indicator hypotheses and the explicit pointed dual cocycle. Normal and optimized runs have identical PASS receipts.

The verifier is a necessary-condition certificate, not a categorifiability decision. The categorical bridges and their scope are explained above and independently audited. No classification count changes on the basis of this note.

Primary inputs are Schopieray, *Categorification of integral group rings extended by one dimension*, published Lemma 3.1; the pivotal parity lemma proved in `R49_FS_MORITA_PROOF.md`; Ng--Schauenburg's center-induction formula and Morita invariance of Frobenius--Schur exponent; and Grossman, arXiv:1612.07185, Section 4.1, Lemma 4.3 (the equivariantization), and Section 4.2 immediately after Lemma 4.6 (the crossed extension), for the concrete 2D2 orbifold and its dual action.
