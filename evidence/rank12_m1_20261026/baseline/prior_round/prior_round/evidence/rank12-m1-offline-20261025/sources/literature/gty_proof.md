# Complete resolution of the 14 rank-10 generalized Tambara–Yamagami rings

All labels refer to the original input basis, with tensor N[i,j,k]. This work uses Jesse Liptrap, *Generalized Tambara–Yamagami categories*, [arXiv:1002.3166v2](https://arxiv.org/html/1002.3166v2), Definition 4.3, Theorem 4, Lemma 4.11 and the reconstruction formulas in Lemma 5.4. It is an exact constructive application of an existing classification theorem; novelty of individual categories is not claimed.

| Result | Input IDs R10_1_… |
|---|---|
| Explicit unitary fusion categories | 14, 57, 68, 79, 97, 100, 148, 150, 154, 167, 183 |
| No complex fusion category | 118, 122, 180 |

## Setup and exact equations

For every ring listed here there are eight invertibles S, two noninvertibles M, and a common left/right stabilizer H of order four. Products of noninvertibles have only invertible summands. Thus these are feudal fusion rules in Liptrap's terminology. H is abelian in every case.

Write x_m(a,b)=χ(a,b)(m), u_m(a,b)=υ(a,b)(m). Choose τ(m)=1/2. The two defining identities reduce to

\[
x_{m^*}(b,a)=x_{amb}(a,b),
\]
\[
\frac{u_m(a,b)}{u_{mc^{-1}}(a,b)}x_m(ab,c)
=x_m(a,c)x_{a^{-1}m}(b,c).
\]

Here a,b,c range over S and m over M. Set x and u equal to 1 when either group argument is the identity. The restriction of x_m to H×H must be a nondegenerate symmetric bicharacter. Also |H|τ(m)τ(m*)=1. These conditions are sufficient for a fusion category by Theorem 4.

The generator encodes x,u as powers of ζ16. Its 196 phase variables satisfy 1152 quasisymmetry/biderivation identities (before removing redundant zero equations). `gty_liptrap_certificates.json` gives every exponent in the original basis. `gty_verify.py` independently evaluates all identities, checks bicharacter multiplicativity, symmetry and distinct character rows, and verifies the normalization.

## Why the affirmative models are unitary

Liptrap's reconstruction has scalar recouplings and four-by-four recoupling blocks. Every scalar recoupling is a product or ratio of χ,υ values and τ ratios, hence has modulus one in the supplied certificates. Each nontrivial block is, after multiplication of rows and columns by phases, the matrix

\[
\left(\frac{1}{2\,x_m(y,x)}\right)_{x,y\in H}.
\]

Character orthogonality and nondegeneracy make this matrix unitary. This proves unitarity of the reconstructed associator, yielding a unitary fusion category with the specified fusion rules.

As a separate exact check, the verifier reconstructs γ from Lemma 5.4 in the original basis:

\[
\gamma(c,a)(m)=\frac12\frac{u_{(a^{-1}m)^*}(c^{-1},c)}{u_{a^{-1}mc^{-1}}(a^{-1},a)x_m(a,c)}.
\]

It checks all eight four-by-four coset blocks per ring. Every inner product is evaluated exactly in Q(ζ16), using ζ16^8=-1. All 88 blocks are unitary. The result is recorded in `gty_verification.json`.

## Why the three negative cases are excluded over C

The finite ζ16 search alone proves nothing negative. We instead use exact integer monomial relations, without restricting unknown complex numbers to roots of unity.

Suppose a complex fusion category existed. Its two noninvertibles are exchanged by duality in each of the three negative cases. Lemma 4.11 allows τ to be constant, with value ±1/2; the sign cancels from the displayed identities. Normalization follows from the fusion-system triangle identities. Each bicharacter on H has values among fourth roots of unity, because the exponent of H divides four. Enumerate all possible nondegenerate symmetric bicharacters independently at the two elements of M: 16 pairs when H=C2×C2 (case118), and four pairs when H=C4 (cases122,180).

For each pair, write the equations multiplicatively as z^A=i^b, where z contains arbitrary nonzero complex unknowns and A is an integer matrix. An integer row vector y satisfying

\[
yA=0,\qquad yb\not\equiv0\pmod4
\]

is a contradiction: multiplying the equations with exponents y gives 1=i^(yb)≠1. The search found such a y for every pair. The witnesses involve only three to ten original equations. This is an algebraic proof valid for arbitrary nonzero complex values; no bound on phases or search completeness is used.

`gty_exact_obstructions.json` stores A,b and all y. `gty_verify_obstructions.py` independently rebuilds the equations, exhaustively enumerates the symmetric bicharacters, checks each yA=0 as an equality over Z and each yb mod4 as nonzero, and verifies every candidate pair is covered. `gty_obstruction_verification.json` also decodes each witness into named original equations.

To reproduce:

```bash
python work/literature/gty_liptrap.py
python work/literature/gty_verify.py
python work/literature/gty_exact_obstruction.py
python work/literature/gty_verify_obstructions.py
```

Dependencies: Python, NumPy. The checks are exact integer arithmetic; no numerical tolerances are used.
