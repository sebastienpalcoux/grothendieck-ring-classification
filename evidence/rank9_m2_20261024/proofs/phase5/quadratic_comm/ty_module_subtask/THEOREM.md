# The TY subcategory forces a rank-twelve D8 Morita reduction

## Result and scope

For each of R9_2_137, R9_2_1607 and R9_2_1976, every hypothetical complex fusion categorification C has an integral subcategory

D = TY(V4, chi, tau),

where chi is the **nonalternating** nondegenerate symmetric bicharacter, and tau is one of ±1/2. There is a source-determined involution g such that A=1+g is a connected separable algebra, and the Morita dual C_A^* has exactly eight invertibles forming the dihedral group D8 of order eight and four further simple objects, all of dimension d=4+3sqrt(2). These four objects are one D8-orbit, with stabilizer Z(D8)=C2.

This is a uniform necessary categorical reduction. It is not a construction of C or its dual, and it does not exclude any of the three rings. No unitarity, pivotality, or pseudo-unitarity hypothesis is needed.

## 1. The two different stabilizers determine the bicharacter

Let G=Inv(D)=V4 and let Y be the dimension-two simple in D. The based ring of D has Y²=sum_{a in G}a and aY=Y=Ya. The Tambara–Yamagami classification therefore applies to D over C and identifies it with TY(G,chi,tau). In particular its pointed associator is trivializable.

The four dimension-d simples span an indecomposable left D-module category M. Under G they form two orbits of size two, with distinct stabilizers H1={1,h1} and H2={1,h2}. Multiplication by Y sends a simple in either orbit to the sum of the two simples in the other orbit. These facts are exact source-tensor identities.

Choose X in the first orbit. Its internal endomorphism algebra in D has underlying object 1+h1, since its multiplicity at a simple a of D is [aX:X]. This internal endomorphism algebra is connected and separable. Its multiplication is the usual subgroup algebra up to gauge: H²(C2,C*)=0. Thus

M is equivalent to Mod_D(C[H1]).

The TY module calculation says that the two pointed-subcategory components of this induced module category have stabilizers H1 and H1-perp, respectively. In the present special case it is immediate from the usual TY associator: on the Y-supported right C[H1]-modules, tensoring on the left by a in G multiplies the right H1-character by chi(a,-). Hence its stabilizer is H1-perp. This is also Meir–Musicantov, Lemma 9.1 (Lemma 27 in the separately numbered appended version), with trivial subgroup cocycle.

It follows that H2=H1-perp. Since H1 and H2 are distinct lines in V4,

chi(h1,h1)=chi(h2,h2)=-1,   chi(h1,h2)=1.

Therefore chi is the nonalternating form. The remaining involution

g=h1h2

is its unique nonidentity isotropic element: chi(g,g)=1. Its subgroup L={1,g} is Lagrangian, L=L-perp. The element g acts freely on all four nonintegral simples and fixes Y.

There is no condition on the sign of tau from this argument. The module category is induced from the pointed subcategory and exists for either sign. In particular, one must not identify D with Rep(D8) or Rep(Q8) merely from its five-object based ring.

## 2. The correct algebra for the pointed dual

The internal-end algebra 1+h1 used in the preceding paragraph is **not** the algebra giving the pointed dual. Its generator is anisotropic. For the pointed dual one must use A=C[L]=1+g, where g is the unique isotropic involution determined above. This algebra exists in D because the entire pointed subcategory has trivial associator.

Consider D'=Bimod_D(A). Its simples can be described directly.

- In the G-supported sector there are four simples, indexed by (aL,lambda) in G/L × L-hat. Their underlying objects have dimension two, so their D'-dimensions are one.
- In the Y-supported sector the left and right actions of g commute, since chi(g,g)=1. There are four scalar choices for the two actions, giving four more simples. Their underlying object is Y of dimension two, so these D'-dimensions are also one.

Thus D' is pointed of dimension eight. This can also be read from the Lagrangian-subgroup criterion, but the explicit bimodule description identifies its group.

The four G-supported invertibles form

E = G/L × L-hat = C2 × C2.

