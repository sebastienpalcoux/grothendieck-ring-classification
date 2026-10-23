# Independent audit of the triality equivariantizations

The baseline construction realizes **R9_1_12 as a unitary fusion category**.
The direct central-half-braiding construction in the final section also
establishes **R9_1_108 as a unitary fusion category**. Both complete original
fusion tensors are independently verified.

The independent replay is verify_triality_equivariant.py, with receipt
triality_equivariant_audit.json. It uses only the Python standard library.
Its inputs are the original tensors and the proposed certificate; it imports
none of the discovery or construction programs.

## Coherent baseline action and Morita transport

Let \(\mathcal D=\operatorname{TY}(V_4,\chi,+1/2)\simeq
\operatorname{Rep}(D_8)\), where \(\chi\) is alternating. The automorphism
group of \(V_4\) is \(S_3\), and preserves \(\chi\). Permuting the invertible
labels and the corresponding summands of \(m\otimes m\), while fixing \(m\),
preserves all the standard TY associators. These permutations compose
strictly. They therefore specify an actual coherent action of \(S_3\),
including its compositor, rather than merely a homomorphism into the group
of equivalence classes of tensor autoequivalences.

There are three nonregular invertible \(\mathcal D\)-module categories.
They are the two reflection-subgroup module categories and the module
category of projective \(D_8\)-representations for its nontrivial Schur class.
The internal end of a simple object is \(1+h+m\). The three module classes
have the three different nonidentity choices of \(h\). Consequently the
above tensor \(S_3\) action permutes them transitively: their distinguishing
internal-end invertible is permuted in exactly this way. This also proves
that the \(C_3\) restriction moves every one of the three classes.

Take \(A=\operatorname{End}(V)\), where \(V\) is the two-dimensional
projective representation obtained from the \(D_{16}\) cover of \(D_8\).
The conjugation action on \(\operatorname{End}(V)\) is an ordinary \(D_8\)
action. This matrix algebra is Azumaya in the symmetric category
\(\operatorname{Rep}(D_8)\). In particular its equivariant bimodule category
is tensor equivalent to \(\operatorname{Rep}(D_8)\); the equivalence is
realized by the equivariant Morita equivalence for the matrix algebra.
A projective representation is sufficient here because the scalar
ambiguity cancels on the endomorphism algebra.

The stabilizing transposition can be represented by the actual group
automorphism
\[
a(r)=r^{-1},\qquad a(s)=sr.
\]
For the projective lift, write \(R\) for rotation through \(\pi/4\) and
\(S\) for a reflection. The real reflection \(T=SR^{1/2}\) satisfies
\[
T^2=1,\qquad TRT=R^{-1},\qquad TST=SR.
\]
Conjugation by \(T\) thus supplies an involutive, coherent algebra
isomorphism on \(A\). Equivalently the projective Schur class extends from
\(D_8\) to \(D_8\rtimes_a C_2=D_{16}\), as witnessed by the cover
\(D_{32}\to D_{16}\) and its restriction \(D_{16}\to D_8\).

One must still identify this actual automorphism action with the
restriction of the TY action, including coherence. The tensor
autoequivalence group of this TY category is \(S_3\), acting on the three
nonidentity invertibles. The two functors represent the same transposition.
For a fixed such class, coherent \(C_2\) lifts form a torsor under
\[
H^2(C_2,\operatorname{Aut}_{\otimes}(\operatorname{Id}_{\mathcal D}))
=H^2(C_2,C_2)=C_2.
\]
The nonidentity tensor automorphism of the identity is \(+1\) on the
invertibles and \(-1\) on \(m\). The strict TY lift has the two self-dual
equivariant objects \((m,+1)\) and \((m,-1)\): its tensorator preserves the
evaluation component of \(m\otimes m\). Changing the coherence class replaces
these scalars by \(+i,-i\), and duality exchanges the two objects. On the
group side the ordinary two-dimensional representation has a real
involutive implementing reflection, so its two extensions are self-dual.
It therefore belongs to the same coherent class as the strict TY lift.
This step excludes an unnoticed change of the \(C_2\) compositor.

