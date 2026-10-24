# The central-fermion shear and its two equivariantizations

Let E be the unitary half-E6 category. Write its simple objects as 1,f,x,
with f²=1, fx=xf=x, and x²=1+f+2x. Use its specified central fermion f from
Aasen-Lake-Walker, arXiv:1709.01941, Section 7. Set d=1+sqrt(3).

Work in the coherent normal form in which the central pointed subcategory is
sVec, f²=1, and its multiplication is strict. Write c_Z:fZ->Zf for the
central half-braiding; c_f=-id. The following formulas are coherent
categorical constructions and do not assume a braiding on E.

## A genuine action, including its square coherence

On D=E⊠Vec(C2), write an object as (Z,h), h in {0,1}. Define

  F(Z,h)=(f^h Z,h).

Its tensorator F(Z,h)F(W,k)->F(ZW,h+k) moves the inserted f^k left past Z
using c_Z inverse, then multiplies the adjacent powers of f. The central
half-braiding identities prove the tensorator pentagon. The identity functor
with tensorator (-1)^(hk) is the resulting F²: the additional crossing in
composing the two tensorators is precisely c_f^(hk).

For either s=i or s=-i, set eta_(Z,h)=s^h:F²(Z,h)->(Z,h). It is monoidal
because s^(h+k modulo 2)*(-1)^(hk)=s^h*s^k. The action equation F eta=eta F
holds since F preserves h and acts trivially on scalar morphisms. These data
therefore give two coherent C2 actions, not merely order-two permutations of
the fusion ring. All structure maps are unitary.

F fixes (1,0),(f,0),(x,0),(x,1) and exchanges (1,1) with (f,1). The
equivariantization has four invertibles, four objects of dimension d and one
object Y of dimension 2. Let epsilon denote the sign character of the acting
C2. The invertibles form V4=<f,epsilon>: in degree zero the action is the
strict identity, so its equivariantization is E⊠Rep(C2). Its two lifts of x
are a and epsilon*a, with

  a²=1+f+2a,  fa=af=a.

## The central-fermion sign on the odd fixed simple

Choose a unitary isomorphism t:fx->x normalized so that t(id_f tensor t)=id_x.
Such normalization is possible because this composite is a nonzero scalar.
Put r=t c_x^{-1}:xf->x. Naturality and the hexagon for c, together with
c_f=-1, give

  r(t tensor id_f) = -t(id_f tensor r).

For clarity, naturality first gives
c_x(id_f tensor t)=-(t tensor id_f)(id_f tensor c_x); taking the equivalent
inverse relation and composing with t proves the displayed anticommutation.

Let b and epsilon*b be the two equivariant lifts of (x,1). On the left,
tensoring with the degree-zero lift f introduces c_f=-1 in F's tensorator.
On the right, the displayed anticommutation produces the same sign. Hence

  fb=bf=epsilon*b.

Thus f*epsilon fixes b on both sides. This calculation is essential; it is
not inferred from a dimension profile or from commutativity of the input.

## Fusion rules forced independently of the census

Every invertible fixes Y, since Y lies over the free orbit {(1,1),(f,1)}.
Forgetting equivariance and using epsilon*Y=Y gives

  Y²=1+f+epsilon+f*epsilon,
  aY=Ya=b+epsilon*b,
  bY=Yb=a+epsilon*a.

Because f fixes a and swaps the two b lifts, forgetting the product ab and
applying f shows that its two b coefficients are equal. This works on either
side, so

  ab=ba=Y+b+epsilon*b.

The product b² forgets to 1+f+2x in degree zero. It is invariant under
f*epsilon, which exchanges the two a lifts. Its two a coefficients must
therefore both be one. Rigidity determines its invertible part: the stabilizer
of b is {1,f*epsilon}, and the dual of b is either b or epsilon*b. Hence

  b²=1+f*epsilon+a+epsilon*a                    (selfdual case),
or
  b²=epsilon+f+a+epsilon*a                     (dual-pair case).

All other products follow by multiplying by the invertibles. Thus there are
exactly two possible tensors for these actual equivariantizations.

## Both duality cases occur

On the underlying fixed simple (x,1), choose an equivariant structure v for
the action eta=i; it satisfies v F(v)=i. For eta=-i, the structure i*v satisfies
(i*v)F(i*v)=-i. Tensorators and the unit equivariant structure are unchanged
when eta changes. Consequently the action on the one-dimensional pairing
Hom((x,1) tensor (x,1),1) changes by the scalar i²=-1.

For a genuine C2 action that pairing eigenvalue is +1 or -1. Eigenvalue +1
places the unit in b² and gives the selfdual case; eigenvalue -1 places the
unit in b(epsilon*b) and gives the dual-pair case. Changing eta interchanges
these cases. Identifying which sign is called i depends on the chosen
fixed-object intertwiner and is unnecessary for existence: both actions have
been explicitly constructed and they realize both tensors.

The two tensors are constructed without reference to census labels in
`shear.py`, which also checks their fusion axioms and all 486 forgetful tensor
identities. The selfdual tensor matches R9_2_96 with permutation
[0,2,3,5,6,7,4,1,8]; the dual-pair tensor matches R9_2_1266 with permutation
[0,6,7,8,3,2,1,5,4]. Each match checks all 729 structure constants.
Both models are unitary equivariantizations of a unitary category.
