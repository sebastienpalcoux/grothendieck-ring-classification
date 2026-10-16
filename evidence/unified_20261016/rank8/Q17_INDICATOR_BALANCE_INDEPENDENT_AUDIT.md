# Independent audit of the conductor-17 indicator-balance obstruction

Status: PASS. The numerical case binding is delegated to the source-bound replay; the general-to-Galois-pseudo-unitary reduction is independently verified below. Auditor: `simple_global`, 2026-10-16.

I independently checked the theoretical argument communicated by `two_d_two`, including the noncommutative extension to R8_2_36 and R8_2_412. The five cases are R8_2_33, R8_2_36, R8_2_76, R8_2_412 and R8_2_446.

## Low modular compression, including noncommutative rings

All five have dimensions 1 on four invertibles and d=4+sqrt(17) on four noninvertibles, with D=136+32sqrt(17). The source Casimir polynomial is `(lambda-8)^6*(lambda^2-272lambda+1088)`.

For an irreducible ring representation E of dimension e, the Casimir eigenvalue is e*f_E and has multiplicity e^2. Thus the two simple eigenvalues D and Dbar come from one-dimensional characters, while every other formal codegree f_E=8/e is rational. Ostrik's central dimension formula is `dim A_E=D/f_E=eD/lambda`, with I(1) multiplicity e. Keeping this distinction between the Casimir eigenvalue and formal codegree avoids a potential normalization error.

Let J be the central constituent attached to the conjugate dimension character. Then `dim J=D/Dbar=1+8d`. The character-level center correspondence gives S_0J=1/Dbar, S_JJ=1/D and S_EJ=S_E0=1/f_E for every other I(1) constituent. This uses only the dimension of each forgetful object and rationality of f_E; it does not require commutativity or a complete irreducible character table.

The I(1) multiplicity vector m satisfies S m=m. Consequently the modular Galois signs on its support are positive, even when m contains an entry two. The unit/J difference transforms by the primitive quadratic character of conductor 17. Its known low compression equals `-1/sqrt(17)` times that difference, saturating the separately audited conductor bound. Equality forces the full twist-one projection to have no other component, and the conductor/residue theorem forces each high central simple with nonrational dimension ratio to have a primitive 17th-root twist of negative quadratic residue. In particular its twist cannot be one.

## Pointed constituents force rational dimension ratios

If g is invertible of order n=2 or 4, Hom(1,g^n) has dimension one. The pivotal rotation on this space has order n, so its indicator nu_n(g) is an nth root of unity. The center formula gives

    sum_A [FA:g] dim(A) theta_A^n = D nu_n(g).

The positive weights on the left sum to D. Equality in the triangle inequality forces every theta_A^n with [FA:g]>0 to equal nu_n(g), hence theta_A^(n^2)=1. Such a twist has 2-power order. It is incompatible with the primitive-17 twist forced above. Therefore every high central simple containing a nonunit invertible has rational dimension ratio.

Writing a for its total pointed multiplicity and t for its total noninvertible multiplicity, its dimension is a+t*d. Since D=8+32d, rationality of the ratio is equivalent to t=4a.

## The indicator balance

Let P be the sum of the four noninvertibles. High rows with nonrational dimension ratio have no pointed constituent, and their first two normalized relative twist traces to Q(sqrt(17)) coincide because the quadratic character of 2 modulo 17 is +1. High rows with rational dimension ratio have t=4a. Low I(1) constituents have twist one, so contribute zero to the difference of the first two traces. These observations give

    sum_{rho noninvertible} nu_2(rho)
       =4 sum_{g nonunit invertible} nu_2(g).

No assumed braiding on the source category, no known-center identification, and no numerical feasibility test enter this identity.

For C4, the right side is ±4 because exactly one nonunit invertible is self-dual. For V4 it is four times a sum of three signs, hence has absolute value at least four. The numbers of self-dual noninvertibles are respectively 2,0,0,2,0 for the five cases in the order stated above. Thus the absolute value of the left side is at most two, a contradiction in every case.

## Independent source checks

I separately loaded the frozen multiplicity-two rank-eight census, sorted tensors by flattened entries, and checked R36 and R412 directly. R36 has pointed labels [0,1,2,7], noninvertibles [3,4,5,6], duality [0,2,1,4,3,6,5,7]. R412 has pointed labels [0,3,4,5], noninvertibles [1,2,6,7], duality [0,2,1,3,4,5,6,7]. Both have center dimension five as associative algebras and the stated Casimir polynomial. The source archive SHA256 is `35a8d69e9af8c873b3003890218a35b38b792abb89c19066f6705bf9c1c1d1ed`.

The proof's pseudo-unitary obstruction is complete. I also independently checked the primary published statement of A. Schopieray, *Categorification of integral group rings extended by one dimension*, J. London Math. Soc. 108 (2023), 1617–1641, Lemma 3.1, DOI 10.1112/jlms.12789 (https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12789). It states the Galois-pseudo-unitary reduction for every fusion ring whose FP dimensions lie in {1,d}, without a commutativity hypothesis. Its hypotheses apply to all five source tensors. This completes the general complex scope; it does not identify pseudo-unitarity with unitarity.
