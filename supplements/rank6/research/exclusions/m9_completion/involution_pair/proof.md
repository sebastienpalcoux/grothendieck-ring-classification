# General exclusion of R6_9_529 and R6_9_2455

Both tensors admit no complex fusion categorification. The proof combines independently replayed pseudo-unitary exclusions with the following general sphericalization reduction. All files here are separate from the read-only published package.

## Common tensor data

Use basis \(1,g,x,y,a,b\), corresponding to original indices \(0,3,1,2,4,5\) for 529 and \(0,1,2,3,4,5\) for 2455. We have \(g^2=1\), \(gx=y\), \(ga=a\), \(gb=b\). In 529, \(x^*=y\); in 2455 all objects are self-dual. The only nonzero multiplicities are 1, 7, 8, 9.

The FP dimensions are \((1,1,d,d,d-1,d+1)\), \(d=16+\sqrt{257}\), \(d^2=32d+1\). Formal codegrees are \(4,4,8,8,D,D'\), where
\[
D=2056+128\sqrt{257}=8\sqrt{257}(16+\sqrt{257}),\qquad DD'=64\cdot257.
\]
The regular Casimir trace is 4136. Every character outside the quadratic FP orbit has a zero simple dimension.

Tensor SHA-256 values: 529 has 84f6db29c364e47a967ce6bf7da26bf37239fde9ac6480785e9d639814fa6c65; 2455 has 02083204d03d8084f4e82fd397d1c6545936092ffe4074774901eb8201785440.

## Exact pseudo-unitary certificates

Let \(B\) be the central induction Gram matrix, \(u=(1,0,\ldots,0)^t\), \(M=B-uu^t\). Given one of the other five low columns \(c\), their other four columns sum to \(w=B_{\bullet0}-u-c\). Cauchy and positivity of the remaining high Gram matrix give
\[
M-cc^t-\tfrac14ww^t\succeq0.
\]
The matrix \(M\) is positive definite, checked by exact leading principal minors. If \(A=qM^{-1}\) is integral and \(q>0\), this is equivalent to the exact two-by-two test
\[
q-c^tAc\ge0,\quad 4q-w^tAw\ge0,\quad
(q-c^tAc)(4q-w^tAw)\ge(c^tAw)^2.
\]

This complete necessary pruning reduces the low column counts from \((817,833,833,217,217)\) to \((10,9,9,10,10)\) for each tensor. Full Cartesian enumeration, modulo only permutations of equal-codegree columns, gives 497 frames. The existing exact Gram/moment criterion rejects 406. This leaves 91 frames before character reciprocity.

The publication verifier first applies complete exact character reciprocity, leaving 31 of the 91 frames for 2455 and six for 529. It then uses every possible second-indicator assignment: all 32 assignments for the five self-dual nonunits of 2455, and all eight assignments for the three self-dual nonunits of 529 (the nonselfdual pair has indicator zero). All 992 systems for 2455 and all 48 systems for 529 have exact integral Farkas rays. No adjoint-indicator parity reduction is used.

The portable publication verifier is verify.py. It reads frozen full tensors bound to hard-coded digests, regenerates complete original column domains, checks the Cauchy pruning, independently enumerates the small Cartesian domain, reconstructs every individual indicator system, and checks every ray. Optimizers are disabled by replacement functions that raise exceptions. The source package is supplied by --source; it contributes only read-only mathematical primitives. The verifier does not read any unresolved ledger.

This bundle includes only the complete unrestricted-indicator certificates; discovery intermediates are not required.

For completeness, any pivotal structure on either ring is spherical: nonzero pivotal dimension of \(a\) and \(ga=a\) force \(\dim(g)=1\); then \(gx=y\) makes the only possible dual pair have equal dimensions. The existing exact sphere_certificate/check_sphere functions check that every possible spherical character belongs to the FP Galois orbit. Thus spherical categorification would have a pseudo-unitary Galois conjugate and is excluded.

## General signed reduction

Assume a general categorification and apply the standard sphericalization used in the supplied package. Its oriented signed quotient \(T\) has coefficients congruent to the original \(N\) modulo 2, bounded in magnitude by \(N\), obeying all oriented Frobenius and associativity identities. It has a nonzero dual-invariant dimension character. Unit- and dual-preserving sign gauges correspond to changing the chosen lifts.

The fixed objects \(a,b\) force left and right action signs of \(g\) to equal its dimension. Gauge \(g\) to make this dimension \(+1\). In 529, dual invariance makes \(d_x=d_y\ne0\), so both \(gx=y\) and \(xg=y\) have positive sign. In 2455 an independent sign gauge on \(x,y\) achieves the same normalization. Thus \(g\) is central with the unsigned original action.

Its \(+1\) and \(-1\) rational algebra components have dimensions four and two. The dimension character lies in the positive component. A semisimple complex algebra of dimension four admitting a one-dimensional representation has no matrix block of dimension at least four, so it is commutative. The negative component is commutative as well. The full signed algebra is therefore commutative; so is the sphericalization algebra, the direct sum of the original and signed quotients.

Let \(K\) be the dimension-character field, and write
\[
\Delta=2+2x^2+a^2+b^2,\qquad \theta=\Delta/8.
\]
The symbols here are algebraic-integer dimensions with \(y=x\). Central induction in the sphericalization gives \(\Delta/f\in\mathcal O_K\) for every original formal codegree \(f\): its global dimension and the original-sector codegrees are both doubled, so the two factors cancel. Consequently
\[
\theta\in\mathcal O_K,\qquad \theta/\sqrt{257}\in\mathcal O_K.
\]
For the second assertion use \(\Delta/D\) integral and the unit \(16+\sqrt{257}\), of norm \(-1\). The dimension-field condition gives \(E=\mathbb Q(\sqrt{257})\subset K\). The positive algebra component has dimension four, so \([K:\mathbb Q]=2\) or 4.

Cyclotomicity for the commutative sphericalization implies that \(K\) is abelian. Global dimensions and all their conjugates are positive, and \(\theta\) is a \(d\)-number: global dimensions are \(d\)-numbers, and rational rescaling preserves this property. The signed Casimir obeys
\[
\operatorname{Tr}(C_T)=\sum_{i,j,k}(T_{ij}^k)^2\le4136.
\]
All character components contribute positive formal codegrees, so this bounds the active dimension-component trace.

## Quadratic dimension field

Here \(K=E\). Integrality of \(\theta/\sqrt{257}\) implies that \(\operatorname{Tr}(\Delta)\) is a positive multiple of 2056. The trace bound leaves 2056 or 4112.

Modulo two, the signed table at \(g=1,x=y\) gives \(x^2=1\), \(a^2=b^2=0\). Since \(257\equiv1\pmod8\), the ring \(\mathcal O_E/2\mathcal O_E=\mathbb F_2\times\mathbb F_2\) is reduced. Consequently, at each of the two embeddings into the 2-adic integers, the dimension \(x\) is odd, while \(a=2a_0\) and \(b=2b_0\). Integrality of \(\theta=\Delta/8\) forces \(a_0^2+b_0^2\) to be odd, hence 1 modulo 4. Since an odd square is 1 modulo 8,
\[
\Delta=2+2x^2+4(a_0^2+b_0^2)\equiv8\pmod{16}
\]
at both embeddings. Thus \(\theta\) is odd at both embeddings, its trace is even, and \(\operatorname{Tr}(\Delta)\) is divisible by 16. The value 2056 is impossible, leaving 4112.

The other four signed characters have positive codegrees, so the full trace exceeds 4112. Decreasing any permitted coefficient magnitude 7, 8, or 9 lowers its square by at least \(7^2-5^2=24\); magnitude one cannot decrease. Any unsaturated coefficient would give full trace at most \(4136-24=4112\), a contradiction. All coefficients are saturated.

The saturation_check function in verify.py exhausts every oriented endpoint domain, fixing positive \(g\)-action. All active bound-one orbits are exactly those \(g\)-action orbits. The inherited exact engine visits 1786 nodes for 529 and 2886 for 2455, finding exactly eight associative signed tensors in each case. Each is validated against every ordered associativity/Frobenius equation and each has an explicit gauge to the original tensor. See saturated_signs.json.

A gauge-original signed quotient has one lift of each simple closed under tensor products. These form a fusion subcategory of the sphericalization mapping tensor-equivalently onto the original category, hence transporting a spherical structure. This contradicts the scoped certificates.

## Quartic dimension field

The positive rational algebra component is now the field \(K\). The canonical trace of its idempotent \(e_+=(1+g)/2\) is \(1/2\), so the formal-codegree trace decomposition yields
\[
\operatorname{Tr}_{K/\mathbb Q}(1/\Delta)=\tfrac12,\qquad
\operatorname{Tr}_{K/\mathbb Q}(1/\theta)=4.
\]
Also \(\operatorname{Tr}(\theta)\le4136/8=517\).

The element \(\theta\) generates \(K\). If quadratic of norm \(n\), reciprocal trace forces its quadratic trace to be \(2n\), hence full trace \(4n\). Its norm in \(K\) is \(n^2\), divisible by \(257^2\), so \(n\ge257\), contradicting 517. If rational, reciprocal trace forces \(\theta=1\), impossible since \(\theta/\sqrt{257}\) is integral.

Relative trace to \(E\) gives \(\operatorname{Tr}(\theta)=257u\), \(u=1\) or 2. Its norm is \(257^2v\), \(v\) a positive integer. Each product of two conjugates divided by 257 is integral, so the second coefficient is a multiple of 257. Reciprocal trace fixes the third. The minimal polynomial is
\[
t^4-257u\,t^3+257w\,t^2-4\cdot257^2v\,t+257^2v.
\]
The \(d\)-number divisibilities and Maclaurin inequalities imply
\[
v\mid257^2u^4,\quad v^2\mid w^4,\quad
1\le v\le\lfloor257u^3/64\rfloor,\quad
1\le w\le\lfloor3\cdot257u^2/8\rfloor.
\]
Thus \((u,v)\) is \((1,1)\) or \((2,1),(2,2),(2,4),(2,8),(2,16)\). Exactly 1057 triples remain.

An abelian quartic containing \(E\) is biquadratic or cyclic quartic. Its polynomial discriminant is a square in the first case, or 257 times a square in the second, since \(E\) is then the unique quadratic subfield.

The quartic_check function in verify.py independently exhausts the 1057 polynomials with exact rational Sturm sequences and resultant discriminants. There are 736 without four positive roots; the other 321 have discriminant neither a square nor 257 times a square, checked using integer square roots. This replay uses no approximation, factorization, Galois-group discovery, or numerical optimizer. Optimized replay takes under three seconds. The verifier regenerates this complete polynomial domain directly. This excludes the quartic case and completes the general proof.

## Literature inputs

New arguments are the Cauchy column prune, quadratic trace parity, and finite quartic polynomial rejection. Sphericalization, codegree divisibility, cyclotomicity, central relative traces, and character reciprocity are inherited inputs used with their checked hypotheses. No timeout was treated as a completed criterion.

Primary references browsed:

- Etingof, Nikshych, Ostrik, On fusion categories: https://arxiv.org/abs/math/0203060 and https://annals.math.princeton.edu/2005/162-2/p01.
- Ostrik, On formal codegrees of fusion categories: https://arxiv.org/abs/0810.3242.
- Ostrik, Pivotal fusion categories of rank 3: https://arxiv.org/abs/1309.4822.
- Ng, Schauenburg, Frobenius–Schur indicators and exponents of spherical categories: https://arxiv.org/abs/math/0601012.
