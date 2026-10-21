# R1154 and R1795 have incompatible centers

## Theorem and scope

No complex fusion category with Grothendieck ring `R8_3_1154` is categorically
Morita equivalent to a fusion category with Grothendieck ring `R8_3_1795`.
This rules out a common Morita construction for this pair. It does not exclude
either ring individually, and it supplies no categorification of either ring.

The proof uses the previously certified general-to-Galois-pseudo-unitary
reduction for R1154 and the previously certified exhaustive R1154 center domain.
The new step is a comparison with the four scalar formal codegrees 10 of R1795.
The earlier common-center comparison in
`evidence/rank8_next_20261021/models/NEW_CONSTRUCTION_ATTEMPTS.md` used
224 intermediate R1154 patterns. The final three patterns close that comparison.

## Proof

Both rings have Frobenius--Perron dimension

\[
 D=540+240\sqrt5.
\]

First suppose both categories are pseudo-unitary. The complexified R1795 ring
is commutative with eight distinct scalar characters, whose formal codegrees are

\[
 4,\quad 20,\quad 10,10,10,10,\quad
 540+240\sqrt5,\quad540-240\sqrt5.
\]

Ostrik's induction theorem [1, Theorem 2.13] embeds the irreducible
representations of the complexified Grothendieck ring into the simple objects
of the Drinfeld center. The object associated to a representation of formal
codegree \(f\) has categorical dimension \(D/f\). Consequently, the center of
an R1795 categorification contains **four distinct** simple objects of dimension

\[
 \delta=D/10=54+24\sqrt5.
\]

In a pseudo-unitary category these are also their Frobenius--Perron dimensions.
No assertion about their twists is needed here.

For R1154, the exhaustive center restrictions currently leave patterns
`6971`, `8766`, and `8772`. The only permitted center dimension type equal to
\(\delta\) is global type 7, equivalently high-column type 2. Its multiplicity
is zero in all three patterns:

| R1154 pattern | Center rank | Multiplicity of dimension \(54+24\sqrt5\) |
| --- | ---: | ---: |
| 6971 | 23 | 0 |
| 8766 | 21 | 0 |
| 8772 | 29 | 0 |

Morita equivalent fusion categories have equivalent Drinfeld centers, and a
tensor equivalence preserves Frobenius--Perron dimensions. These inventories
are incompatible, proving the claim in the pseudo-unitary setting.

For arbitrary complex categorifications, apply the existing R1154
Galois-pseudo-unitary reduction to the entire hypothesized Morita context.
The same field automorphism preserves the two fusion rings and their Morita
equivalence. Global dimension and Frobenius--Perron dimension are Morita
invariants [2, Theorem 2.15 and Corollary 8.14]. Thus if the transformed R1154
category is pseudo-unitary, its R1795 Morita partner is pseudo-unitary as well.
The preceding contradiction applies. In particular, this argument does not
need a separate general-to-pivotal theorem for R1795.

## Exact certificate and dependencies

`morita_obstruction.py` independently rechecks all eight R1795 characters
against all 512 fusion coefficients, computes their formal codegrees, and
checks both FP dimensions and the absence of \(D/10\) from every final R1154
pattern. Computations use rational pairs for \(\mathbb Q(\sqrt5)\), without
floating-point arithmetic. Its receipt is `morita_obstruction.json`.

The script binds the canonical tensors and all input receipts by SHA-256.
It replays the arithmetic of this final comparison; it does not repeat the
earlier large exhaustive center enumeration or signed-sphericalization
enumeration. Those dependencies are:

* `evidence/rank8_frontier_20261021/central_integrality/general_galois_pu_gate.json`
  for the unrestricted R1154 Galois-pseudo-unitary reduction;
* `evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json`
  for the complete low/high restriction-column domain;
* `evidence/rank8_postpublication_20261021/r1154_galois_review/review.json`
  and its proof for the final three patterns and 25 pair histograms;
* `evidence/rank8_frontier_20261021/global_induction/complete_results/R8_3_1795_atomic_real_sts_h4.json`
  for the character table, verified directly against the canonical tensor here.

Run from the repository root:

```sh
python evidence/rank8_research_20261022/r1154_r1795/morita_obstruction.py
```

## Additional R1154 Galois constraints