Form the crossed product \(\mathcal B=\mathcal D\rtimes S_3\) and its
graded Morita dual
\[
\mathcal C=\operatorname{Bimod}_A(\mathcal B).
\]
Since \(A\) is neutral, \(\mathcal C\) is faithfully \(S_3\)-graded and its
neutral category is again tensor equivalent to \(\mathcal D\). Its
\(C_3\) subextension \(\mathcal E\) is nonregular, because the generator
moves the \(A\)-module class. The rank-two module classification and exact
fusion argument in THEORY.md identify \(K_0(\mathcal E)\) with R9_1_117.
This argument includes multiplicity-two possibilities before imposing
associativity; it does not assume the desired multiplicity-one answer.

The coherent equivariant algebra structure on \(A\) provides an invertible
object in the transposition component with coherent square \(1\). It
therefore makes \(\mathcal C\) a crossed product
\(\mathcal E\rtimes C_2\), with an honest categorical \(C_2\) action.
The Azumaya equivalence on the neutral component is natural for the
automorphism \(a\). Its equivariantization is consequently
\(\operatorname{Rep}(D_8\rtimes_a C_2)=\operatorname{Rep}(D_{16})\).
Indeed \(q=st\) satisfies \(q^2=r\) and \(sqs=q^{-1}\).

## Why the nonneutral equivariant simples are self-dual

For a faithful group grading, the subcategories on conjugate subgroups
are categorically Morita equivalent. The appropriate graded coset is the
invertible bimodule category implementing the equivalence. Applying this
to the three order-two subgroups of \(S_3\), each of the two nonregular
order-two subextensions is Morita equivalent to the regular one, hence
to \(\operatorname{Rep}(D_{16})\). Each nonregular subextension has profile
\(1^4,2^3\).

Here is the full subgroup-and-cocycle argument needed to deduce its
self-duality. Any category Morita equivalent to \(\operatorname{Rep}(D_{16})\)
is of the form \(\mathcal C(D_{16},1,H,\psi)\). In the double-coset
description, the cosets contained in the normalizer of \(H\) contribute
\[
[N_{D_{16}}(H):H]\cdot |H_{\mathrm{ab}}|
\]
invertibles whenever conjugation preserves the cohomology class of \(\psi\).
It does so for every subgroup here: cyclic groups have trivial Schur
multiplier, and \(V_4,D_8,D_{16}\) each have a Schur multiplier of order two,
on which every automorphism acts trivially. The double-coset projective
multiplier is the ratio of the two transported subgroup cocycles, so
equality of their classes suffices; equality of representatives is not
being assumed.

The complete subgroup possibilities are as follows.

| Subgroup \(H\) | Normalizer size | Forced number of invertibles |
|---|---:|---:|
| \(1\) | 16 | 16 |
| central \(C_2\) | 16 | 16 |
| rotation \(C_4\) | 16 | 16 |
| rotation \(C_8\) | 16 | 16 |
| \(V_4\) | 8 | 8 |
| index-two \(D_8\) | 16 | 8 |
| reflection \(C_2\) | 4 | 4 |
| \(D_{16}\) | 16 | 4 |

Thus only a reflection subgroup or the whole group can give the desired
four invertibles. The replay independently enumerates all 19 actual
subgroups, so no conjugacy class is omitted.

For a reflection \(H=C_2\), the cocycle is trivial up to coboundary.
Its five double cosets have size/stabilizer pairs
\((2,2),(2,2),(4,1),(4,1),(4,1)\). Inversion fixes each double coset.
On the two normalizer cosets, conjugation acts trivially on the stabilizer,
whose characters are real. On the other three cosets the stabilizer is
trivial. All seven resulting simples are therefore self-dual.
The verifier checks both double-coset inversion and stabilizer centrality.

For \(H=D_{16}\), the category is \(\operatorname{Rep}(D_{16})\)
independently of \(\psi\), up to tensor equivalence. One direct explanation
is to regard the \(\psi\)-twisted regular representation as a projective
vector space \(W\): \(\operatorname{End}(W)\) is an equivariant matrix
Azumaya algebra in \(\operatorname{Rep}(D_{16})\), and equivariant matrix
Morita equivalence gives the claimed tensor equivalence. Equivalently,
the dual of the rank-one pointed module associated to \(\psi\) is a
Drinfeld twist of the group algebra, which has the same tensor category.
Every irreducible representation of the dihedral group \(D_{16}\) is
self-dual.

