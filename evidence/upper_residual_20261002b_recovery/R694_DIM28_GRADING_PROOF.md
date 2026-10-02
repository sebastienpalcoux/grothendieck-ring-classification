# General exclusion of R8_2_694

## Statement and exact census premises

No fusion category over C has global Frobenius–Perron dimension 56, simple dimensions 1^4, 2, 4^3, and C_ad=C. In particular R8_2_694 has no complex fusion categorification. No pivotal, spherical, pseudo-unitary, unitary or braided assumption is used.

The fresh source check uses the published rank-eight census, sorted lexicographically by all tensor coefficients inside exact multiplicity 2. The tensor fingerprint is
cad504d4abf1b34f332a7184d3cbf725d4e04d1fcb955fde654aa1516ec86831.
The dimension vector in the census basis is [1,1,1,1,2,4,4,4]. All64 dimension products and4096 associativity relations hold, and the adjoint closure contains all8 basis objects. This gives precisely the theorem premises. The additional invertible-ring structure is unnecessary.

## First equivariantization

ENO's solvability theorem for dimension p^a q^b and the characterization by prime cyclic extensions/equivariantizations apply to dimension56=2^3·7. The final operation cannot be a nontrivial extension because C_ad=C. It cannot be C7-equivariantization because Rep(C7) would supply seven invertibles. Thus C=D^C2, FPdim(D)=28.

Every simple Y of D lies under an equivariant simple of dimension
[C2:(C2)_Y] dim(pi) FPdim(Y).
Consequently FPdim(Y) is rational, hence integral as an algebraic integer. D cannot be pointed: the C2-equivariantization of a pointed category has simple dimensions at most2, because stabilizer C2 has no nontrivial projective Schur multiplier. C has4-dimensional simples.

## Dimension28 lemma

Every nonpointed integral fusion category D of dimension28 has U(D)=C2 and adjoint fusion ring Rep(D14), where D14 has order14.

Jordan–Larson, Theorem1.1, implies D is group-theoretical: p=7,q=2, and7 does not divide q+1=3. Write D=C(G,omega,H,psi), |G|=28. Sylow theory and Schur–Zassenhaus give G=C7 ⋊ P, where P=C4 or V4. Its action on C7 is trivial or inversion. The subgroup orders are1,2,4,7,14,28. The standard GT simple-object formula uses double cosets and projective irreducibles of H ∩ gHg^-1.

For |H|=1 or7, H is normal cyclic and all stabilizer projective irreducibles have degree1, so the category is pointed. Central H of order2 gives the same result.

If H has order2 and is noncentral, P=V4 with inversion action. The subgroup C7 ⋊ H=D14 is normal of index2; support supplies a faithful C2 grading. Its neutral component is C(D14,omega',C2,psi') and has the Rep(D14) fusion ring by the coprime cocycle reduction below with complement C2.

If |H|=14, H is normal. An abelian H=C14 gives a pointed category because H²(C14,C*)=0. Otherwise H=D14; support in G/H gives a C2 grading with neutral Rep(H). The multiplier H²(D14,C*) is zero by the coprime C7 ⋊ C2 spectral sequence, so cocycle-twisted support cosets do not create omitted projective degrees.

For H=G the condition dpsi=omega permits a simultaneous gauge to(1,1), giving Rep(G). A nonabelian group of order28 has center C2 and quotient D14. Thus its adjoint category is Rep(D14), with universal grading C2.

For |H|=4, conjugate H to P. Positive-degree cohomology of C7 with C* coefficients is7-primary. Therefore
H^a(P,H^b(C7,C*))=0 for a,b>0.
Restriction to P is split by inflation. Since omega|P=dpsi, its class has zero P-component and is determined by a P-invariant class in H³(C7,C*).

Choose a normalized mu7-valued cocycle representing that class. The map H³(C7,mu7)→H³(C7,C*) is an isomorphism. Multiplicatively average the representative over P and raise to the inverse of |P| modulo7. The result alpha is strictly P-invariant and has the original class. Extend it to G by
omega_alpha((n1,p1),(n2,p2),(n3,p3))
=alpha(n1,p1·n2,p1p2·n3).
This representative restricts identically to1 on P. After gauging omega to it, psi is a2-cocycle on P. Inflate psi along G→P; the corresponding identity tensor autoequivalence removes psi without changing omega_alpha.

Hence the category is (Vec_C7^alpha)^P with strict permutation action. If P acts trivially, it is pointed. Otherwise the kernel K=C2 acts strictly trivially. K-characters give a faithful C2 grading, whose neutral category is
(Vec_C7^alpha)^(P/K).
Its fusion ring is Rep(D14), with dimensions1²,2³.

In every nonpointed case the displayed neutral component is adjoint to itself. Its noninvertibles X_i, indexed by nonzero C7 elements modulo inversion, satisfy
X_i²=1+epsilon+X_(2i).
Doubling cycles through all three indices. Since the adjoint of the entire graded category is contained in the neutral component and contains that component's adjoint, it equals the neutral component. This proves U(D)=C2 exactly.

## Contradiction

The outer C2 action preserves the canonical adjoint category D_ad. It permutes three2-dimensional simples by an involution, so at least one is fixed. Its stabilizer is C2 and its projective obstruction vanishes since H²(C2,C*)=0. The two characters of C2 therefore supply two distinct2-dimensional equivariant simples in C.

The census ring has only one2-dimensional simple. This contradiction proves the general exclusion.

## Primary references

- Etingof–Nikshych–Ostrik, Weakly group-theoretical and solvable fusion categories, https://arxiv.org/pdf/0809.3031 .
- Jordan–Larson, On the classification of certain fusion categories, Theorem1.1, https://arxiv.org/pdf/0812.1603 .
- Burciu–Natale, Fusion rules of equivariantizations of fusion categories, Corollary2.13 (orbit/stabilizer dimensions).
- Standard group-theoretical double-coset description and universal-adjoint grading description.

The theoretical argument was independently audited during recovery. The source premises were then independently replayed from the remote published census. It is separate from the not-yet-rebuilt publication ledgers.
