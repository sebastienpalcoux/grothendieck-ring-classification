# R155: fermion traces and odd Gauss sums

These arguments use the certified six-profile reduction and its unique central
pointed subgroup `Semion ⊠ sVec`. They do not assume unitarity, nor a tensor
factorization of the original category. Work in the positive spherical Galois
representative. Write `d=4+3√2`, `D=72+48√2`, `b=2+4d=D/4=3√2 d`,
and `u=exp(-πi/4)`. Split **the center** as `Z(C)=Semion ⊠ B`.
Then `B` is modular, has unique nontrivial invertible fermion `f`, and
`τ⁺(B)=D/(1+i)=D(1-i)/2`.

## Exact inherited input, reconstructed

`check_center_profiles.py` reconstructs all semion packets and all fermion charge
splits from the high-column profile input, using the exact existing routines.
It does not read the saved packet/charge conclusions and uses no optimizer.
Each profile has two initially admissible semion orientations, with exactly one
remaining fermion-charge split. The dimensions in the odd component are:

| profile | rank B | even | odd | forced #Fix(f) | odd dimensions |
|---|---:|---:|---:|---:|---|
|275|30|16|14|2|d×4, 2d×8, b×2|
|277|27|16|11|5|d×4, 2d×4, 4d×1, b×2|
|279|24|16|8|8|d×4, 4d×2, b×2|
|296|26|16|10|6|d×2, 2d×4, 3d×2, b×2|
|298|23|16|7|9|d×2, 3d×2, 4d×1, b×2|
|306|22|16|6|10|3d×4, b×2|

Here even/odd means monodromy with f is +1/-1. In every row the two b
objects have underlying restrictions `1+h+2X+2Y` and `g+gh+2X+2Y` and
twists `1,-i`, respectively. The first is the fermion-odd, semion-even
summand of I(1). The second is g times its semion-odd partner in I(1).
All summands of I(1) have twist 1. Both b objects are f-fixed: each is
unique in its restriction type in B, and multiplication by h preserves that
restriction type.

## Fermion trace

Verlinde diagonalizes N_f with eigenvalues S_fj/S_0j=μ_f,j. Since N_f is
the permutation matrix of tensoring by f,

    #Fix(f) = trace(N_f) = rank(B_even) - rank(B_odd).

A fixed simple necessarily has monodromy -1, because balancing gives
`θ_(fV)=(-1) μ_f,V θ_V`. Thus #Fix(f) cannot exceed the odd rank.
This directly excludes profiles **298 and 306**. The old integral-rotation
certificate for 306 is unnecessary for this exclusion.

Even simples occur in f-pairs with opposite twists, so they contribute zero
to τ⁺(B). Odd f-pairs have equal twists. Ribbon duality also preserves
twists: θ_(V*)=θ_V, with no complex conjugation.

The known b pair contributes b²(1-i). Since b²=18d² and
`(D/2-b²)(1-i)/d²=-24u`, all remaining odd contributions, divided by d²,
sum to -24u.

## Profile 275

Exactly two f-fixed simples are allowed, and the b pair accounts for both.
The odd d objects have restrictions X,X,Y,Y. Tensoring by f swaps the
pair over X and swaps the pair over Y; duality matches these pairs.
Consequently all four have one twist α. The eight odd 2d objects form
four f-pairs with twists β₁,...,β₄. The Gauss equation is

    4α + 8(β₁+β₂+β₃+β₄) = -24u.

Dividing by 4 shows that the root of unity α is divisible by 2 in the
ring of algebraic integers, impossible. Thus **275 is excluded**.

## Profile 279

The four odd d objects have restrictions X,X,Y,Y, and duality implies
that their twist sum is 2(α+β). Write γ,δ for the two 4d twists.
The Gauss equation becomes

    α+β + 8(γ+δ) = -12u.

Hence α+β is divisible by 4 in the ring of algebraic integers. Every
Galois conjugate of (α+β)/4 has absolute value at most 1/2; its norm
therefore forces it to vanish. Thus γ+δ=-3u/2, which is not an algebraic
integer. Therefore **279 is excluded**, without any indicator assumption.

## Profile 277: twist orders

Exactly five f-fixed simples are allowed. Two are b objects and the unique
4d object is also fixed. Among the four d objects, fixed points occur in
multiples of four: f acts on the two over X and the two over Y, and duality
commutes with f. There are only two fixed points left, so all four d
objects are free and share a twist α. The four 2d objects comprise two
fixed points of twists β,γ and one free pair of twist δ. Let ε be the
unique 4d twist. The Gauss equation is

    α+β+γ+2δ+4ε = -6u.                         (1)

Use the Galois symmetry of the modular data of **Z(C)**, whose anomaly is
trivial. Its twists satisfy θ_(σ̂j)=θ_j^(a²), for the cyclotomic automorphism
ζ→ζ^a. The rational pointed character values ±1 show that σ̂ preserves
both semion and fermion monodromy charges, hence preserves B and its odd
component. It also preserves each dimension kd occurring here: if σ
fixes √2 this is immediate; otherwise `D/σ(D)=1+4d` and
`(1+4d)σ(d)=-d`, so the positive dimensions are again kd after the Galois
sign. Finally, the rational matrix N_f commutes with the signed Galois
permutation because its Verlinde eigenvalues are rational. Hence Galois
permutations preserve f-fixedness.

The four d objects all have twist α, the unique free 2d pair has twist δ,
and the unique 4d object has twist ε. Therefore α,δ,ε are invariant under
all square powers of cyclotomic units. Their orders divide 24. The two
fixed 2d objects are permuted, so the square-power orbit of each of β,γ
has size at most two. Cauchy's theorem restricts twist prime divisors to
2 and 3. The square subgroup of `(Z/(2^a3^b))^×` has size
`2^max(a-3,0) 3^max(b-1,0)`. Thus the orders divide 48. If there is a
primitive 16th-root component, the automorphism a=5 exchanges the twists
and gives γ=-β. Both their sum and the sum of their cubes then vanish;
for equations (1) and (2) below this case can be represented by an
opposite pair of 24th roots.

## Profile 277: the cubic indicator

Apply the center indicator formula to X and split the sum into B and gB.
For each V in B, its contribution is

    dim(V) θ_V³ ( [F(V):X] - i [F(V):Y] ).

Even f-pairs cancel, since their twists are opposite and the X,Y
multiplicities of their restrictions agree. The b pair contributes
4b=D. The remaining restrictions give

    ν₃(X) = 1 + (u/6) S₃,
    S₃ = α³+β³+γ³+2δ³+4ε³.                   (2)

In particular `|ν₃(X)-1|≤9/6`. The full four-dimensional Clifford
rotation domain is

    {-2,-2ζ₃,-2ζ₃²,1,ζ₃,ζ₃²}.

Every value except 1 has distance at least √3 from 1. Thus ν₃(X)=1 and
S₃=0. This uses the full actual domain, not an assumption that ν₃ is real.

`gauss277.py` enumerates equation (1) over 24th roots by testing 24³
choices of α,δ,ε and looking up unordered β,γ pairs. It uses integer
arithmetic in `Z[t]/(t^8-t^4+1)`. There are 30 solutions of (1), and
none has S₃=0. Therefore **277 is excluded**.

The verifier uses explicit guards, including in optimized Python. No
LP/MILP status is used in these exclusions.

## Profile 296

Only profile 296 remains. Its [twist spectrum is forced](forced_twists.md),
with center rank 52 and exponent 24. Existence remains unresolved.