Write the two nonneutral components of \(\mathcal E\) as
\(\{X_0,X_1\}\) and \(\{Y_0,Y_1\}\), with \(X_i^*=Y_i\).
The self-duality just proved for the objects in the nonregular order-two
components of \(\mathcal E\rtimes C_2\) says precisely
\(t(X_i)=Y_i\). Hence the two dimension-four simples of
\(\mathcal E^{C_2}\) restrict to \(X_i+Y_i\) and are self-dual.
This is the categorical input that fixes the orbit pairing in the tensor
reconstruction.

## Independent exact tensor reconstruction

The verifier reconstructs the neutral representation tensors directly
from character orthogonality, rather than importing the proposed neutral
ring. For \(C_8\rtimes C_2\), restrictions of the two-dimensional characters
have Fourier frequencies \(\{k,ak\}\), with \(a=7\) for \(D_{16}\) and
\(a=3\) for \(SD_{16}\). Fourier coefficient counting and the reflection
contribution give exact integer inner products.

It separately constructs the R117 tensor from the left and right
stabilizers \(h_L=1,h_R=2\), and reconstructs the restriction matrix \(F\).
Every dimension-four object is an induced \(X_i\). Frobenius reciprocity and
\[
\operatorname{Ind}(X)\otimes W
=\operatorname{Ind}(X\otimes\operatorname{Forget}(W)),\qquad
W\otimes\operatorname{Ind}(X)
=\operatorname{Ind}(\operatorname{Forget}(W)\otimes X)
\]
therefore determine every remaining product. When both factors are induced,
the verifier derives the product in both ways and checks equality.
It then checks the restriction homomorphism, all associativity equations,
duality, dimensions, multiplicity one, and all 729 original coefficients
under each asserted based isomorphism.

For R9_1_12 the source-to-model permutation is
\[
(0,3,2,4,8,7,6,1,5),
\]
and all nine simples are self-dual. This gives the complete audited model.

For R9_1_108 the source-to-model permutation is
\[
(0,4,6,8,7,1,2,3,5).
\]
The reconstructed model dual permutation is
\((0,1,2,3,6,5,4,8,7)\). The direct categorical construction below
provides exactly these action data and establishes its existence.

## References and scope

The underlying module-category classification for a group representation
category is by subgroup/projective-representation data. The group-theoretical
double-coset formula and graded Morita transport used here are standard
categorical Morita theory. Nikshych--Riepel, arXiv:1309.5026, Section 9,
compute the relevant Brauer--Picard group and exhibit the nonregular
\(C_3\) extension of \(\operatorname{Rep}(D_8)\).

Their Remark 9.4 about \(\operatorname{Rep}(Q_8)\) uses the definition of
nontrivial extension in their Section 4: some homogeneous component is not
regular as a left module. It therefore does rule out the alternative
\(Q_8\) neutral category in the separate necessity argument for R117.
The existence of order-three tensor autoequivalences of
\(\operatorname{Rep}(Q_8)\) does not contradict that statement.

This baseline construction uses unitary TY data, finite coherent unitary
actions, and equivariant finite-dimensional matrix algebras. It is unitary.
No exclusion of either dimension-24 profile \(1^8,4\) or \(1^4,2,4\) is
claimed or needed for this positive construction.


## Accepted direct categorical construction for R9_1_108

The following direct construction establishes **R9_1_108 as a unitary
categorical model**. It does not require the broader classification of
all possible involutions.

Write \(\alpha\) for the accepted baseline coherent involution of
\(\mathcal E\), and put
\[
A=\operatorname{Inv}\mathcal Z(\mathcal D)
=Z(D_8)\times\widehat{D_8}\cong\mathbf F_2^3.
\]
Let \(z\in A\) denote the nontrivial half-braiding on the tensor unit:
it acts by \(-1\) on \(m\), and by \(+1\) on all neutral invertibles.
The regular-module stabilizer \(S_3\subset\operatorname{BrPic}(\mathcal D)=S_4\)
fixes \(z\).

