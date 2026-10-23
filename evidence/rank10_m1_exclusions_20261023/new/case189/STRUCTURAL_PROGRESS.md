# R10_1_189: theoretical reductions (not a classification decision)

The source tensor in `research/catalogue.json` has the following normal form. Put `g=X_1` and `x=X_9`. Then `g^5=1`, `gx=xg`, `x*=x`, and

    x^2 = 1 + (g+g^2+g^3+g^4)x.

The source order of `(1,g,g²,g³,g⁴,x,gx,g²x,g³x,g⁴x)` is `[0,1,8,7,2,9,4,6,5,3]`.

Set `d=2+sqrt(5)`, so `d²=1+4d`, and `D=5(1+d²)=10+20d`. This is a nonuniform two-orbit fusion ring, with trivial stabilizer and identity commutation automorphism. Standard Haagerup–Izumi results requiring inversion and uniform noninvertible coefficients do not apply.

By Schopieray, *Categorification of integral group rings extended by one dimension*, JLMS108(2023), 1617–1641, Lemma3.1, hypothetical complex categorifiability reduces to a pseudo-unitary categorification.

## Sign caution in the cited Galois lemma

For a central simple of dimension `a+bd`, modular Galois symmetry gives the SQUARED identity

    dim(sigma_hat Z)^2 = (a+(4a-b)d)^2.

For `a>0`, positivity of the integer coefficients of a restriction forces the positive displayed sign and `0<=b<=4a`. For `a=0`, the NEGATIVE sign is allowed and the new dimension is again `bd`. Consequently the printed Lemma3.6 must not be used to exclude all central simples whose restrictions contain only noninvertibles. The same paper explicitly employs these objects in §4.1.

## Exact induction Gram matrix

In the normal order `(g^i, g^i x)`, `i=0,...,4`, the matrix is

    B_GG = 10 I,
    B_GX = 5(J-I),
    B_XX = 15 I + 15 J.

Thus a central simple whose restriction contains an invertible can contain only copies of ONE invertible `g^i`. If this multiplicity is `a`, its multiplicity in `I(g^i)` is also `a`.

## Every I(g^i) is multiplicity-free

For `i=0` this is the standard commutative-fusion-ring induction theorem.
For `i != 0`, Schopieray Proposition3.8 (or the pseudo-unitary triangle-inequality proof using Ng–Schauenburg indicators) makes all fifth powers of the constituent twists equal. Hence their twists belong to one coset of the fifth roots of unity. The first four twist moments vanish since `Hom(1,(g^i)^j)=0` for `j=1,...,4`. Fourier inversion forces the total dimension in each of the five twist eigenspaces of `I(g^i)` to be `D/5=2+4d`.

A constituent with invertible multiplicity `a` contributes `a(a+bd)` to its eigenspace. Comparing rational coefficients gives `sum a²=2`. Therefore each eigenspace consists of exactly two distinct central simples, each with `a=1`. Thus each `I(g^i)` contains exactly ten central simples, and their five pairs have noninvertible totals adding to4.

The five induction blocks are disjoint. There are exactly fifty central simples whose restrictions contain invertibles; any other central simples have pure noninvertible restrictions.

## Full Galois restriction transform

For the automorphism `zeta5 -> zeta5²`, write a restriction vector as `(a_i,b_i)` in the normal order. The exact transform obtained from the scalar character table `H_chi,i=chi(i)/f_chi` is

    a'_i = a_(3i),
    b'_i = sum_j a_j - a_(3i) - b_(3i),

where indices are modulo5 and the central Galois sign is positive when any `a_i>0`, negative for pure noninvertible restrictions. Thus every constituent of `I(g^j)` restricts as `g^j + sum_{i in S} g^i x`, where `S` is a subset of the four indices other than `j`. In particular these restriction columns are binary. Pure columns transform by permutation (after the negative Galois sign) and are not ruled out.

The fifty columns containing invertibles contribute20 to each diagonal entry of `B_XX`. Hence the pure restriction columns have total squared coordinate sum10 in each of the five coordinates, total50.

## Pure dimensions

A pure simple has dimension `bd`, with positive integer `b`. Its modular formal codegree is

    dim(Z(C))/(bd)^2 = D²/(b² d²) = 500/b².

This is a rational algebraic integer, so `b²` divides500 and `b` lies in `{1,2,5,10}`. Combining with the preceding diagonal budget bounds each coordinate by3. A `b=10` column, if present, must be `(2,2,2,2,2)` when its Galois orbit budget is imposed; it is NOT excluded merely by the diagonal bounds.

