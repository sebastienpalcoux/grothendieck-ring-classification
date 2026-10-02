# A dimension-96 obstruction: R7_2_252 and R7_2_315

Both rings admit no fusion categorification over C. The proof is independent
of pivotality, braiding, positivity or a choice of associator.

## 1. The ring premises and first equivariantization

Each ring has dimension 96, simple dimensions 1,1,2,3,3,6,6, invertible
group C2, and trivial universal grading. Write h for its nontrivial
invertible, E for the dimension-two simple, P,Q for the dimension-three
simples, and W,V for the dimension-six simples. Multiplication by h fixes
E,W,V and exchanges P,Q. These statements, the positive dimension
character and generation of the whole ring by the adjoint subring are
checked directly against the full census tensors in the accompanying
certificate.

Suppose C categorifies either ring. By ENO Theorem 1.6, dimension
96 = 2^5*3 makes C solvable. The last prime step in its solvable construction
cannot be a faithful extension, because its universal grading is trivial.
It is an equivariantization C = D^{Cp}. The embedding Rep(Cp) into C and
the invertible group C2 force p=2. For this C2 equivariantization, an
h-fixed simple comes from a free orbit and forgets to two distinct simples
of half its dimension; two simples exchanged by h forget to the same fixed
simple. Thus D has dimension 48 and type

    1^3 3^5.

This uses the usual projective orbit/stabilizer formula; all projective
representations of a cyclic stabilizer over C are one-dimensional.

## 2. A second equivariantization is forced to be pointed

D has no nontrivial universal grading. Indeed, its grading group has order
dividing 48 and hence is solvable. Any nontrivial such group has a prime
cyclic quotient of order 2 or 3. In a C2 grading all three invertibles are
neutral, and the neutral dimension would be 24 = 3 + 9n, impossible. In a
C3 grading the invertible group C3 either lies in the neutral component or
maps isomorphically onto the grading group. The neutral dimension would
then be 16 = 3 + 9n or 16 = 1 + 9n, also impossible. Here n counts the
dimension-three simples in the neutral component.

Solvability therefore forces D = E^{C3}, with FPdim(E)=16; its three
invertibles exclude any other prime at this step. The three characters of
C3 already account for all invertibles of D. Every remaining simple of D
has dimension three. Such a simple arises either from a free orbit of
three invertibles of E or from a fixed dimension-three simple of E; each
fixed dimension-three simple yields three simples in D. Consequently E
has one of the following types:

    1^16, or 1^7 3.

The second type is impossible: its seven invertibles would form a pointed
subcategory of dimension seven, which cannot divide dimension sixteen.
Equivalently, if X were its unique dimension-three simple, all seven
invertibles would fix X; thus X X* would contain all seven once and its
remaining dimension two could not be an integer multiple of dim(X)=3.
Therefore E = Vec_H^omega for a group H of order sixteen.

The canonical central Rep(C3) in D is uniquely determined by its underlying
invertible subgroup. The kernel of Inv(Z(D)) -> Inv(D) is
Aut_tensor(Id_D), which is trivial because U(D)=1. Hence the outer C2
action preserves this central Tannakian subcategory. Equivariantization
and de-equivariantization in stages give

    C = (Vec_H^omega)^G,    1 -> C3 -> G -> C2 -> 1.

The central Rep(G) embeds fully faithfully in C. A group of order six is C6 or
S3. The former would contribute six invertibles, whereas C has only two.
Thus G=S3. This argument retains all possible categorical action coherence
and all possible omega; it does not assume a strict action.

## 3. The required orbit pattern

In the S3 equivariantization of Vec_H^omega, the identity orbit contributes
the three ordinary representations of S3, of dimensions 1,1,2. These
already account for all simples of those dimensions in C.

A further orbit of size one would have a projective stabilizer S3. Every
irreducible projective representation has degree at most sqrt(6), hence
degree one or two, and would supply a forbidden additional small simple.
An orbit of size two has cyclic stabilizer C3 and supplies dimension-two
simples, also impossible. An orbit of size three has stabilizer C2 and
supplies exactly two dimension-three simples. A free orbit supplies one
dimension-six simple. The census dimensions therefore force the complete
action orbit pattern on H to be

    [1,3,6,6].

The normal C3 subgroup acts freely on every nonidentity element, so its
automorphism is fixed-point-free. A transposition fixes exactly two
elements of H: the identity and one point of the unique orbit of size
three. We now show these two requirements are incompatible for every
group H of order sixteen.

## 4. An elementary order-sixteen obstruction

Let alpha be a fixed-point-free automorphism of order three on H. Every
alpha-stable subgroup has order congruent to one modulo three. In
particular, |Z(H)| is 4 or 16. If |Z(H)|=4, then Z(H)=V4, since C4 has
no fixed-point-free automorphism of order three. The quotient H/Z(H)
cannot be cyclic, for then H would be abelian. Thus it is V4, and the
commutator gives an alpha-equivariant alternating map

    wedge^2(V4) -> Z(H)=V4.

The source is one-dimensional over F2 and has trivial alpha action. The
target has no nonzero alpha-invariants. The commutator map is therefore
zero, contradicting noncommutativity. Hence H is abelian.

Among the five abelian groups of order sixteen, C16 has no order-three
automorphism, C8 x C2 has characteristic subgroup 2H=C4, and C4 x C2^2
has characteristic subgroup 2H=C2. The latter two cannot support a
fixed-point-free order-three action on that subgroup. Consequently

    H = C4^2 or C2^4.

Every involution of either remaining group fixes at least four elements.
For C2^4, write its matrix S over F2. Since (S-I)^2=0, rank(S-I)<=2,
so dim ker(S-I)>=2.

For C4^2, reduce S modulo two. If the reduction is the identity, S fixes
the four elements of 2H. Otherwise the nontrivial involution over F2 is
conjugate to [[1,1],[0,1]]. Lift this basis change modulo four and write
S=[[a,b],[c,d]], with a,b,d odd and c even. From S^2=I one obtains
bc=0 and b(a+d)=0 modulo four, hence c=0 and d=-a. For every x in Z/4,
the first fixed-point equation has the unique solution

    y = -b^{-1}(a-1)x.

The second equation holds automatically because
(-a-1)(a-1)=1-a^2=0 modulo four. Thus S has exactly four fixed points in
this case as well.

This contradicts the two fixed points required by [1,3,6,6], and completes
the general exclusion of both census rings.

## Source scope and exact certificate

The only structural fusion-category inputs are ENO arXiv:0809.3031,
Theorem 1.6 and the prime extension/equivariantization characterization
of solvability; equivariantization/de-equivariantization in stages
(DGNO arXiv:0906.0620, Theorem 4.18 and Proposition 4.19); and the
projective orbit/stabilizer description of equivariant simple objects
(Burciu--Natale arXiv:1206.6625). The remaining group argument is proved
above. No classification of order-sixteen associators or model-specific
equivariance choices is used.

`verify_d96_premises.py` binds both tensors to the raw census, checks every
dimension equation, duality, the invertible action, and generation by the
adjoint subring. `d96_premise_certificates.json` retains the full tensors
and source hashes. An independent certificate from the criteria audit
also checks the finite involution claims.
