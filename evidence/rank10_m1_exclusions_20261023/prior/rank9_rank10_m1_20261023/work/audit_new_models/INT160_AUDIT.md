# Independent audit: the dimension-160 obstruction

**Verdict: accepted.** The corrected argument excludes \(\mathrm{R10\_1\_83}\) and \(\mathrm{R10\_1\_177}\) as Grothendieck rings of complex fusion categories. No pivotal, spherical, pseudo-unitary, or unitary hypothesis is used. The earlier abstract action-lifting assertion is unnecessary; the central Tannakian construction below supplies the dihedral equivariantization directly.

The independent replay is:

    python work/audit_new_models/verify_int160_audit.py

It imports no construction or search code. It uses Python's standard library, the original tensors in work/input_audit/tensors.json, and the four explicit reference cochains in work/resolve_integral/normal_forms160.json. It outputs int160_audit.json. The replay passed. The finite checks support the proof; they do not infer exhaustiveness of possible categorical actions from a search.

## 1. What the original tensors force

Both rings have dimension profile \(1^2,2^2,5^6\), total FP dimension 160, trivial universal grading, and a central nonidentity invertible \(g\). Tensoring by \(g\) fixes exactly the two dimension-2 simples and exchanges the six dimension-5 simples in three pairs. These assertions are checked directly on the original basis, using an exact positive dimension character and an exact adjoint-subring closure.

The original-basis noncommutativity witnesses are:

| Ring | \(i,j,k\), zero based | \(N_{ij}^k\) | \(N_{ji}^k\) |
|---|---|---:|---:|
| R10_1_83 | 1,6,7 | 0 | 1 |
| R10_1_177 | 1,3,5 | 0 | 1 |

By ENO Theorem 1.6, any prospective category \(\mathcal C\) is solvable. ENO Proposition 4.4 gives an actual chain of prime cyclic extensions and equivariantizations ending in \(\mathcal C\). Its last step cannot be a nontrivial extension, because \(\mathcal C_{\rm ad}=\mathcal C\). Its last equivariantizing group must have order 2: its representation category embeds in \(\mathcal C\), which has exactly two invertibles. Thus

\[
\mathcal C=\mathcal D^{C_2}.
\]

For \(C_2\), a fixed simple of \(\mathcal D\) has two equivariant lifts, exchanged by the sign representation. A free orbit has one lift, fixed by sign. The input permutation therefore forces the type of \(\mathcal D\) to be \(1^5,5^3\). Its invertibles form \(C_5\); the outer involution inverts them and fixes the three dimension-5 simples.

The group \(C_5\) acts trivially on the set of three noninvertibles by left tensoring. Consequently all five invertibles occur in \(Y Y^*\), for every dimension-5 simple \(Y\), so \(C_5\subset\mathcal D_{\rm ad}\). Its possible dimensions are \(5+25k\), \(0\leq k\leq3\). Since the homogeneous components of the universal grading have equal dimension, this number divides 80; only 5 and 80 remain. Dimension 5 is impossible: every simple belongs to a homogeneous component, and a dimension-5 simple contributes 25 to its component's dimension. Hence \(\mathcal D_{\rm ad}=\mathcal D\).

Apply the solvable last-step argument to \(\mathcal D\). It yields a canonical central copy of \(\operatorname{Rep}(C_5)\) whose underlying objects are all five invertibles of \(\mathcal D\). Nothing about the multiplication of the three noninvertibles, beyond the dimension profile, is needed here.

## 2. The central dihedral subcategory exists

If a fixed invertible object \(u\) has two half-braidings, their ratios on simple objects \(X\) are scalars \(\lambda_X\). The half-braiding hexagon implies

\[
\lambda_Z=\lambda_X\lambda_Y
\quad\text{whenever }Z\subset X\otimes Y.
\]

Thus the ratio is a tensor natural automorphism of the identity functor, equivalently a character of the universal grading group. Because \(\mathcal D_{\rm ad}=\mathcal D\), it is trivial. Therefore each underlying invertible has a unique central lift.

Every tensor autoequivalence of \(\mathcal D\) induces a braided autoequivalence of \(Z(\mathcal D)\). Uniqueness makes the canonical central \(\operatorname{Rep}(C_5)\) stable under the given \(C_2\) action, including its coherence isomorphisms.

