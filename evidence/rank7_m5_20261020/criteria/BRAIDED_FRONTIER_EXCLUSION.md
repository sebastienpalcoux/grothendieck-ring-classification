# The two general survivors have no braided categorification

**Scope.** Neither `R7_5_3895` nor `R7_5_5039` is the Grothendieck ring of a
braided fusion category over an algebraically closed field of characteristic
zero. This does **not** exclude a fusion-category categorification without a
braiding. Both rings therefore remain on the general survivor list.

All indices below are the zero-based indices of the pinned census tensors.
The exact executable proof is `verify_braided_frontier.py`. It first replays
`../sqrt5_reduction/verify_reduction.py`, binds its tensor hashes to the two
braided tests, and then checks the arguments below. The computation uses no
floating-point comparison, numerical optimizer, or Python `assert`.

## Reduction from an arbitrary braiding to positive modular data

The independently verified signed-quotient/character reduction proves that
every categorification of either ring is spherical and is Galois conjugate
to a pseudo-unitary category; see `../sqrt5_reduction/PROOF.md`. Applying the
same field automorphism to a braiding preserves its defining identities.
Consequently a braided categorification would give a pseudo-unitary braided
categorification of the same based ring.

Direct closure under multiplication and duality shows that **each of the six
nonunit basis elements generates the entire ring**, for each tensor. Thus the
Müger center of a braided categorification, being a fusion subcategory, must
be either Vec or the entire category. The latter would make the category
symmetric. Deligne's theorem on symmetric fusion categories implies integral
Frobenius--Perron dimensions in that case, whereas both rings have the simple
dimension `5+2 sqrt(5)`. The Müger center is therefore Vec. The canonical
positive spherical structure of a pseudo-unitary category makes this a
modular category.

This argument does not assume a pivotal structure for the original putative
categorification. Its existence and the positive Galois reduction are supplied
by the separately replayed structural result.

## R5039: a missing modular formal codegree

Write `s=sqrt(5)` and `D=720+320s`. The positive dimensions, in tensor order,
are

```
(1, 5+2s, 5+2s, 8+4s, 8+4s, 10+4s, 9+4s).
```

In a modular category each simple object of dimension `d_i` determines a
character with formal codegree `D/d_i^2`. Here

```
D/(5+2s)^2 = 16,
```

but the exact Casimir characteristic polynomial is

```
(x-8)^3 (x-5)^2 (x^2-1440x+6400),
```

which does not vanish at 16. This contradiction excludes pseudo-unitary
modularity, and the preceding reduction excludes every braiding.

## R3895: exhaustive modular balancing and a second-indicator contradiction

The positive dimensions are

```
d=(1, 5+2s, 5+2s, 10+4s, 8+4s, 8+4s, 9+4s),
D=720+320s=(20+8s)^2.
```

Every basis element is self-dual. A modular character assignment `p` must
match formal codegrees `f_{p(j)}=D/d_j^2`, and then its normalized S matrix is
forced:

```
S_ij = chi_{p(j)}(X_i) d_j / (20+8s).
```

The exact complete character table gives precisely four bijections `p`.
All four forced matrices are symmetric and real orthogonal. Their entries
are in `K=Q(sqrt(5))`; the nontrivial automorphism of K acts by a signed row
permutation whose underlying permutation is

```
pi=(0 6)(4 5),
```

fixing indices 1, 2, and 3. The exact matrices and signs are in
`braided_frontier_normal.json` and `R7_5_3895_modular_probe.json`.

### Completeness of the finite twist search

For a general modular category the correct Galois identity for its actual
twists is

```
theta_{pi_sigma(i)} / theta_{pi_sigma(0)} = sigma^2(theta_i).
```

The denominator must be retained: no trivial-anomaly assumption is made.
This is Dong--Lin--Ng, Proposition 4.7, equation (4.12).

The categorical Cauchy theorem restricts prime divisors of the twist order
to 2 and 5, since `D=80(9+4s)` and `9+4s` is an algebraic unit. For any
automorphism fixing K the character permutation is the identity, so its
square fixes every twist. If a twist had 2-part at least 16, take a cyclotomic
automorphism with exponent 3 on the 2-part and 1 on the 5-part. It fixes K,
but the 2-adic valuation of `3^2-1` is only 3. If a twist had 5-part at least
25, use exponent 6 on the 5-part and 1 on the 2-part; it fixes K, but the
5-adic valuation of `6^2-1` is only 1. Both are contradictions. Thus every
twist is a fortieth root of unity.

