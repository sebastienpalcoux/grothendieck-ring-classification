# Independent audit: a unitary model of R9_2_1254

**Result: accepted.** The construction provides an actual coherent unitary C2 action after central condensation, and its equivariantization matches all 729 census coefficients. The cover functor has order four on objects; imposing order two before condensation would exclude this valid construction.

The independent replay files are `mr_order4_audit.py` and `mr1254_tensor_audit.py`. They do not import the construction scripts. They read the exact phases in `../weak_a/mr_order4_descent_2_3_1_4.json` and the pinned census tensor in `source_tensors.json`. All inputs lie within phase4; no live repository, network, or earlier work directory is needed. The JSON audit receipts record the resulting checks.

## Categorical descent

Write ζ=exp(2πi/16). The covering category B is the parity subcategory of Ising⊠Vec(C16,Ω), where

    Ω(a,b,c)=ζ^[2a floor((b+c)/16)].

Its 24 simple objects are (i,a), with i=0,1 for 1,ψ and a even, or i=2 for σ and a odd. It has dimension 32. The central invertible g=(ψ,8) has right half-braiding g⊗(i,a)→(i,a)⊗g with exponent

    β(i,a)=7a+e_i mod16,     (e_0,e_1,e_2)=(0,8,12).

The audit checks every half-braiding hexagon, its central square, self-braiding one, and the trivial associator on g's powers. Thus A=1⊕g is a central commutative separable unitary algebra, and D=B_A is a unitary fusion category of dimension 16.

The cover object permutation is

    F(i,a)=(i xor(a/2 mod2),3a),  i=0,1;
    F(2,a)=(2,3a),

with charge modulo 16. Its square is K(x)=g^p(x)⊗x, where p is the odd parity. The supplied tensorator J_F has unit-modulus scalars. Independently rebuilding the Ising and pointed associators verifies all **18,432 nonzero tensor-functor associator entries** for F. The 1/√2 magnitudes are preserved because F preserves the σ type. Unit constraints and central transport also pass.

The canonical tensorator J_K is obtained by associating (g^p x)(g^q y), moving g^q past x by the inverse right half-braiding, and multiplying the leading powers of g. This separately passes all **18,432 entries**. The supplied d:F²⇒K satisfies all **640 fusion-channel monoidality equations**

    d(x)+d(y)−d(z)
      =J_F(x,y;z)+J_F(Fx,Fy;Fz)−J_K(x,y;z) mod16.

Here and below J and d denote additive exponents. The central algebra map φ:F(A)→A is identity on 1 and ζ on g. Its algebra equation is φ_g²=J_F(g,g;1), whose exponent is 2. The compatibility needed to descend d is exactly

    d(g)=J_F(g,g;1)=2 mod16,

and is verified. Hence F descends to a unitary tensor functor f on D, and d descends between f² and the functor induced by K.

The latter functor is canonically monoidally isomorphic to Id_D: on the free module q(x), apply the regular-algebra multiplication map λ:q(g)→1_D to q(g)^p⊗q(x). Its monoidality is precisely the central interchange used in J_K, with β(g)=1 and g²=1. This establishes f²≅Id as tensor functors, before checking the remaining group-action coherence.

## Explicit C2 coherence

The direction of the free-module comparison matters. It is

    q(Fx) → f(qx),     γ_x=J_F(x,A)(id⊗φ⁻¹).

It gives f(λ)=φ_g λ under the comparison. If κ:qK⇒q is the canonical map above, then the transported f(κ_x) acquires the scalar φ_g^p J_F(g,x;gx)^−p. Consequently the C2 coherence defect for κ∘q(d), in additive exponents, is

    δ(x)=d(Fx)−d(x)−p(x)[1−J_F(g,x;gx)] mod16.

The independent replay gives δ=0 on every even object and δ=8 on every odd object. Replace the saved exponents by

    d′(i,a)=d(i,a)−4a mod16.

This multiplies d by a grading character. It preserves all 640 monoidality equations and the algebra compatibility, and makes **δ identically zero on all 24 simple objects**. Thus the descended involution has an explicit coherent unitary C2 action; no unresolved coherence premise remains. As a separate consistency check, the universal grading is C8, f acts by 3, and

    H³(C2,C8_3)=ker(1+3)/im(3−1)=2C8/2C8=0.

The explicit correction already proves the required coherence without relying on that obstruction calculation.

## Fixed lifts and independent census match

The quotient D has simples u^a (a∈C8) and ρ_r (r∈C4), with

    u^a u^b=u^(a+b),       u^aρ_r=ρ_r u^a=ρ_(r+a),
    ρ_rρ_s=u^(r+s+1)+u^(r+s+5).

The action is u^a↦u^−a and ρ_r↦ρ_(3r+1). Only 1 and u^4 are fixed. Their representatives in B are literally fixed by F. The audit confirms

    d′(u^4)=J_F(u^4,u^4;1)=14 mod16.

Therefore both equivariant lifts of u^4 have square 1, and the four invertibles of the equivariantization form V4. The odd moving orbits {ρ_0,ρ_1} and {ρ_2,ρ_3} are mutually dual, since ρ_r*=ρ_(3−r).

The independent tensor reconstruction uses fixed-output multiplicity (dimension+trace)/2 and the multiplicity at one representative for a moving output. Every contribution with a moving input pair has trace zero, since the involution exchanges the summands. Contributions with fixed inputs are determined by the verified V4 multiplication. Thus there are no omitted fusion-space phases.

With model basis

    [1,ε,u4+,u4−,{u1,u7},{u2,u6},{u3,u5},odd01,odd23],

the source-to-model basis permutation is

    [0,7,8,2,3,1,4,6,5].

All **729 coefficients** agree. This proves unitary realizability of R9_2_1254, without a claim to classify all its categorifications. The differently ordered model basis in `../weak_a/mr_1254_model.json` explains its different displayed permutation.

The source corpus and individual canonical tensor SHA-256 hashes are recorded in `source_tensors.json`. Both independent scripts also pass under `python -O`, so their conclusions do not depend on enabled assertions.
