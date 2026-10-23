# A nonsplit group-theoretical realization of R11_1_104

This is an explicit categorical construction, not a fusion-ring recognition
heuristic. Its finite input is `jordan_gt_model.json`; the independent
verification does not depend on the search that discovered the cocycle.

## Group and associator

Write A=F2^3 as integers a=a0+2a1+4a2. Put

    sigma(a0,a1,a2)=(a0+a1,a1+a2,a2),   z=(1,0,0).

The order-32 group G consists of (a,e), 0<=e<4, with

    (a,e)(b,f)=(a+sigma^e(b)+z floor((e+f)/4), e+f mod4).

Here addition in A is modulo two; the table index is 4a+e. Thus t=(0,1)
acts by sigma and satisfies t^4=z. The subgroup H is the plane a0=0,
e=0, with indices [0,8,16,24].

Let W be the complete normalized 32-by-32-by-32 integer array under the
`omega` key of the certificate, and put omega(g,h,k)=exp(2 pi i W(g,h,k)/8).
The executable certificate checks every one of the 32^4 identities

    W(b,c,d)-W(ab,c,d)+W(a,bc,d)-W(a,b,cd)+W(a,b,c)=0 mod8.

It also checks all normalization equations and W|H^3=0. Therefore Vec_G^omega
is an actual unitary pointed fusion category, and C[H] is an associative
connected separable algebra in it. Its category of bimodules, with relative
tensor product, is the unitary fusion category C(G,omega,H,1). Its dimension
is |G|=32.

For reproducibility, `jordan_full_cochain.py` reconstructs W from linear
equations over Z/8. It prescribes on A the trilinear cocycle

    W((a,0),(b,0),(c,0))
      =4 a0(b0 c0+b1 c1+b2 c2+b1 c2) mod8.

The solver uses a Cayley spanning tree for generators (0,1) and ((0,0,1),0).
The unknowns are W(g,b,c) for those two generators, b,c nonidentity. From
delta W(g,h,b,c)=0 one recursively recovers W(gh,b,c). The remaining
generator equations and prescribed restriction form a finite linear system
with 1922 variables. Binary bit-plane elimination solves it over Z/8,
including divisions by two after all unit pivots have been removed. No
existence inference depends on completeness of this search: the full
cocycle check independently verifies the final array.

## Derivation of the tensor calculation

We fix the associator convention alpha:((X Y) Z)->X(Y Z), acting by omega.
Write L_a and R_b for left and right H-actions on a homogeneous vector of
degree x. Since the algebra cochain is trivial, the bimodule identities are

    L_a L_b = omega(a,b,x)^(-1) L_ab,
    R_b R_a = omega(x,a,b) R_ab,
    R_b L_a = omega(a,x,b) L_a R_b.

Define T(a,b)=L_a R_(b^-1), taking degree x to axb^-1. Directly applying
these three identities gives

    T(a,b) T(c,d)|V_x = exp(2 pi i kappa(a,b,c,d,x)/8) T(ac,bd)|V_x,

where, writing w=W,

    kappa(a,b,c,d,x)
      =w(c,xd^-1,b^-1)-w(a,c,xd^-1b^-1)+w(x,d^-1,b^-1).

Thus the simples supported on a double coset HzH are indexed by irreducible
projective characters of K_z=H intersection zHz^-1, with factor set

    alpha_z(a,c)=kappa(a,z^-1az,c,z^-1cz,z).

If x=uzv^-1 and ax=xb, set k=u^-1au and l=v^-1bv=z^-1kz.
The character at the degree x is the projective character at k times the
scalar with exponent

    kappa(a,b,u,v,z)-kappa(u,v,k,l,z).

This follows by comparing T(a,b)T(u,v) and T(u,v)T(k,l), so it includes the
transport phases rather than assuming an untwisted character formula.

For the relative tensor product V tensor_H U, the balancing relation is

    (R_h v_x) tensor u_y
      = omega(x,h,y) v_x tensor (L_h u_y).

Choose x from representatives of G/H and put y=x^-1z. A stabilizer element
(a,b), az=zb, contributes to the trace on this summand precisely when
h=x^-1ax belongs to H. Then yb^-1=h^-1y. Apply the induced left and right
actions on the tensor product and reduce its first degree from ax=xh back
to x using the displayed balancing relation. The resulting trace is

    exp(2 pi i E/8) tr T_V(a,h)|V_x tr T_U(h,b)|U_y,

where

    E=w(x,y,b^-1)-w(a,x,yb^-1)+w(x,h,yb^-1)
      -w(x,h,h^-1)+w(a,x,h^-1).

For example, the last two terms arise from

    (R_h|V_x)^(-1)L_a
      =omega(x,h,h^-1)^(-1)omega(a,x,h^-1)L_aR_(h^-1).

Sum over x, then take the ordinary projective-character inner product on
K_z, dividing by |K_z|. This yields every tensor multiplicity. It is exactly
the phase convention implemented in `integral/gt32.py` with all exponents
doubled from Z/8 to its Z/16 arithmetic. Polynomial reduction modulo
Phi_16=X^8+1 keeps the calculation exact.

The resulting simple dimensions are (1,1,1,1,2,2,2,2,2,2,2), up to the
stored model order. The tensor has rank eleven and multiplicity one. The
explicit source-to-model basis bijection is

    [0,4,8,5,9,1,2,3,10,6,7].

`jordan_verify.py` checks all 1331 source coefficients under this map,
as well as the group, cocycle, algebra and reconstructed tensor. The
separate independent tensor replay under `nonintegral/audit104` also passes:
it builds actual free bimodules, verifies their action axioms, forms balanced
relative tensor quotients, and solves graded intertwiner equations. It uses
neither this projective-character convolution nor `gt32.py`. Both normal and
optimized-Python executions reproduce all 1331 coefficients. Thus the model
has passed both the direct cocycle verification and independent tensor audit.

## Categorical references and scope

The construction as bimodules over a twisted subgroup algebra is standard:
Etingof--Gelaki--Nikshych--Ostrik, *Tensor Categories*, Section 9.7,
https://math.mit.edu/~etingof/egnobookfinal.pdf; and Schauenburg,
*A Higher Frobenius--Schur Indicator Formula for Group-Theoretical Fusion
Categories*, Introduction and Section 2,
https://arxiv.org/abs/1502.02906. We use their general construction and
projective-stabilizer description, not the paper's indicator formula.
The tensor phases above are derived explicitly in our associator convention.

The nonsplit group and the displayed cocycle supply a concrete new model
for this census input. They do not classify all associators of this ring.
Failure of the preceding split-action and bounded polynomial searches was
used only to guide this construction, never as an exclusion criterion.
