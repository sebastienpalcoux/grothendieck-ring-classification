# Two general exclusions from a three-parameter signed argument

**Theorem.** Neither R7_3_783 nor R7_3_1015 admits categorification over C. No pivotal structure is assumed.

## 1. Source fusion rules

Both rings have basis 1,g,g²,E,ρ0,ρ1,ρ2, where g³=1, E*=E, ρ0*=ρ0 and ρi=g^iρ0. Put G=1+g+g² and S=ρ0+ρ1+ρ2. Their rules are

    gE=Eg=E,
    ρ0g=g^rρ0,                         r=-1 or +1,
    E²=G+3E+S,
    Eρi=ρiE=E+2S,
    ρ0²=1+2E+2S.

The two values r=-1,+1 give respectively R7_3_783 and R7_3_1015. In the source order take g=X1 and ρ0=X6 in both cases; E=X4 and E=X5 respectively. These relations generate every product, and the verifier compares all343 structure constants.

## 2. Every categorification is spherical

Let C be a hypothetical categorification. Pass to its sphericalization and then take the signed quotient ε=-1. Choose a lift g with g³=1; one of the two lifts has this property. Choose the positive-second-indicator lifts E and ρ0. Use the lifts g^iρ0 to define ρi.

Since g³=1 and gE has the same underlying simple as E, gE=E in the signed algebra: its coefficient is±1, whose cube must be1. The same applies to Eg. Similarly the scalar in ρ0g=±g^rρ0 must have cube1, so ρ0g=g^rρ0.

The coefficient of ρ0 in E² is1. Indeed its original multiplicity is1, and the positive-indicator square-channel congruence is modulo4. Multiplying E² on the left by g leaves E² fixed. Thus the three orbit coefficients in E² are all1. Frobenius reciprocity gives the coefficients of1,g,g² all1. Consequently

    E²=G+bE+S,       b∈{-1,3}.

Because (gE)ρ0=Eρ0 and E(g^iρ0)=Eρ0, every Eρi equals an element fixed by left multiplication by g. The support and Frobenius reciprocity therefore give

    Eρi=E+aS.

Here a is also the coefficient of E in ρ0², since E and ρ0 are self-dual. The original coefficient is2, and the square-channel congruence gives a∈{-2,2}. Write

    ρ0²=1+aE+c0ρ0+c1ρ1+c2ρ2,       ci≤2.

No sign normalization or modulo-four restriction is required for c1,c2. The ordinary absolute-value bound suffices. Let c=c0+c1+c2≤6. Multiplying the last relation by G gives

    Sρ0=G+3aE+cS.

Now compare E²ρ0 and E(Eρ0). Their S-coefficients give the single identity

    ba+c=3a².

If a=-2, then c is10 or18. If a=2,b=-1, then c=14. All contradict c≤6. Thus a=2,b=3,c=6, forcing c0=c1=c2=2. All displayed signed products are therefore the original positive products. The g-relations generate all remaining products, so the chosen seven lifts are closed under tensor product and duality. They form a spherical fusion subcategory of the sphericalization, and the forgetful functor restricts to a tensor equivalence with C. Therefore C admits a spherical structure.

This argument proves pivotality/sphericality directly; it does not infer pivotality merely from the original based-ring symmetries.

## 3. Spherical categorification is impossible

The regular Casimir polynomial of each ring is

    (x-15)(x-6)^4(x²-240x+900).

Write D=120+30sqrt15 and D'=120-30sqrt15. The spherical global dimension δ is the codegree of its categorical-dimension character, hence an eigenvalue of the Casimir. Thus δ∈{6,15,D,D'}. Ostrik's formal-codegree induction theorem implies that δ/D is an algebraic integer. The rational alternatives have norms

    Norm(6/D)=1/25,       Norm(15/D)=1/4,

which are not integers. Therefore δ is D orD'.

For the quadratic field Q(sqrt15), whose discriminant is60, Schopieray's dimension-block bound (Theorem5.1, arXiv:2609.35287v1) requires

    (1/δ-1/δ')² ≤ 1/60.

But the left-hand side is1/15. This contradiction excludes both rings.

## Sources and verification

- The canonical sphericalization and positive-indicator parity conditions are the same established inputs as `evidence/upper_residual_20261002b/r7_nonintegral/SIGNED_GENERAL_PROOF.md` (Ostrik, arXiv:1309.4822, §5.1; Liu–Palcoux–Ren–Vercleyen, arXiv:2203.06522v5, Theorem3.9).
- V. Ostrik, *Pivotal fusion categories of rank3*, arXiv:1309.4822, Theorem2.13: δ/f is an algebraic integer for each formal codegree f.
- A. Schopieray, *The dimension block of a spherical fusion category*, arXiv:2609.35287v1 (28 September2026), Theorem5.1.

`verify_C3_signed_general.py` reads the census, identifies g,E,ρ, reconstructs all343 products, checks the only four possible(a,b) branches, and verifies the exact Casimir/norm/dimension-block arithmetic. The proof of the signed reduction is entirely theoretical; the replay checks only source identification and elementary arithmetic.