An equivariant central object of \(\mathcal D\) is central in \(\mathcal D^{C_2}\): use its original half-braiding with the underlying object of every equivariant object. Equivariance of its half-braiding makes this a morphism in \(\mathcal D^{C_2}\). This constructs the canonical braided embedding \(Z(\mathcal D)^{C_2}\to Z(\mathcal D^{C_2})\). On the subcategory in question the forgetful functor into \(\mathcal C\) is fully faithful, since the original central \(\operatorname{Rep}(C_5)\) already embeds fully faithfully into \(\mathcal D\).

The symmetric category \((\operatorname{Rep}(C_5))^{C_2}\) is genuinely Tannakian: compose its symmetric forgetful functor to \(\operatorname{Rep}(C_5)\) with the usual fiber functor to vector spaces. Its simple dimensions are \(1,1,2,2\), because the action is inversion on \(C_5\). Its Tannaka group has order 10 and is nonabelian, hence is \(D_{10}\).

De-equivariantize \(\mathcal C\) by this central \(\operatorname{Rep}(D_{10})\). The usual equivariantization/de-equivariantization theorem gives \(\mathcal C=\mathcal E^{D_{10}}\), with FP dimension 16 for \(\mathcal E\). The four low-dimensional simples of \(\mathcal C\) are exactly the objects over the unit orbit of \(\mathcal E\). Every other simple of \(\mathcal E\) therefore contributes to a dimension-5 simple of \(\mathcal C\). The dimension formula \(5=nrd\), with orbit size \(n\), projective representation degree \(r\), and underlying FP dimension \(d\), makes \(d\) a rational algebraic integer. It is 1 or 5; the latter is impossible in dimension 16. Also \(r=5\) is impossible for a stabilizer of order at most 10, since \(r^2\) is bounded by its order. Thus \(d=1,n=5,r=1\).

Consequently \(\mathcal E=\mathrm{Vec}_V^\omega\), where \(V\) has order 16 and the normal \(C_5\) acts freely on its 15 nonidentity elements. Its center is characteristic and nontrivial; its size \(2^j\) must satisfy \(5\mid(2^j-1)\), so \(j=4\). Thus \(V\) is abelian. The same argument for its characteristic nontrivial subgroup \(V[2]\) proves \(V=C_2^4\).

## 3. All relevant associators and tensorators are covered

Identify \(V\) with \(\mathbb F_{16}\). The rotation is multiplication by an element \(a\) of order 5. The involution is, after conjugation by a rotation, \(b(x)=x^4\). Indeed \(a\) generates the field as an \(\mathbb F_2\)-algebra, so a linear map conjugating \(a\) to \(a^{-1}=a^4\) is \(x\mapsto cx^4\). Its square being the identity gives \(c^5=1\); rotation conjugation removes \(c\).

The standard explicit presentation of \(H^3(C_2^4,\mathbb C^*)\) has 14 binary generators, of types \(x_i y_i z_i\), \(x_i y_j z_j\), and \(x_i y_j z_k\), with respectively one, two, or three distinct indices. Their restrictions to cyclic subgroups are the 14 squarefree nonconstant monomials of degrees at most 3, evaluated on \(V\setminus\{0\}\). These functions are independent and span the even-parity subspace of all 15 functions. Therefore the diagonal restrictions detect the cohomology class. The independent replay checks their rank 14.

The \(C_5\)-invariant classes are exactly the functions constant on its three orbits, whose three values sum to zero. There are four. The reference associators in normal_forms160.json have restriction patterns \(000,110,101,011\), so represent all four classes. They are strictly rotation invariant. The replay checks their cocycle equations and explicit rotation-invariant reference tensorators \(\beta_0\) for \(b\). Every \(\beta_0\) is symmetric on \(\operatorname{Fix}(b)=\mathbb F_4\).

