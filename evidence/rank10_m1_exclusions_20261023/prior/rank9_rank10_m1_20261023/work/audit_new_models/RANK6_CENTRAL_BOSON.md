# Dimension-24 rank-six branch: the unique central boson

This note proves the categorical step that reduces the dimension-24
quotient profile \(1^4,2,4\) to the already classified near-group branch.
It does **not** assert that the rank-six profile is uncategorifiable.

The exact independent replay is verify_rank6_central_boson.py, with receipt
rank6_central_boson_audit.json. It uses only the Python standard library,
enumerates all relevant finite orthogonal matrices, and checks all sign
quotient profiles directly against the original rank-nine tensors.

## The dimension-12 classification input

Let \(\mathcal B\) have the rank-six fusion rules
\[
|G(\mathcal B)|=4,\quad
m^2=\sum_{g\in G(\mathcal B)}g,\quad mn=nm=2n,\quad
n^2=\sum_{g\in G(\mathcal B)}g+2m+2n,
\]
with dimensions \(1,2,4\) on the three indicated types. The group of
invertibles may initially be either \(C_4\) or \(V_4\); the proof does
not assume one. The remaining displayed products are forced by dimensions
and Frobenius reciprocity because \(m\) and \(n\) are the unique simples
of their respective dimensions.

Its universal grading is trivial. By solvability in dimension
\(24=2^3\cdot3\), the last step in a prime cyclic solvable sequence is an
equivariantization, and the group must be \(C_2\) because its character
group embeds in the order-four group \(G(\mathcal B)\). Thus
\(\mathcal B=\mathcal E^{C_2}\), with \(\dim\mathcal E=12\).
The orbit/stabilizer dimension formula forces profile \(1^4,2^2\)
for \(\mathcal E\): the four-dimensional object must restrict to an orbit
of two two-dimensional simples, the two-dimensional object must restrict
to an orbit of two invertibles, and the four invertibles come from two
fixed invertibles. The action therefore transposes the two
two-dimensional simples and two of the four invertibles.

Here is an exhaustive reduction of its fusion rules, requiring no
classification of small fusion rings. Write \(G=G(\mathcal E)\), of
order four, and \(X,Y\) for the two-dimensional simples. The given
involution exchanges \(X,Y\).

If the left \(G\) action on \(\{X,Y\}\) were transitive, its stabilizer
\(H\) would have order two. Frobenius reciprocity and dimensions would give
\[
XX^*=\sum_{h\in H}h+Z
\]
for one of \(Z=X,Y\). This object is self-dual, so \(Z\) is self-dual;
duality then fixes both \(X\) and \(Y\). Left and right stabilizers coincide
by duality. For \(g\notin H\) one has \(Y=gX=Xg\), and \(g^2\in H\).
Consequently
\[
Y^2=g^2X^2=X^2=\sum_{h\in H}h+Z.
\]
An automorphism exchanging \(X,Y\) must preserve their common stabilizer
\(H\) but exchange \(Z\) with the other two-dimensional simple.
It cannot preserve their common square. This is a contradiction.

Thus every invertible fixes both \(X,Y\) on the left, and by duality
on the right as well. It follows that \(XX^*=YY^*=\sum_G g\).
The two objects cannot both be self-dual: writing
\(XY=aX+(2-a)Y\), associativity of \(X^2Y=X(XY)\) forces \(a=0\),
and then associativity of \(XY^2=(XY)Y\) would give
\(4X=2\sum_G g\), an impossibility. Therefore \(X^*=Y\).
Now \(XY=YX=\sum_Gg\), and writing
\(X^2=aX+(2-a)Y\), associativity of \(X^2Y=X(XY)\) forces \(a=0\).
Hence
\[
X^2=2Y,\qquad Y^2=2X,\qquad XY=\sum_{g\in G}g.
\]
This is the faithful \(C_3\) grading with pointed neutral category
\(\operatorname{Vec}_G^\omega\) and rank-one nonneutral components.
A rank-one module category over \(\operatorname{Vec}_G^\omega\) supplies
a two-cochain trivializing \(\omega\), so the neutral associator can be
taken trivial.

