# A unitary model for R8_2_868

Let d=(7+sqrt(53))/2, so d²=1+7d. The ring is the Q-dual even part of the unitary Haagerup–Izumi C7 subfactor.

Evans–Gannon, arXiv1006.1326, Theorem5(d), constructs the unitary C7 subfactor and identifies its center modular data. Both even parts of the actual finite-depth C*-subfactor are unitary fusion categories. Izumi, arXiv1609.07604, Proposition7.4 and Theorem7.5, determines all simple objects of the dual of the Q-system1⊕rho. For odd G=C7 they have dimensions
1,d,(d−1)^3,(d+1)^3,
so the dual D has rank8.

Morita invariance identifies its center with the published double. Its twist-one simples are the unit, b of dimension d², and six A_i of dimension1+d². In the C53 sector the nonzero labels have twists exp(2pi i s x²/53), which are not1; among the c_(h,j), twist1 occurs exactly at j=0.

Consider the actual canonical Lagrangian algebra L=I_D(1). It is connected, has trivial twist and dimension FPdim(D)=7(1+d²), so
L=1+m_b b+sum_(i=1)^6 m_i A_i.
Set S=sum m_i. Comparing rational and irrational coefficients in its dimension gives
m_b+S=7, m_b+2S=13.
Therefore m_b=1,S=6.

Induction/forgetful adjunction and F I_D(1)=sum_X X⊗X* imply dimEnd(L)=rank(D)=8. Thus1+1+sum m_i²=8. The nonnegative integer multiplicities satisfy sum m_i=sum m_i²=6, forcing each of the six to equal1.

Consequently the actual canonical object is exactly the object required in Evans–Gannon Theorem7. Theorem5(d)'s modular data determine the required center fusion through Verlinde. No uniqueness of algebra multiplication is needed. Theorem7 now gives the entire dual fusion ring.

In basis(1,a,b1,b2,b3,c1,c2,c3), indexed modulo7 with b0=c0=0, b_(-i)=b_i and c_(-i)=c_i, the rules are:
a²=1+a+sum b+sum c;
a b_i=a+sum b−b_i+sum c;
a c_i=a+sum b+c_i+sum c;
b_i c_j=a+sum b+sum c;
b_i b_j=delta_(ij)1+(1−delta_(ij))a+sum b−b_(i+j)−b_(i−j)+sum c;
c_i c_j=delta_(ij)1+(1+delta_(ij))a+sum b+c_(i+j)+c_(i−j)+sum c.

R868_model.js and verify_recovery.py construct these rules without reading the target tensor. The fresh model-to-census map is [0,3,1,2,4,5,7,6]. All512 coefficients match the remote published census. All4096 associativity relations and64 dimension products in Q(d) pass exactly. The census fingerprint is1cfda199ea64692ba0d9bd267cb99212d408bc60fdc740757192771fcf0229bd; the independently constructed model fingerprint is02c8f84da2ea39eb781f4fb542565f4d90fc91c7f7b9246dd04c16f5a1b8152a.

The new Gannon–Schopieray–Yadav preprint, arXiv2609.25185 (21 September2026), TheoremA(3), Section4.3 and AppendixE.4, independently describes the same Q-dual and its generator fusion matrix. The unitary existence assertion here uses the established C7 subfactor, so it does not require a claim of uniform unitarity for arbitrary odd orders.

Primary sources:
- https://arxiv.org/pdf/1006.1326 , Theorems5(d),6,7.
- https://arxiv.org/pdf/1609.07604 , Proposition7.4 and Theorem7.5.
- https://arxiv.org/html/2609.25185v1 , TheoremA(3), Section4.3, AppendixE.4.

The theoretical argument was independently audited. The complete census comparison was freshly replayed during recovery.
