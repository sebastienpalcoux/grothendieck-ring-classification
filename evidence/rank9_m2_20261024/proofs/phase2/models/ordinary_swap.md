# Ordinary swap of the equal half-E6 fermionic product

Let E be the unitary half-E6 category, with simples 1,f,x and x²=1+f+2x,
central fermion f, and d=dim(x)=1+sqrt(3). Its existence and central-fermion
local data are the published input Aasen–Lake–Walker, arXiv:1709.01941v2,
Sections 7.1–7.2 (the same input as the established project diagonal-fermion theorem).
Use the same choice in both factors.

In E⊠E, b=f⊠f is a central boson. Set A=1+b and Q=(E⊠E)_A.
The established equal-rotation fixed-point calculation gives the six simples
(1,g,a,a',u,v), where u*=v, g fixes a,a' and interchanges u,v, and

- a²=1+g+2a; (a')²=1+g+2a'; aa'=u+v;
- au=a'+u+v=av; a'u=a+u+v=a'v;
- u²=v²=g+a+a'+u+v; uv=1+a+a'+u+v.

The source constructor `fermionic_products.fusion_tensor(2,2)` replays these rules
from that categorical theorem. The dimensions are 1,1,d,d,d²/2,d²/2.

Let S be the ordinary factor swap, and equip A with the identity algebra
isomorphism S(A)→A, on both summands. This gives a coherent unitary C2 action T
on Q. It fixes 1,g,u,v and interchanges a,a'. Indeed, the actions on x⊠x are
±(t⊠t), with t:x⊗f→x normalized to square one, and the ordinary swap preserves
each of these; it does not change the sign of the A-action.

Consequently C=Q^{C2} has four invertibles, four simples over u,v and one simple
X over a+a'. Put epsilon for the nontrivial character of C2.

The four invertibles form C4, as an explicit calculation shows. In the pointed
part sVec⊠sVec write e0,e1 for the two homogeneous components of gA in degrees
(f,1),(1,f). Choose the swap equivariance e0↔e1. It squares to the identity.
An isomorphism μ:g⊗_A g→A has coefficients

μ00=1, μ01=b, μ10=-b, μ11=-1.

The signs come from balancing with the specified central fermion. On all four
pairs, simultaneous exchange of e0,e1 sends μ to -μ. Hence this equivariant
lift t of g satisfies t²=epsilon, and t has order four. The scalar equalities
are replayed in `ordinary_swap.py`.

The central objects z1=f⊠1 and z2=1⊠f centralize A: their monodromy with b
is the product of two fermionic minus signs. Thus their free A-modules have
descended half-braidings with every A-module. In this central local-module
construction z2=z1*b and bA is the unit, so z1*A and z2*A are isomorphic
as central objects of Q. Their underlying object is the simple invertible g.
Its module-isomorphism space is one-dimensional; every nonzero module
isomorphism is therefore a scalar multiple of a central one and is central.
In particular the map exchanging e0,e1 is central and has square one. It
gives g a coherent equivariant central structure. The central functor from
equivariant central objects of Q to Z(Q^{C2}) consequently supplies a central
lift of t. Hence t commutes with every class in K0(C).

The action of t on the four simples over u,v is transitive: t exchanges the
underlying u and v, while t²=epsilon exchanges their two equivariant structures.
Choose one of them Y; all four are t^jY, j∈Z/4. Also tX=X.
Write G=sum_{j=0}^3 t^j and V=sum_{j=0}^3 t^jY.
The forgetful functor and invariance under epsilon give, with no choices,

X²=G+2X+V,  XY=YX=X+V.

For example, forgetting XY gives a+a'+2u+2v. Epsilon fixes X, so the
coefficients of the two equivariant lifts of each u and v must be equal.

The same forgetful functor gives

Y²=t^a+X+(t^b+t^c)Y,

where a,c are odd and b is even. The invertible constituent is unique by
rigidity; u² has underlying invertible g. Frobenius reciprocity requires
{b,c}={a-b,a-c}, so b+c=a modulo four. The four possibilities are all carried
to one another by replacing Y by t^rY. Choose a=1,b=2,c=3, obtaining

Y²=t+X+(t²+t³)Y.

These identities determine all 729 structure constants, independent of any
census input. They match R9_2_1983 exactly, with source-to-model basis permutation
[0,1,3,5,8,7,6,4,2]. `ordinary_swap.py` verifies the fusion axioms, all 486
forgetful tensor identities, and the full tensor match. Every categorical
operation is unitary, so this is a unitary model.
