# Even cyclic stabilizer characters: new necessary conditions for R6_4_155

This extends the project's odd cyclic Clifford criterion to every even order at least four. Applied to the frozen R6_4_155 candidate, all 1,144 tested blocks pass. This does not construct associators or exclude the ring.

## Hypotheses

Use exactly the anticommuting-stabilizer hypotheses of `prop:stabilizer-rotation`: a spherical fusion category, an order-two invertible h admitting the algebra 1+h, a simple Y fixed on both sides, and normalized left/right h actions that anticommute. The earlier argument supplies an involution a on Y² by inserting a pair of h lines. On the generalized rotation space

`V = Hom(F(Z), Y^n)`, with `E^n = theta_Z^(-1)`,

normalize E by an nth root of theta_Z to E0 with E0^n=1. Let n=2m>=4. The n cyclic translates A_j of the pair insertion satisfy

`A_j²=1; A_j A_(j+1)=-A_(j+1) A_j; A_j A_k=A_k A_j otherwise`.

The boundary translates and these identities follow from the same generalized pivotal-rotation naturality used in the existing odd theorem. E0 cyclically permutes the A_j.

## Even-cycle representation calculation

The adjacency matrix of the even n-cycle over F2 has radical spanned by the two alternating vectors. Accordingly the insertion algebra is a direct sum of four matrix algebras M_r(C), where r=2^(m-1). Its central involutions are the products of the even and odd A_j. Rotation exchanges these involutions. Thus it fixes two simple blocks, and exchanges the other two.

The following three cyclic spectra, and all their cyclic shifts, exhaust the restriction to E0 of irreducible representations of the insertion algebra extended by cyclic rotation. Multiplicities are counts; repeated exponents are retained.

1. For each even-cardinality subset S of {1,3,...,2m-1}, take exponent `-sum(S)/2 mod n`. This character has dimension r.
2. For each odd-cardinality subset S of the same set, take exponent `(1-sum(S))/2 mod n`. This character also has dimension r.
3. For each subset S of {1,...,m-1}, take both exponents `-sum(S) mod n` and `m-sum(S) mod n`. This character has dimension 2r.

Here the two divisions by two are ordinary integer divisions of even numerators. They are not inversions modulo the even number n.

For the fixed blocks, realize A_j as adjacent Clifford bilinears with an antiperiodic boundary. The orthogonal transformation implementing rotation has eigenangles `(2a+1)pi/n`, a=0,...,m-1, and determinant one. Its two half-spin representations give the even and odd subsets above, after scalar normalization to nth power one. Each scalar normalization differs by a cyclic shift.

For the exchanged pair, use a periodic Clifford boundary. The cyclic orthogonal transformation has rotation angles `2pi a/n`, a=1,...,m-1, together with eigenvalues +1 and -1. A pin implementer has eigenvalues proportional to `± exp(i*pi*sum(a*epsilon_a)/n)`. Normalizing its nth power produces the third spectrum. Its opposite-eigenvalue symmetry means its n shifts contain only m distinct characters.

These lists are complete: each fixed matrix block has n possible implementers differing by scalar nth roots, and the exchanged pair has m irreducibles induced from its rotation-square stabilizer. The sum of squared dimensions is

`2*n*r² + m*(2r)² = n*2^n`,

the dimension of the semidirect-product algebra. Consequently the cyclic eigenvalue multiplicity vector of E0 must be a nonnegative integer sum of cyclic shifts of these three spectra. Reversing the rotation convention or changing its normalization only permutes the allowed shifts.

## Exact application

The input is the already published generalized-rotation certificate:

`supplements/rank6/research/frontier/new_research/r155_generalized/certificate.json`

SHA256: `b76cdb3fbc8c4cc6c23d3e177be26d0a74d1adab114069b9e40b04b62678fca7`.

The new check covers even orders 4,6,...,24, noninvertible indices 1 and 2, and all 52 central targets. Every one of the 1,144 spectra has an exact positive character decomposition, saved in `even_clifford_receipt.json`.

`check_even_clifford.py` constructs witnesses using rational linear algebra and a bounded integer correction. Numerical infeasibility is never interpreted as a categorical obstruction. This distinction mattered: unscaled large integer problems produced spurious infeasibility, while exact rational centering yielded positive witnesses. `verify_even_clifford.py` independently replays every witness using only Python integer arithmetic and the standard library; it also rejects a deliberately mutated witness. The replay passes under ordinary and optimized Python.

This proof and replay are new partial work. The candidate still passes, so R6_4_155 remains unresolved.