Its \(S_4\) orbit has four elements, not one. Indeed, if the nonregular
triality fixed \(z\), then the relative-center equivariantization would
lift it to a central structure on \(1_{\mathcal E}\). The only possible
projective-equivariance obstruction is in \(H^2(C_3,\mathbf C^*)=0\).
But all central structures on \(1_{\mathcal E}\) are
\[
\operatorname{Aut}_{\otimes}(\operatorname{Id}_{\mathcal E})
=\operatorname{Hom}(U(\mathcal E),\mathbf C^*)
=\operatorname{Hom}(C_3,\mathbf C^*)=C_3,
\]
and each restricts trivially to the neutral category. None can restrict
to \(z\). Since the regular-module stabilizer is a maximal subgroup
of \(S_4\), the orbit therefore has exactly four elements.

Denote them by \(w_p,w_q,w_a,w_b\), with \(w_p=z\).
Their only relation is
\(w_p+w_q+w_a+w_b=0\): a relation of weight one or two would make one
zero or two equal, while applying permutations to a relation of weight
three would also make two equal. They span \(A\), proving the
coefficient-module description
\[
A\simeq\mathbf F_2^4/\langle(1,1,1,1)\rangle.
\]
The triality cycles \(p,a,b\) and fixes \(q\), so its fixed subgroup
is precisely \(\{0,w_q\}\). The reversing transposition fixes \(p,q\)
and exchanges \(a,b\).

On the neutral category this transposition is the group automorphism
\(a\) audited above. Its norm on \(A\), in group-theoretic coordinates,
has image generated by the canonical symmetric central lift
\(\widetilde h=(1,h)\) of the unique nontrivial fixed character \(h\).
In the four-point description the same norm image is
\(w_a+w_b=w_p+w_q\). Thus
\[
w_q=z+\widetilde h.
\]
In particular the underlying neutral object of \(w_q\) is \(h\).
Since \(w_q\) is triality invariant, the relative-center description and
\(H^2(C_3,\mathbf C^*)=0\) lift it to an actual central structure on
\(h\) in \(\mathcal E\). The three choices of equivariance differ by
characters of \(C_3\); all restrict to the same \(w_q\) on \(\mathcal D\).

Choose an invertible \(g\in\mathcal D\) with
\(g\alpha(g)=h\), which is possible because the norm of the transposition
on \(V_4\) is its fixed line. Define the tensor autoequivalence
\[
\beta=\operatorname{Ad}_g\circ\alpha.
\]
The baseline action coherence identifies \(\beta^2\) with
\(\operatorname{Ad}_{g\alpha(g)}=\operatorname{Ad}_h\).
The central structure just constructed trivializes \(\operatorname{Ad}_h\).
Consequently the class of \(\beta\) defines a homomorphism
\(C_2\to\operatorname{Aut}_{\otimes}(\mathcal E)\).

The obstruction to upgrading this homomorphism to an actual categorical
action lies in
\[
H^3(C_2,\operatorname{Aut}_{\otimes}(\operatorname{Id}_{\mathcal E}))
=H^3(C_2,C_3)=0.
\]
The equality holds for either \(C_2\) action on \(C_3\), because
multiplication by two is invertible on the coefficient group.
Likewise \(H^2(C_2,C_3)=0\). Hence an actual coherent action exists.
Any required correction to the square trivialization is a character of
\(U(\mathcal E)=C_3\), and is the identity on \(\mathcal D\).

There are two separately determined changes from \(\alpha\) to \(\beta\).

First, on the neutral symmetric category, \(\operatorname{Ad}_g\) is
canonically identified with the identity. Comparing the squares under
that identification uses the canonical symmetric central lift of
\(g\alpha(g)=h\). The chosen square trivialization instead uses \(w_q\).
Their ratio is exactly \(z\). The neutral square coherence therefore
changes sign on \(m\). The two equivariant lifts of \(m\) become a dual
pair, with scalars \(+i,-i\). Equivalently, the neutral group presentation
changes from \(t^2=1\) to \(t^2=r^2\), with the same conjugation action
\(trt^{-1}=r^{-1}\), \(tst^{-1}=sr\). Setting \(q=st\) gives
\(q^2=r^3\) and \(sqs=q^3\), identifying the group as \(SD_{16}\).
This derives the neutral representation tensor used in the replay.

Second, in the canonical R117 labels, the left/right stabilizers are
\(1,2\), the fixed character is \(h=3\), and either norm preimage is
\(g=1\) or \(2\). The inner action of \(g\) changes the nonneutral
index by the sum of its left and right permutation characters, which is
one for these two choices. Thus
\[
\beta(X_i)=Y_{i+1}.
\]
The dimension-four restrictions are precisely \(X_i+Y_{i+1}\).