## Third indicators

The source rules give `dim Hom(1,x³)=0`, and `dim Hom(1,(g^i x)³)=1` for `i != 0`. Thus the respective third indicators are0 and cubic roots of unity. The Cauchy theorem confines the primes in the center twist conductor to2 and5, so the latter indicators must actually equal1. This may be combined with the preceding five twist pairs and pure-column constraints, but no contradiction or categorical construction has yet been established.

## Pointed associator and absence of braidings

The theorem in `POINTED_ASSOCIATOR.md` proves that the pointed associator class must vanish in `H³(C5,C×)`. Its proof uses primitive25th twists under a hypothetical nonzero class, Galois orbits of equal restrictions, and a two-by-two Gram-minor contradiction. Both the conceptual steps and a stronger exact check allowing all35 I(1) singleton count compositions were independently audited. This is a necessary condition, not an exclusion of the ring.

There is no braided categorification of this ring. Schopieray's *Irrational braided generalized near-groups*, Theorem3.6, classifies the nonintegral braided case as a pointed factor times either Fibonacci/Yang–Lee type or the rank4 adjoint sl2 level6 type. Their noninvertible Frobenius–Perron dimensions are `(1+sqrt5)/2` and `1+sqrt2`, respectively, neither of which is `2+sqrt5`. The theorem applies because the invertible group acts transitively on the five noninvertibles and the global dimension is irrational. This statement does not rule out a nonbraided fusion category.

## Precise open step

The regular algebra `A=sum_i g^i` now exists. Its category of right modules has two simple objects and the action of x has matrix `[[0,1],[1,4]]`. It is only a module category in general: no central structure on A has been established, so this matrix cannot be treated as the multiplication rule of a rank2 fusion category. In particular Ostrik's rank2 classification cannot be applied to it. Establishing an appropriate central structure, finding a different obstruction, or constructing a nonbraided category remains necessary. The necessary Gram/Galois/dimension constraints alone admit integer solutions; the exploratory file `gram_probe_witness.json` is one such solution and is not a modular datum or categorical model.

The stronger result in `MORITA_REDUCTION.md` proves that the A-bimodule dual has this same based ring. It classifies all four possible rings with FP dimension profile `1^5,d^5`; two are excluded because their quartic formal codegrees would give central simple dimensions outside Q(sqrt5), and one contains the forbidden rank2 fusion subcategory `x²=1+4x`. This proof does not establish tensor equivalence to the original category or any central lift. Its elementary arithmetic is checked by `verify_morita_reduction.py` and was independently audited.

## A finite bound on the remaining twists

The Frobenius–Schur exponent of a hypothetical category divides1600. Here is a bound independent of a numerical search. The categorical Cauchy theorem restricts the primes in the exponent to2 and5, since `Norm(D)=500`. All central simples containing an invertible in their restriction now have twists of order dividing5: the unit induction has twist1, and the pointed associator theorem makes `nu5(g)=1` for the other four inductions.

For every fixed pure noninvertible restriction column, the number of distinct central simples having that column is at most10: some coordinate is a positive integer, and the residual diagonal Gram budget at that coordinate is10. Any cyclotomic automorphism fixing zeta5 fixes the full scalar character matrix H, so it fixes the complete restriction column. Its sign is positive because it fixes D and all simple dimensions, which lie in Q(sqrt5). If the twist has exact order `2^a*5^b`, the distinct twist powers obtained by squared automorphisms in this kernel number

    2^max(a-3,0) * 5^max(b-1,0).

This count is the size of the squares in the units modulo `2^a`, multiplied by the size of the subgroup congruent to1 modulo5 in the units modulo `5^b`. It is at most10, hence `a<=6` and `b<=2`. All individual twist orders, and therefore their least common multiple, divide `2^6*5^2=1600`. The stronger individual-order inequality above must still be observed. This bound is a necessary condition; no solution or contradiction of the remaining twist equations has been established.

## Sources

- Andrew Schopieray, *Categorification of integral group rings extended by one dimension*, DOI10.1112/jlms.12789, especially Lemma3.1, Eq.(30)–(33), Proposition3.8, and §4.1. https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.12789
- Bruillard–Ng–Rowell–Wang, *Rank-finiteness for modular categories*, Theorem3.9. https://arxiv.org/html/1310.7050v3
- Andrew Schopieray, *Irrational braided generalized near-groups*, Canadian Mathematical Bulletin66(2023), 1255–1268, Theorem3.6. https://doi.org/10.4153/S0008439523000334

No model or exclusion is claimed in this note.
