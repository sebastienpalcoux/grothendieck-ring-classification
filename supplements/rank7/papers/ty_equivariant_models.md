# Two unitary rank-seven models of dimension 24

Date: 2 October 2026. The two rings are R7_2_1 and R7_2_195. These are categorical constructions with coherent group actions, not proposed fusion-rule identifications alone.

## Common starting category

Let T=TY(C3,chi,tau), where chi(a,b)=exp(2 pi i ab/3) and tau=1/sqrt(3). Its simples are a in C3 and m, with a*b=a+b, a*m=m*a=m and m*m=sum_a a. Write |a|=0 and |m|=1 for its faithful C2 grading.

Inversion I(a)=-a, I(m)=m defines a coherent C2 action on T. Indeed inversion preserves chi. The standard TY associators, including the Fourier matrix tau*chi(a,b)^(-1), are invariant after relabelling channels by inversion. Its tensorators are the canonical channel identifications and I^2=Id as a tensor functor. This action is also supplied directly by Gelaki--Naidu--Nikshych, Proposition 4.8. These categories and functors are unitary: all associators are phases, permutations or the normalized Fourier matrix, and all functor tensorators are unitary.

## R7_2_1: parity shift in an untwisted pointed factor

Take E=T Deligne Vec(C2). A simple is (X,e), e in C2. Define

    F(X,e)=(I(X),e+|X|).

Since |X tensor Y|=|X|+|Y|, the Vec(C2) tensorators are identities. The TY tensorators are those of I. The Vec(C2) associator is trivial, so functor coherence follows immediately from that of I and the grading identity. Also F^2=Id as a tensor functor. This is an actual unitary C2 action, with identity multiplication coherence.

In the equivariantization C=E^C2, the two fixed invertibles (0,0),(0,1) each split into two equivariant simples t_e^+,t_e^-. The other four invertibles form two free orbits P_e={(1,e),(2,e)}. The two m-simples form one free orbit Z={(m,0),(m,1)}. Thus the dimensions are four ones, two twos, and 2sqrt(3).

Choose the model basis

    (1,h,t,ht,P0,P1,Z)=(t0+,t0-,t1+,t1-,P0,P1,Z).

The invertibles form C2 x C2; h fixes both P's and t exchanges them. All four invertibles fix Z. The remaining products, with e,f in C2, are

    P_e P_f = t_(e+f)^+ + t_(e+f)^- + P_(e+f),
    P_e Z=Z P_e=2Z,
    Z^2=1+h+t+ht+2P0+2P1.

The fixed-channel multiplicities are obtained by the swap action on the two product channels: its + and - eigenspaces each have dimension one. The orbit products have unique equivariant simple outputs, so their multiplicities are fixed by forgetting equivariance. These rules match all 343 census coefficients under

    model-to-census permutation [0,5,1,2,4,3,6].

## R7_2_195: a twisted C4 factor

Let z generate C4 and put zeta=exp(2 pi i/4). On C4 use the normalized unitary cocycle

    omega(a,b,c)=zeta^(a floor((b+c)/4)),  0<=a,b,c<4.

In T Deligne Vec(C4,omega), take the full diagonal fusion subcategory E whose simples are

    (a,z^(2e)),   a in C3, e in C2;
    (m,z), (m,z^3).

It is closed under tensor products and duality because TY parity equals the exponent of z modulo two. Define F by inversion in both factors:

    F(a,z^(2e))=(-a,z^(-2e)),   F(m,z^j)=(m,z^(-j)).

The TY tensorator is that of I. On homogeneous C4 degrees a,b use the scalar tensorator J_(a,b)=zeta^(u(a,b)), in the direction F(X) tensor F(Y) -> F(X tensor Y), where

    u = [[0,0,0,0],
         [0,0,0,3],
         [0,3,2,1],
         [0,1,0,0]].

Write w(a,b,c)=a floor((b+c)/4), reducing all arguments modulo four before evaluating. Exact integer checks give

    u(b,c)-u(a+b,c)+u(a,b+c)-u(a,b)
      = w(a,b,c)-w(-a,-b,-c) mod4,
    u(a,b)+u(-a,-b)=0 mod4.

The first is the tensor-functor associativity equation; the second says that F^2 has the identity tensorator. Thus identity eta:F^2->Id gives coherent C2 multiplication. The scalar cocycle equation for omega is checked for every quadruple. No assumed or incoherent choice of eta on z^2 is used.

The simple orbits in E^C2 again yield four invertibles, two 2-dimensional simples P0,P1, and one 2sqrt(3)-dimensional simple Z. Label the fixed invertibles by 1,h,t,t', where t is the + equivariant lift of (0,z^2), h is the nontrivial equivariant lift of the unit, and t'=ht. Although t has equivariant structure +1 and eta=Id, its tensor square has equivariant structure J_(2,2)^(-1)=-1. Consequently

    t^2=h, t^3=t', t^4=1,

so the invertible group is C4. All remaining products are the same formulas above, with t_0^+=1,t_0^-=h,t_1^+=t,t_1^-=t^3.

For completeness the fixed outputs in Z^2 arise from two channel pairs. The degree-two pair (m,z)*(m,z), (m,z^3)*(m,z^3) is swapped with coefficients 1,1. The degree-zero pair (m,z)*(m,z^3), (m,z^3)*(m,z) is swapped with coefficients i,-i. Each swap has eigenvalues +1,-1, giving exactly one copy of each fixed lift. Every other product multiplicity follows from its unique free orbit. Thus the full fusion tensor agrees with R7_2_195 under

    model-to-census permutation [0,6,1,2,5,3,4].

All scalar associators and tensorators are unitary. Taking the full diagonal subcategory and equivariantization by this unitary action preserves unitarity. Hence this is a unitary categorification over C.

## Verification and sources

The portable module `software/ty_equivariant_models.py` verifies all 343 coefficients for each ring, binds both target tensors by SHA256, checks both model fusion tensors' associativity, and verifies every cocycle/tensorator/action equation for the C4 factor. It also independently rebuilds all fusion coefficients from equivariant Hom invariant dimensions `(dimension + trace)/2`. Its deterministic receipt is `output/ty_equivariant_models_verification.json`. The dated update verifier binds the complete ledger to the pinned census source. The categorical existence proof is the construction above; equality and coherence checks support that proof and are not a replacement for it.

Primary references:

- D. Tambara and S. Yamagami, *Tensor Categories with Fusion Rules of Self-Duality for Finite Abelian Groups*, J. Algebra 209 (1998), 692--707, https://doi.org/10.1006/jabr.1998.7558.
- S. Gelaki, D. Naidu and D. Nikshych, *Centers of graded fusion categories*, Algebra & Number Theory 3 (2009), 959--990, Section 4A (explicit TY associators), Proposition 4.8 (bicharacter-preserving automorphism action), https://msp.org/ant/2009/3-8/ant-v3-n8-p05-s.pdf.
- S. Burciu and S. Natale, *Fusion rules of equivariantizations of fusion categories*, https://arxiv.org/abs/1206.6625, for orbit/stabilizer descriptions of equivariant simples and fusion products.

These two constructions alone make no assertion about other rank-seven tensors. The independent quaternion construction in the manuscript also realizes R7_4_2.