Take the automorphism with exponent 17 modulo 40. It is nontrivial on K and
its square has exponent 9 modulo 40. Writing
`theta_i=zeta_40^{k_i}`, the Galois identity becomes

```
k_{pi(i)} = k_6 + 9 k_i (mod 40),   k_0=0.
```

All solutions, without omission, have

```
k_6=8c,                   c in {0,1,2,3,4},
k_1,k_2,k_3 = -c (mod 5), each with 8 choices modulo 40,
k_4 arbitrary modulo 40,
k_5 = 8c+9k_4 (mod 40).
```

There are exactly `5*8^3*40=102400` candidates per S matrix. The script also
checks all seven Galois congruences on every generated candidate.

It imposes the balancing identity

```
theta_i theta_j (sqrt(D) S_ij) = sum_k N_ij^k d_k theta_k
```

for every nonunit pair `i<=j`. All arithmetic is exact polynomial reduction
modulo `Phi_40`, with `sqrt(5)=1+2(zeta_40^8+zeta_40^32)`. The vectorized
integer sieve has explicitly checked overflow bounds. Exactly four balanced
twist assignments remain. With `zeta=zeta_5`, they are the conjugate pairs

| Twists in tensor order | Exact second indicators |
| --- | --- |
| `(1,-1,-1,1,zeta^2,zeta^3,1)` and its conjugate | `(1,5,5,10,9,9,9)` |
| `(1,-1,-1,-1,zeta,zeta^4,1)` and its conjugate | `(1,1,1,2,1,1,1)` |

The indicators are evaluated with the modular formula

```
nu_2(X_k) = (1/D) sum_{i,j} N_ij^k d_i d_j (theta_i/theta_j)^2.
```

For a self-dual simple object its second Frobenius--Schur indicator is +1
or -1. Index 3 instead gives 10 or 2 in every remaining case, a
contradiction. No Vafa-equation sufficiency or existence inference is used:
all candidates satisfying the necessary balancing conditions already fail
another necessary condition.

## Replay and controls

From the repository root:

```
python evidence/rank7_m5_20261020/criteria/verify_braided_frontier.py --output evidence/rank7_m5_20261020/criteria/braided_frontier_normal.json
python -O evidence/rank7_m5_20261020/criteria/verify_braided_frontier.py --output evidence/rank7_m5_20261020/criteria/braided_frontier_optimized.json
```

The indicator implementation is checked against the Fibonacci modular
category, which gives `(1,1)`, and the semion category, which gives `(1,-1)`.
The latter ensures that the implementation and exclusion allow the negative
second indicator. Raw tensor hashes, fusion closures, all S assignments,
balancing-sieve counts, surviving twists, and exact indicators are recorded.
The wrapper does not rewrite the general census or any accepted ledger.

## References and exact source locations

- Etingof--Gelaki--Nikshych--Ostrik, *Tensor Categories*, Corollary 9.9.11
  (symmetric fusion categories are integral), Proposition 9.5.1 (canonical
  positive spherical structure), and Proposition 8.20.12 (trivial Müger
  center is equivalent to nondegeneracy). The author's final text is at
  <https://math.mit.edu/~etingof/egnobookfinal.pdf>.
- Ostrik, *On formal codegrees of fusion categories*, proof for modular
  categories in section 3 (in particular `f_i=1/S_0i^2`):
  <https://arxiv.org/pdf/0810.3242>.
- Bruillard--Ng--Rowell--Wang, *Rank-finiteness for modular categories*,
  Theorem 3.9, categorical Cauchy theorem:
  <https://arxiv.org/pdf/1310.7050>.
- Dong--Lin--Ng, *Congruence Property in Conformal Field Theory*,
  Proposition 4.7, equation (4.12), PDF page 26:
  <https://arxiv.org/pdf/1201.6644>.
- Ng--Schauenburg, *Frobenius--Schur Indicators and Exponents of Spherical
  Categories*, Theorem 7.5 (modular indicator formula), Theorem 7.7 (twist
  order equals FS exponent), and the second-indicator discussion in section
  7: <https://arxiv.org/pdf/math/0601012>.
