# R11_1_179: a coherent order-three action on an existing near-group model

Let D be any of Izumi's three unitary near-group categories on Q8 with fusion
rules gρ=ρg=ρ and ρ²=sum_(g∈Q8)g+2ρ. These existing categories have dimension
24 and simple dimensions 1^8,4. Their categorical existence is Izumi,
*A Cuntz algebra approach to the classification of near-group categories*,
arXiv:1512.04288v2, Theorems 1.1 and 6.1 and the explicit tuple in Lemma 6.13.
The primary PDF https://arxiv.org/pdf/1512.04288 was checked directly on
23 October 2026. The prior project proof
`work/resolve_rank9_neargroup/NG_ACTIONS.tex` describes the applicable normalized
functor construction, from Remark 3.6, Definition 4.8 and Theorem 4.9.

Use quaternionic matrices I=diag(i,-i), J=[[0,1],[-1,0]], K=IJ, and the
antiunitary j=J composed with complex conjugation. The categorical data have
j1=j, j2=−ζj for a cube root ζ and l=0. Put

    W = −(1+I+J+K)/2.

This is a unitary SU(2) matrix, commutes with j, satisfies W³=1 and has trace −1.
Conjugation by W cyclically permutes I,J,K. Therefore it intertwines the
faithful two-dimensional representation π of Q8 with the group automorphism
φ cycling i,j,k. The normalized Izumi construction gives a genuine tensor
autoequivalence γ, with

    γ(S_g)=S_(φ(g)),        γ(T(v))=T(Wv).

It preserves all defining categorical data, including j2 for every ζ. Since
π(φ(g))=Wπ(g)W*, the commutator bicharacter χ is preserved as well, and l=0
has no remaining compatibility condition. Thus the Cuntz endomorphism
reconstruction formulas are covariant: the sum of S_g and the contraction
sum_i T_i j(T_i) are invariant, and the formula for ρ(T) is preserved by the
intertwining and antiunitary equations. Hence γ conjugates the pointed
endomorphisms by φ and commutes with ρ. Restriction to the tensor category
they generate gives the stated tensor functor; no result from Section 13,
which is specialized to irrational near-group categories, is required.
Since
φ³=1 and W³=1, its cube is the identity on the generating morphisms and hence
on the reconstructed category. Thus the identity compositors give an actual
coherent C3 action. This is stronger than merely prescribing an order-three
permutation of the fusion ring.

The unitary equivariantization C=D^(C3) has dimension 72. There are two fixed
invertibles 1,−1, each with three equivariant structures, producing six
invertibles. The two free orbits {i,j,k} and {−i,−j,−k} produce two objects of
dimension three. The fixed object ρ has three equivariant lifts P_a, a∈Z/3,
each of dimension four. Hence its rank is 11 and its dimension multiset is
1^6,3^2,4^3.

Write L_(g,a) for the lift of a fixed invertible, and U,V for the two free
orbit objects. The pointed part is computed by equivariant homogeneous fibres:
for a free output, count ordered pairs multiplying to a representative; for a
fixed output, project onto the specified C3 character. A free three-cycle
contributes each character once. The remaining products are

    L_(g,a) P_b = P_b L_(g,a) = P_(a+b),
    U P_b = P_b U = V P_b = P_b V = P_0+P_1+P_2,
    P_a P_b = L_(1,a+b)+L_(-1,a+b)+U+V+P_(a+b+1)+P_(a+b+2).

The last two terms follow because W has eigencharacters ζ3 and ζ3² on
Hom(ρ,ρ²): W³=1 and trace W=−1 determine them. The fixed pointed outputs
follow from γ(S_1)=S_1 and γ(S_(-1))=S_(-1). The three lifts have duality
P_a*=P_(-a), so exactly one is self-dual.

`construct.py` checks the exact Gaussian-integer equations for 2W, constructs
all products, verifies fusion axioms, and matches every one of the 1331 input
coefficients. With model labels

    (1,0),(1,1),(1,2),(-1,0),(-1,1),(-1,2),U,V,P0,P1,P2

the model-to-input basis bijection is

    [0,7,8,9,1,2,5,6,10,4,3].

The source tensor hash is recorded in `model.json`. No enumeration of
associators is claimed: this supplies a unitary realization, and all three
existing cube-root choices give this same based tensor.

The separate `verify.py` does not import the constructor. It independently
recovers all multiplicities by the character formula
dim Hom_C3(U,V)=(1/3)sum_(t=0)^2 Tr(t on Hom(U,V)), on the complete
underlying near-group fusion spaces. For Hom(ρ,ρ²) the character is (2,−1,−1);
all other fusion spaces are the one-dimensional absorption or S_g spaces.
It also checks all 14641 associativity identities, the action matrix, the
source hash, and the entire tensor match. Run

    python -O work/rank11/nonintegral/integral179/verify.py
