# A character-weighted extension of the saturated Galois indicator lemma

Audited theoretical lemma; it has no classification decision on its own. Its signed reindexing proof and the neutral 2D2 application were independently checked. This extends the published fixed-field lemma by reindexing the modular Galois permutation, and applies to saturated quadratic characters inside a multiquadratic dimension field.

## Hypotheses

Let C be pseudo-unitary. Assume its simple dimensions, hence all center dimensions, lie in a multiquadratic field K. Let D=FPdim C. Choose a nontrivial quadratic character chi of Gal(K/Q), of cyclotomic conductor f. Choose a rational linear coordinate p_chi:K→Q on the chi-eigenspace, so

    p_chi(sigma x)=chi(sigma) p_chi(x)

for every sigma. Define ell(z)=p_chi(z/D). Suppose every center simple A outside I(1) for which ell(dim A)≠0 has theta_A^f=1. This hypothesis can follow from equality in the compression bound for that character's dimension block.

Then for every positive integer k coprime to f,

    sum_i ell(dim X_i) nu_k(X_i)=chi(k) ell(1).          (CI)

Unlike the simpler fixed-field lemma, this permits chi(k)=−1. No condition k²=1 modulo f is needed.

## Proof

Let L be a cyclotomic field containing K and all twists. Lift the prescribed unit k modulo f to an automorphism tau of L, using CRT to keep its exponent coprime to the full conductor. Let pi and epsilon_A be its modular Galois permutation and signs. Put sigma=tau|K and z_A=dim A. Modular Galois symmetry gives

    z_(pi A) = epsilon_A (D/sigma D) sigma(z_A),
    theta_(pi A)=tau²(theta_A).

Therefore, with ell_A=ell(z_A),

    ell_(pi A)=epsilon_A chi(k) ell_A,
    tau(ell_A z_A)=chi(k) (sigma D/D) ell_(pi A) z_(pi A).

The first induction trace is

    sum_A ell_A z_A theta_A = D ell(1).                 (1)

Apply tau. The rational coefficients ell_A are fixed, and the preceding transformation accounts exactly for both Galois signs. A term with ell_A=0 vanishes. Outside I(1), each remaining twist has order dividing f; inside I(1), the twist is1. Hence, if h is any positive inverse of k modulo f,

    tau(theta_A)=theta_A^k=theta_(pi A)^h.

Reindexing B=pi A in tau(1) consequently gives

    chi(k) (sigma D/D) sum_B ell_B z_B theta_B^h
       = sigma D ell(1).

Cancel sigma D and use the kth induction indicator formula (with exponent h) to obtain

    sum_i ell(dim X_i) nu_h(X_i)=chi(k) ell(1).

Since inversion permutes the units modulo f and chi(h)=chi(k), this proves (CI) for every unit exponent. In fact the weighted indicator sum depends only on k modulo f.

The argument does not assert that pi is an involution. It uses only its bijectivity, the exact dimension transformation, and the canonical anomaly-free center twist transformation.

## Arbitrary pseudo-unitary 2D2 neutral categories

For the rank-four 2D2 ring, put d=2+sqrt5. Its dimensions are (1,1,d,d), its global dimension is D=20+8sqrt5, and its formal codegrees are D,Dbar,4,4. Thus the central-unit difference saturates the conductor-five bound:

    1/D−1/Dbar=−1/sqrt5.

The saturation hypothesis above follows, and ell can be scaled to the source weights

    (2,2,−1,−1).

All four simple labels 1,g,r,gr are self-dual. Taking k=2, with chi5(2)=−1, gives

    2+2 nu2(g)−nu2(r)−nu2(gr)=−2.

The only possible signs are consequently

    nu2(g)=−1,       nu2(r)=nu2(gr)=+1.

This is a general pseudo-unitary conclusion, not a unitary classification assumption. The pointed C2 associator is therefore nontrivial. It remains compatible with restricting an odd associator class on C4, so it alone does not exclude R8_2_24.

Taking k=3, with chi5(3)=−1, gives

    nu3(r)+nu3(gr)=4,

because Hom(1,g³)=0. Each cubic invariant space has dimension2, so its rotation trace has absolute value at most2. Equality forces

    nu3(r)=nu3(gr)=2,

and both rotations are the identity. No Cauchy theorem or separate cyclotomic-intersection argument is needed for this step.

These conclusions supply the indicator premises in `R24_PROJECTIVE_INNER_SQUARE_PROOF.md`. They do not assert that every neutral category has the known unitary automorphism group or admits the Q-system 1+r.
