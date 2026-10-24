# New restriction for the three commutative rank-nine cases

**Status:** R9_2_137, R9_2_1607 and R9_2_1976 remain unresolved. The argument below rules out a central lift that an earlier research note had retained as a possible route. It does not produce an exclusion or a model of a source ring.

## Theorem

Let C be any complex fusion categorification of one of those three rings. Its unique isotropic free involution g has no half-braiding. Consequently the pointed braided subcategory of Z(C) is either Vec or sVec. Moreover, Z(C) contains no nontrivial Tannakian fusion subcategory, and every integral-dimensional simple of Z(C) is invertible.

These statements require no pivotality or unitarity assumption on C.

## Proof

The already proved TY-module reduction identifies the integral subcategory of C with TY(V4, chi, tau), with chi nonalternating and tau equal to either sign of 1/2. Its two anisotropic involutions h1,h2 stabilize the two different orbits of large simples. Their product g is isotropic and acts freely on those four simples. The source labels, using zero-based indexing, are:

| Ring | Dimension-two object | h1 | h2 | g | Free g-orbits |
|---|---:|---:|---:|---:|---|
| R9_2_137 | 8 | 7 | 2 | 1 | {3,6}, {4,5} |
| R9_2_1607 | 3 | 4 | 6 | 5 | {1,2}, {7,8} |
| R9_2_1976 | 5 | 6 | 7 | 8 | {1,2}, {3,4} |

The full adjoint subcategory equals C; the checker verifies this by closing the supports of all XX*. Thus the universal grading is trivial. The kernel of the forgetful homomorphism Inv(Z(C)) → Inv(C) consists of tensor automorphisms of the identity, hence is the character group of the universal grading and is trivial.

Suppose g has a half-braiding. Its central lift has order two, by this injectivity. On the TY subcategory, its self-braiding is chi(g,g)=1. This follows from the invertible central-object formulas in Gelaki–Naidu–Nikshych, Proposition 4.1. Thus its generated braided subcategory is Rep(C2), and its forgetful image is the full subcategory on 1,g. Central de-equivariantization gives a fusion category E=C_(C2).

The two free g-orbits of invertibles produce two invertibles in E. The g-fixed dimension-two simple splits into two further invertibles. The two free orbits of dimension-d simples, d=4+3sqrt(2), produce two simple objects X,Y of dimension d. Each orbit is duality-stable, so X and Y are self-dual. Writing the four invertibles as 1,h,u,hu, the exact products are

    hX=X, hY=Y, uX=Y, uY=X,
    X²=Y²=1+h+4X+4Y,
    XY=u+hu+4X+4Y.

The only alternatives are u²=1 and u²=h. They give respectively V4 and C4 as invertible groups. Both quotient tensors are already excluded by general-scope results in this project:

| Quotient group | Exact target | Existing general exclusion |
|---|---|---|
| V4 | R6_4_174 | General higher stabilizer-rotation obstruction |
| C4 | R6_4_6 | Forced C4 associator with stabilizer-rotation obstruction |

For both rows the permutation from quotient basis (1,h,u,hu,X,Y) to the stored target basis is (0,5,1,2,3,4). The checker compares every one of the 216 tensor coefficients and checks the six source-to-quotient maps at every coefficient. Therefore E cannot exist, and g cannot have a central lift.

For any central lift of h1 or h2, the same TY formula gives self-braiding -1. There can be at most one such lift: the product of two would lift g. Injectivity excludes other possibilities. This proves the pointed-center assertion. It is essential here that a fermionic central lift in a nonbraided C is not automatically a transparent fermion in a braided C; its fixed objects do not supply a contradiction.

Finally let Rep(H) be a Tannakian subcategory of Z(C). The algebraic-integer divisibility theorem for fusion subcategories gives FPdim(Z(C))/|H| integral. Here FPdim(C)=144+96sqrt(2), of field norm 2304=2^8·3². Taking norms shows that every prime divisor of |H| is 2 or 3. Burnside's theorem makes H solvable. If H is nontrivial its abelianization is nontrivial, so Rep(H) has a nonunit invertible object with self-braiding +1. This contradicts the pointed-center assertion. Thus H is trivial.

In particular, no fusion category Morita equivalent to C has a nontrivial faithful finite-group grading: such a grading would embed Rep(H) in its center, which is braided equivalent to Z(C).

For the final assertion, let E be the full subcategory of Z(C) consisting of objects whose forgetful image lies in the integral TY subcategory of C. It is a fusion subcategory because the forgetful functor is tensor and the TY subcategory is closed under tensor products, duals, and summands. Each central simple has dimension a+b d with nonnegative integers a,b; the irrationality of d shows that it has integer dimension precisely when b=0. Thus E contains exactly the integral-dimensional central simples and is integral. Its integer FP dimension again has prime divisors only 2 and 3. The categorical Burnside theorem (Etingof–Nikshych–Ostrik, Theorem 1.6) makes E solvable, in particular weakly group-theoretical. It has no nontrivial Tannakian subcategory, so it is weakly anisotropic. Natale's Theorem 4.1 then implies that E is pointed. Consequently E is exactly Vec or sVec, as claimed. Notice that the weakly group-theoretical theorem is applied only to E, whose dimension is an integer; it is not applied to the nonintegral ambient center.