Here is why this finite list controls **arbitrary complex actions**, not only the recorded finite phases. For one of these associators, the rotation functor's tensorator is a 2-cocycle with class \(u\in H^2(V,\mathbb C^*)\). Its fifth power is monoidally isomorphic to the identity, hence \(N(u)=0\), where \(N=1+a+\cdots+a^4\). Since this coefficient group is 2-primary, \(H^1(C_5,H^2(V,\mathbb C^*))=0\). Conjugating the action by an identity-on-objects tensor autoequivalence therefore kills \(u\). A monoidal natural isomorphism then makes the rotation tensorator trivial. One may take all rotation functors to be its strict powers. Classification of the remaining action compositors is unnecessary for the following step.

Let \(\beta\) be an arbitrary tensorator for \(b\). The monoidal natural isomorphism expressing \(ba=a^{-1}b\) says \(\beta(ax,ay)/\beta(x,y)\) is a 2-coboundary. The ratio \(\gamma=\beta/\beta_0\) is a 2-cocycle. Its commutator is an alternating bicharacter invariant under \(a\), because 2-coboundaries on an abelian group are symmetric. There is no assumption that \(\beta\) itself is invariant.

Every invariant alternating form has the form

\[
B_c(x,y)=\operatorname{Tr}_{16/2}(cxy^4),\qquad c\in\mathbb F_4.
\]

To see completeness, write any bilinear form as \(\operatorname{Tr}_{16/2}(xL(y))\), with \(L(y)=\sum_{i=0}^3c_i y^{2^i}\). Rotation invariance allows only \(i=2\), and symmetry forces \(c^4=c\). These forms are alternating because \(x^5\in\mathbb F_4\). On \(\mathbb F_4\times\mathbb F_4\), all vanish, since the absolute trace of an element of \(\mathbb F_4\) is zero. The replay also checks this independently by enumerating all 64 alternating forms.

Thus every \(\beta\) is symmetric on the fixed subfield. All reflections are rotation conjugate; strict rotation functors transport this property to their fixed spaces, and the intervening monoidal natural isomorphisms only multiply tensorators by symmetric coboundaries. Nonidentity rotations fix only zero, and normalized tensorators have value 1 there. Changes of the associator by a 2-cochain do not affect tensorator asymmetry on fixed pairs: the corresponding gauge ratio is 1 on such pairs. The argument consequently covers the initial category before the chosen normalization.

## 4. Fixed-space symmetry forces commutativity

Use the forward convention \(J_h(x,y):F_h(x)\otimes F_h(y)\to F_h(x+y)\). For equivariant objects \(X,Y\), the trace of \(h\) on their tensor product's \(h\)-fixed grade \(z\) is

\[
\sum_{\substack{x+y=z\\ hx=x,\;hy=y}}
J_h(x,y)^{-1}\,\chi_X(h,x)\chi_Y(h,y).
\]

Nonfixed pairs contribute zero trace because \(h\) permutes the corresponding direct summands. The expression is symmetric in \(X,Y\) by the established symmetry of \(J_h\) on fixed pairs. Projective stabilizer characters determine the representations on every orbit and hence determine the equivariant object. Therefore \(X\otimes Y\cong Y\otimes X\) at the level of objects and the Grothendieck ring is commutative. This contradicts both original input witnesses and proves the exclusions.

## Primary references checked

1. P. Etingof, D. Nikshych, V. Ostrik, *Weakly group-theoretical and solvable fusion categories*, [arXiv:0809.3031](https://arxiv.org/abs/0809.3031), Theorem 1.6, Proposition 4.4, and Sections 2.6, 2.11. Proposition 4.5 is a closure statement; the actual extension/equivariantization chain is 4.4.
2. H.-L. Huang, Z. Wan, Y. Ye, *Explicit cocycle formulas on finite abelian groups with applications to braided linear Gr-categories and Dijkgraaf-Witten invariants*, [arXiv:1703.03266](https://arxiv.org/abs/1703.03266), Section 3.2, formula (3.1), and the complete-representatives statement.
3. S. Burciu, S. Natale, *Fusion rules of equivariantizations of fusion categories*, [arXiv:1206.6625](https://arxiv.org/abs/1206.6625), for the orbit/projective-stabilizer parametrization and dimension formula.

The central embedding and fixed-space commutativity argument above have also been checked directly, so no unproved general action-lifting theorem or exhaustive classification of \(D_{10}\) compositors is being invoked.