These are exactly the two data used in the independent tensor reconstruction:
neutral \(\operatorname{Rep}(SD_{16})\) and the opposite nonneutral orbit
pairing. They produce R9_1_108 with the based permutation recorded above.
All central structures, inner functors, and finite-order coherence
corrections can be taken unitary. The resulting model is therefore unitary.

The categorical-action obstruction used here is the standard obstruction
for a group homomorphism into the tensor-autoequivalence group to lift to
the categorical automorphism group; see Etingof--Nikshych--Ostrik,
Fusion categories and homotopy theory, arXiv:0909.3140, Corollary 7.9.
The relative-center lifting is the graded-center equivariantization of
Gelaki--Naidu--Nikshych, arXiv:0905.3117.


## Independent acceptance of the complete R117 branch

The exhaustive action classification in TRIALITY_ACTIONS.md, Sections 0--3,
has also been independently audited and is accepted. Its conclusion is
stronger than the two positive constructions: allowing every
categorification of the R117 ring and every coherent grading-reversing
involution yields only the fusion rings R9_1_12 and R9_1_108.

The internal-end algebras \(1+h_L+m\) and \(1+h_R+m\), with distinct
\(h_L,h_R\), force \(\chi(h_L,h_L)=\chi(h_R,h_R)=1\).
Multiplication by either stabilizer element on its internal-end algebra
is invertible, so the relevant multiplication maps involving \(m\) are
nonzero; the TY associator on \((h,m,h)\) then gives this equality.
A nonalternating nondegenerate bicharacter on \(V_4\) has just one
nonzero isotropic element. Thus the bicharacter is alternating.
The negative TY sign would give \(\operatorname{Rep}(Q_8)\), excluded
by Nikshych--Riepel Remark 9.4 for a nonregular extension. Hence every
neutral category is \(\operatorname{Rep}(D_8)\).

In \(S_4=\operatorname{BrPic}(\mathcal D)\), all nonregular triality
homomorphisms are conjugate under the regular-point stabilizer \(S_3\).
The intersection of the triality normalizer with that stabilizer has
one nonidentity element, the reversing transposition. There is therefore
one possible \(S_3\) Brauer--Picard homomorphism up to the allowed equivalences.

For its coefficient module
\(A=\mathbf F_2^4/\langle(1,1,1,1)\rangle\), already derived above,
\[
H^2(S_3,A)=C_2,\qquad
H^3(S_3,\mathbf C^*)=C_6,\qquad H^4(S_3,\mathbf C^*)=0.
\]
The first obstruction vanishes because the baseline construction exists.
Thus the extension-classification torsors include exactly the two
multiplication classes and the six scalar associator classes described
in the proposed proof.

For a fixed \(C_3\)-primary scalar class, the two possible \(C_2\)-primary
scalar classes are distinguished by whether the odd component has a
coherent order-two invertible section. Its group of invertibles is an
extension of \(V_4\) by the transposition action of \(C_2\).
For this action, the fixed subgroup and the norm image are the same
order-two subgroup, so \(H^2(C_2,V_4)=0\), and the group extension splits.
There are two order-two lifts of the nonidentity quotient element,
and they are conjugate by neutral invertibles. Their restricted
associator classes consequently agree. Inflating the nontrivial
\(H^3(C_2,\mathbf C^*)\) class reverses that value, so exactly one
scalar choice admits a \(\operatorname{Vec}(C_2)\) section.
The vanishing \(H^2(C_2,\mathbf C^*)=0\) removes any further
section-embedding ambiguity. Conjugate sections give equivalent actions.

Finally, changing the \(C_3\)-primary scalar class changes neither the
R117 fusion ring nor its object permutation. Its restriction to the
neutral \(C_2\) subextension is trivial, so the neutral equivariantization
and the restriction matrix \(F\) are unchanged. Every nonneutral
equivariant simple is induced. The two projection formulas used in the
exact replay therefore determine every product from these unchanged
data. This proves equality of fusion tensors for all three scalar
\(C_3\) twists, without relying on an assumed trace convention.

The two accepted categorical constructions realize the two remaining
multiplication classes and give exactly R9_1_12 and R9_1_108.
Accordingly R9_1_62 and R9_1_87 cannot arise from the R117
de-equivariantization branch.