## Lower-rank proof dependencies and scope

The existing proof for R6_4_174 is the paragraph “The ring R(4,174)” in `manuscripts/rank6/papers/chapters/higher_stabilizer.tex`. It reconstructs the unique anti-invariant module branch, whose stabilizer signs on both noninvertibles are negative. Their cubic invariant spaces have dimension four. The Clifford-rotation bound places their relative third-indicator traces in [-2,1]. The height-six central-induction analysis reconstructs ten low frames, eight character labelings, and 128 second-indicator systems; exact separating rays exclude all of them. Its general-scope reduction uses the two-FP-dimension Galois-pseudo-unitarity theorem. The checker is `stabilizer_rotation_higher.verify_general`.

The existing proof for R6_4_6 is Theorem `thm:c4-multiplicity-four` in `manuscripts/rank6/papers/chapters/pointed_associators.tex`. A pointed-algebra module argument forces associator class 2 in H³(C4,C*), hence fourth indicator -1 for an order-four generator in the pseudo-unitary representative. Positive twist saturation imposes theta⁴=-1 on its induced central constituents. The unique anti-invariant module branch gives the same cubic bounds. Ten low frames and four second-indicator assignments per frame are excluded by forty exact rational Farkas certificates. Again the two-FP-dimension theorem supplies general scope. The checker is `round3_smallest.verify`.

This use of the two-dimension theorem is an **existence reduction to a pseudo-unitary Galois conjugate**. It does not assume the original category is unitary or that an arbitrarily selected spherical structure is positive.

`verify_no_central_boson.py --replay-dependencies` reconstructs both lower-rank certificates under optimized Python, with numerical optimizer entry points disabled. Dependency tensors and certificates are retained in `lower_rank_dependencies.json`; the quotient maps are in `central_lift_reduction_certificate.json`; the new transport receipt is `no_central_boson_receipt.json`.

For this continuation, the fast transport check completed. The optional duplicate full replay was stopped while reconstructing R6_4_174's 128 old systems after more than 23 CPU minutes; it did not complete, and R6_4_6's fresh replay had not started. The argument inherits the already published general-scope proofs, whose exact source versions are hash-bound, rather than claiming a fresh reproof. See `dependency_replay_status.json` for the distinction. All newly introduced exact checks completed.

## Correction to the earlier boundary

The earlier `phase5/quadratic_comm/CENTRAL_LIFT_REDUCTION.md` correctly derived the conditional quotients, but described the V4 quotient R(4,4) as open by citing the external Meng–Yu paper alone. It missed the project's existing general exclusion of the identical tensor R6_4_174, and likewise did not connect the C4 quotient to R6_4_6. The corrected conclusion is that the central-lift branch is impossible. It remains invalid to infer that the central lift exists merely because g is central in the based ring.

## Primary references

- Gelaki–Naidu–Nikshych, *Centers of graded fusion categories*, Proposition 4.1 (central invertibles of TY categories): https://arxiv.org/pdf/0905.3117.
- Drinfeld–Gelaki–Nikshych–Ostrik, *On braided fusion categories I*, Theorem 4.18, Proposition 4.19, and Remark 4.21 (central de-equivariantization without a pivotal assumption); Corollary 4.28 and its proof (a faithful grading supplies central Rep(H)): https://arxiv.org/pdf/0906.0620.
- Etingof–Nikshych–Ostrik, *On fusion categories*, Proposition 8.15 (FP-dimension divisibility for fusion subcategories): https://arxiv.org/abs/math/0203060.
- Schopieray, *Categorification of integral group rings extended by one dimension*, published corrected form of Lemma 3.1, Journal of the London Mathematical Society 108 (2023): https://doi.org/10.1112/jlms.12789. The earlier arXiv v1 wording incorrectly states positivity of every original category; that stronger assertion is not used. The input is the weaker Galois-pseudo-unitarity conclusion, originating in Thornton's thesis Theorem IV.3.6.
- Etingof–Nikshych–Ostrik, *Weakly group-theoretical and solvable fusion categories*, Theorem 1.6 (integer FP dimension with at most two prime divisors implies solvability): https://arxiv.org/pdf/0809.3031.
- Natale, *The core of a weakly group-theoretical braided fusion category*, Theorem 4.1 (integral, weakly group-theoretical, weakly anisotropic braided fusion categories are pointed): https://arxiv.org/html/1704.03523v1.