The group \(G\) is either \(C_4\) or \(V_4\). The former is impossible.
Indeed
\(\operatorname{BrPic}(\operatorname{Vec}_{C_4})\) is the isometry group
of \(\mathbf Z_4^2\) with quadratic form \(q(x,y)=xy\bmod4\).
Every primitive isotropic vector lies on one of the two coordinate axes.
An invertible isometry therefore is diagonal or antidiagonal, with
opposite-axis entries inverse to each other. There are exactly four such
isometries, and hence no element of order three. A trivial
Brauer--Picard homomorphism would make a nonneutral component regular,
of rank four, whereas its rank is one. This excludes \(C_4\).
The independent replay also enumerates all these isometries.

We conclude that \(G=V_4\). Jordan--Larson classify all categorifications
of these rules as their six \(R_{3,V_4}\) categories: two \(C_3\)-extension
types of \(\operatorname{Vec}(V_4)\), each with three scalar associator
twists. Thus all possible \(\mathcal E\), including the nongroup-theoretical
ones, are included in the center argument below.

Write \(\mathcal D=\operatorname{Vec}(V_4)\) for the neutral subcategory.
The two nonneutral \(C_3\) components have one simple object each,
of dimension two. Their products with their duals are
\(\sum_{a\in V_4}a\).

## Exact finite classification data

The braided pointed center of \(\mathcal D\) has invertible group
\[
A=V_4\oplus V_4^*\simeq\mathbf F_2^4,\qquad
q(a,\chi)=\chi(a).
\]
Its positive ribbon twist is \((-1)^{q(a,\chi)}\).
The Brauer--Picard group is \(O^+(4,2)\), of order \(72\).
The parabolic subgroup preserving \(V_4^*\) has order \(12\) and represents
tensor autoequivalences of \(\mathcal D\).

The relevant extension matrices \(M\) have order three and an invertible
upper-right \(2\)-by-\(2\) block. There are exactly six. Modulo parabolic
conjugation and inversion, they form two orbits of sizes four and two.
Using row-bit notation, representatives are
\[
M_1=(4,12,15,6),\qquad M_2=(8,4,6,9).
\]
Their fixed vectors are respectively
\[
A^{M_1}=\{0,7,10,13\},\qquad A^{M_2}=\{0\}.
\]
Crucially,
\[
q(7)=q(10)=q(13)=1.
\]
Thus for **every** allowed triality, the only isotropic fixed vector is
zero. This assertion is invariant under every orthogonal change of basis.

The replay constructs orthogonal matrices by their four basis images,
independently of the discovery program's row enumeration. It verifies
the full group order, parabolic order, all six matrices, their two orbits,
and the absence of nonzero isotropic fixed vectors for every one of them.
For completeness it also lists the three involutive parabolic normalizers
in each class which invert triality and transpose the nonidentity neutral
invertibles. The central argument needs only the triality fixed spaces.

## Center restriction lemma

Form the crossed product
\[
\mathcal K=\mathcal E\rtimes C_2.
\]
It is faithfully graded by
\(C_3\rtimes C_2=S_3\), with neutral category \(\mathcal D\).
Every adjoint product of a homogeneous simple object belongs to
\(\mathcal D\), while the product of the dimension-two triality simple
with its dual contains every invertible of \(\mathcal D\). Hence
\[
\mathcal K_{\mathrm{ad}}=\mathcal D,\qquad U(\mathcal K)=S_3.
\]

Consider an invertible object \(Z\) of \(\mathcal Z(\mathcal K)\).
Its underlying simple object is homogeneous, of some degree \(g\in S_3\).
The half-braiding with each nonzero homogeneous component forces
\(gh=hg\) for every \(h\in S_3\). Since \(Z(S_3)=1\), the degree is neutral.
We may therefore restrict its half-braiding to \(\mathcal D\), obtaining
\[
\operatorname{res}(Z)\in\operatorname{Inv}\mathcal Z(\mathcal D)=A.
\]
Compatibility with the half-braiding on the triality component makes
this class triality invariant. This is equivalently the canonical
Brauer--Picard action on the center in the relative-center description
of a graded category.

The canonical positive ribbon twist of \(Z\) is computed using its
underlying neutral object and that restricted half-braiding. It equals
\((-1)^{q(\operatorname{res}(Z))}\).
Every possible nonzero restriction is therefore fermionic, by the
fixed-space calculation above. In particular every boson has trivial
restriction.