This folder also records a stronger necessary Galois test that **does not
exclude any additional pattern or pair histogram**. It constrains the actual
Galois permutation, and supplies compatible exact witnesses for every current
survivor.

Use the earlier center labels \(A_0=1,A_1,\ldots,A_4\), normalized modular
matrix \(s\), and the signed permutation convention
\(\sigma(s)=Gs\), with \(G_{i,\pi(i)}=\epsilon_i\). Here \(\sigma\)
restricts to the nontrivial conjugation of \(\mathbb Q(\sqrt5)\); its extension
to the full cyclotomic field is **not** assumed to have order two.

For every surviving pair histogram, the earlier action reconstruction fixes
the entire rational matrices

\[
 M_2=N_{A_2},\qquad K_3=N_{A_3}-N_{A_1},\qquad
 K_4=N_{A_4}+N_{A_1}.
\]

For any one of these matrices \(M=s\operatorname{diag}(\lambda_j)s^{-1}\),
Galois covariance gives

\[
 M=GQ_MG^{-1},\qquad
 Q_M=s\operatorname{diag}(\sigma(\lambda_j))s^{-1}.
\]

All its eigenvalues at high spectral labels are rational. The five low
spectral columns \(u_0,\ldots,u_4\) are explicitly known, real and orthonormal.
Thus the entire matrix on the right is computable exactly:

\[
 Q_M=M+\sum_{E=0}^4
 (\sigma(\lambda_E)-\lambda_E)u_Eu_E^{\mathsf T}.
\]

On the dimension class of \(A_2\), consisting of \(A_2\) and four high-type-10
objects, \((M_2)_{A_2,A_2}=18\), whereas the corresponding other four
diagonals of \(Q_{M_2}\) equal 16. Its diagonal at \(A_2\) is 18.
Because the signed Galois permutation preserves this dimension class,
diagonal covariance forces \(\pi(A_2)=A_2\).

Similarly \((K_4)_{A_4,A_4}=24\); every other object in its dimension class
(high type 7, when present) has diagonal 23 in \(Q_{K_4}\). Hence
\(\pi(A_4)=A_4\). When the class is a singleton, fixedness already follows
from dimensions.

`galois_fixed_review.py` repeats the complete transport-table enumeration on
all 36 incoming pair histograms with these two fixed-label constraints.
Precisely the previous 25 survive: 7 on pattern 6971, 5 on 8766, and 13 on
8772. It saves a full labelled signed permutation for each.
`forced_galois_probe.py` reconstructs all three matrices for every witness and
checks **every entry** of all three covariance equations, along with the
diagonal uniqueness arguments. All 25 witnesses pass.

These witnesses do not solve the remaining fusion-matrix, modular-data or
pentagon equations. In particular, a failure of one previously chosen witness
would not exclude its pair histogram: alternative permutations must be
considered, and they exist here.

```sh
python evidence/rank8_research_20261022/r1154_r1795/galois_fixed_review.py > evidence/rank8_research_20261022/r1154_r1795/galois_fixed_review.json
python evidence/rank8_research_20261022/r1154_r1795/forced_galois_probe.py > evidence/rank8_research_20261022/r1154_r1795/forced_galois_probe.json
```

The independent effect enumeration in `galois_fixed_a2.py` also fixes **both**
\(A_2\) and \(A_4\), despite its historical filename. It independently gives
the same 25 surviving histogram identifiers; the transport reviewer above
additionally supplies expanded witnesses used by the covariance replay.

## Primary references

1. V. Ostrik, *Pivotal fusion categories of rank 3*, Moscow Mathematical
   Journal **15** (2015), 373--396, Theorem 2.13;
   [arXiv:1309.4822](https://arxiv.org/abs/1309.4822).
2. P. Etingof, D. Nikshych, V. Ostrik, *On fusion categories*, Annals of
   Mathematics **162** (2005), 581--642, Theorem 2.15, Corollary 8.14 and
   Proposition 8.23;
   [arXiv:math/0203060](https://arxiv.org/abs/math/0203060).
   The center equivalence used for Morita invariance also appears in the proof
   of Corollary 8.14.

The modular Galois permutation input is exactly the one cited and reviewed in
`evidence/rank8_postpublication_20261021/r1154_galois_review/PROOF.md`.