Choose the Y-supported invertible s with both A-actions trivial. The TY bimodule product calculation gives s²=1. Conjugation by s swaps the two coordinates of E, after identifying G/L with L-hat through aL↦chi(a,-)|L. This pairing is nondegenerate because L=L-perp. Consequently

Inv(D') = (C2 × C2) semidirect C2,

with the last factor interchanging the two generators. This is D8, not Q8 and not C2³. Explicitly it has presentation

p²=q²=s²=1,  pq=qp,  sps=q.

The eight element orders are 1,2,2,2,2,2,4,4. Its center is {1,pq}.

The formulas are the specialization H=L, psi=1, H-perp=H, t_h=1, nu=1 of Meir–Musicantov, Sections 9.3–9.5. The sign tau affects the associator of the pointed dual; it does not change this based group. No claim that this pointed category has trivial associator is made.

## 3. The full Morita dual has exactly twelve simples

Now form C'=Bimod_C(A). The D-supported part is the eight-object pointed category D' just described.

On the remaining part, the free action of g partitions the four dimension-d simples into two orbits. Each orbit supports a unique simple right A-module, with underlying object X+gX, of total C-dimension 2d. Left multiplication by g preserves each such right-module isomorphism class. To add a compatible left A-action is to choose a projective equivariant structure for this C2 stabilizer. Since H²(C2,C*)=0, there are precisely two choices for each orbit. Therefore this part gives four simple A-bimodules, each of C'-dimension

(2d)/FPdim(A)=d.

Hence C' has dimension type (1^8,d^4) and rank twelve. The total dimension checks as

8+4d² = 144+96sqrt(2) = FPdim(C).

The eight invertibles above are all of Inv(C'), since d>1. Their action on the four noninvertibles is transitive: if X and Y belonged to different invertible orbits, YX* would have no invertible constituent, and its dimension equation would give d²=n d for an integer n, contradicting the irrationality of d. This is also Schopieray, Lemma 2.6.

The stabilizer has order 8/4=2. For a fusion ring with a single noninvertible orbit the stabilizer is normal (Schopieray, Lemma 2.8). The only normal order-two subgroup of D8 is its center, so the stabilizer is Z(D8). In particular, for any noninvertible X in C',

XX* = 1+z + sum_q m_q X_q,

where z is the nontrivial central involution and the four nonnegative integers m_q sum to eight, since d²=2+8d.

This gives a common D8-quadratic categorical frontier for all three commutative source rings. Additional constraints from the module action, duality, and associativity are needed to determine the possible m_q and the left/right quotient action. Such necessary fusion rings still need categorifications or complete categorical exclusions.

## 4. Source labels and exact certificate

All indices are zero-based.

| Source ring | Y | First orbit | h1 | Second orbit | h2 | Isotropic/free g |
|---|---:|---|---:|---|---:|---:|
| R9_2_137 | 8 | {3,6} | 7 | {4,5} | 2 | 1 |
| R9_2_1607 | 3 | {1,2} | 4 | {7,8} | 6 | 5 |
| R9_2_1976 | 5 | {1,2} | 6 | {3,4} | 7 | 8 |

`verify_structure.py` checks the original tensors, every one of the 243 dimension equations, the TY fusion subcategory, the indecomposable module graph, both internal-end supports, the stabilizers and free g-action. It verifies the forced bicharacter and constructs the eight-element semidirect-product table. The result is `structure_certificate.json`.

## References

- D. Tambara and S. Yamagami, *Tensor categories with fusion rules of self-duality for finite abelian groups*, J. Algebra 209 (1998), 692–707, https://doi.org/10.1006/jabr.1998.7558. The classification is over an algebraically closed field of characteristic zero; no unitarity assumption enters.
- E. Meir and E. Musicantov, *Module categories over graded fusion categories*, Section 9, https://arxiv.org/pdf/1010.4333. Lemma 9.1 gives the perpendicular stabilizer; Sections 9.3–9.5 identify the group of invertible subgroup-algebra bimodules and its conjugation action. The available PDF includes two differently numbered versions; the corresponding later numbering is Lemma 27 and Sections 9.2–9.4.
- A. Schopieray, *Categorification of integral group rings extended by one dimension*, Lemmas 2.6 and 2.8, https://arxiv.org/pdf/2208.07319. These are based-ring structural facts and do not require a pivotal or unitary category.