The kernel of restriction is exactly
\[
\operatorname{Hom}(U(\mathcal K),\mathbf C^*)
=\operatorname{Hom}(S_3,\mathbf C^*)=C_2.
\]
Indeed, trivial restriction means that the underlying object is the
tensor unit and its half-braiding on the neutral category is trivial.
Half-braidings on the tensor unit are tensor automorphisms of the
identity, hence characters of the universal grading. Conversely both
characters of \(S_3\) give such objects. Both are bosonic, since their
underlying object is the unit.

Consequently \(\mathcal Z(\mathcal K)\) has **exactly one nontrivial
invertible boson**, the sign character of \(S_3\).
No surjectivity assertion for the restriction map is required.
Possible obstructions to lifting fermionic fixed vectors have no effect
on the argument.

## Transport to the rank-six category and another equivariantization

The crossed product \(\mathcal K\) and equivariantization \(\mathcal B\)
are categorically Morita equivalent. Their centers are braided equivalent.
All categories here are integral and therefore pseudo-unitary; the
canonical positive ribbon structures are preserved by this equivalence.
It follows that \(\mathcal Z(\mathcal B)\) also has a unique nontrivial
invertible boson. It is the canonical central sign of
\(\mathcal B=\mathcal E^{C_2}\), whose forgetful object is nontrivial.

Suppose now that a dimension-48 category \(\mathcal C\) in the target
family has this rank-six quotient:
\(\mathcal C=\mathcal B^{C_2}\).
Its action must preserve the unique central boson. It therefore preserves
the central Tannakian subcategory \(\operatorname{Rep}(C_2)\).
Equivariantizing this invariant central subcategory gives a central
Tannakian subcategory of \(\mathcal C\) of dimension four.

Here the equivariantization is a symmetric fusion category with four
invertible simples. It has an ordinary symmetric fiber functor by
forgetting equivariance to \(\operatorname{Rep}(C_2)\) and then to vector
spaces. Thus it is \(\operatorname{Rep}(H)\) for a group \(H\) of order four.
The forgetful functor from this central subcategory to \(\mathcal C\)
is fully faithful: the original central \(\operatorname{Rep}(C_2)\)
had fully faithful forgetful functor to \(\mathcal B\), and equivariance
imposes the same morphism condition on both sides. Its four invertible
objects therefore embed as all of \(G(\mathcal C)=V_4\).
This excludes \(H=C_4\) and gives \(H=V_4\).

In particular **each of the three nontrivial invertibles of
\(\mathcal C\) admits a central Tannakian lift**. One may now choose
the sign whose quotient has the near-group profile \(1^8,4\).
The original source-basis checks give:

| Input | Rank-six quotient sign | Triality quotient sign | Near-group quotient sign |
|---|---:|---:|---:|
| R9_1_12 | 1 | 2 | 7 |
| R9_1_62 | 6 | 7 | 5 |
| R9_1_87 | 4 | 3 | 5 |
| R9_1_108 | 7 | 6 | 5 |

All indices are zero-based original basis IDs, with unit \(0\).
The replay derives these profiles from the actual multiplication
permutations and the \(C_2\) equivariantization dimension formula.
It does not identify a quotient from dimension alone.

For R9_1_62 and R9_1_87, the independently completed near-group branch
exclusion now applies to the central sign with original basis ID \(5\).
This removes their rank-six quotient branch without claiming the
rank-six category itself is impossible.

## References and logical scope

The extension classification input is Jordan--Larson,
On the classification of certain fusion categories, arXiv:0812.1603,
Theorem 1.4 and Proposition 3.1. The two representatives and all scalar
twists must be retained; assuming all dimension-12 categories are
group-theoretical would omit half the classification.

Solvability in dimensions \(p^a q^b\) and the existence of a prime
cyclic solvable sequence are Etingof--Nikshych--Ostrik,
Weakly group-theoretical and solvable fusion categories,
arXiv:0809.3031, Theorem 1.6 and Proposition 4.4.
The central restriction uses the relative-center construction of
Gelaki--Naidu--Nikshych, Centers of graded fusion categories,
arXiv:0905.3117.

The center lemma has been independently audited by the
integral-obstructions agent. The finite matrix calculation and original
sign profiles have been independently replayed here. The only remaining reference to the parent package is the completed
near-group exclusion for the alternative quotient.
