# R8_3_3472: computer-assisted exclusion

**Conclusion.** The fusion ring R8_3_3472 has no complex fusion categorification.
The argument covers arbitrary complex fusion categories, not only unitary or
pseudo-unitary categories. This is the canonical source-derived evidence package for the new exclusion.

## Replay

From the repository root:

```sh
python3 evidence/r3472_exclusion_20261022/replay.py
```

The full replay reconstructs the sphericalization gate, complete center domains,
all frame exclusions, the surviving-frame identities, the terminal model, and
two independent exact terminal proofs. It requires Python 3, SymPy, NumPy (used
by an existing exact-domain helper), and a C++ compiler for the existing native
sphericalization gate. No optimization solver or network access is needed.
All paths are resolved relative to this package and the repository root.

For the two terminal proofs alone, using only the Python standard library:

```sh
python3 evidence/r3472_exclusion_20261022/terminal/check.py
python3 evidence/r3472_exclusion_20261022/independent/verify.py
```

`replay.py --quick` also checks that the independent certificate is exactly
linked to the primary model and all 1,648 cuts. `--skip-spherical` omits the
separately recorded sphericalization replay. A complete maintenance replay
with `--write` refreshes `verification.json` and `proof_manifest.json`.

The top-level wrapper explicitly runs every child check with assertions
enabled, including when the wrapper itself is invoked with `python -O`.
Direct assertion-based checker invocations reject `-O`.

## Mathematical argument

Write r = sqrt(2), delta = 7 + 5r, and D = 700 + 490r. The simple dimensions
are 1, three copies of delta-1, delta, and three copies of delta+1.

1. **Reduction to the positive spherical case.** The complete signed
   sphericalization search has 84 variables and visits 298,865,973 nodes. Its
   only normalized solution is the original fusion tensor. Consequently every
   complex categorification admits a spherical structure. Of the eight ordinary
   dimension characters, only the FP character and its sqrt(2)-conjugate have
   no zero simple dimensions. Transporting the entire spherical category by
   an automorphism of C therefore gives a pseudo-unitary categorification.
   The independent audit and fresh replay are in
   `provenance/general_complex_reduction.txt` and its replay log.
   That audit identifies and hashes the existing source and prior certificate.

2. **Complete center restrictions.** Central induction gives eight distinct
   twist-one summands of I(1): the unit, pi of dimension 99+70r, and six objects
   of dimension beta = 100+70r. The Galois vacuum argument and character
   inversion force F(pi) = 1 + 2V, where V is the sum of the seven nonunit source
   simples. The induction Gram matrix is computed directly from the tensor.
   Complete exact enumeration gives 372 labelled low frames. Independently
   reconstructed necessary integrality and Galois tests give the complete
   high-restriction domain; the dimension/orthogonality identity removes its
   final impossible 10gamma column, leaving 171 possibilities.

3. **All but one frame orbit are excluded.** The distinguished modular STS
   identities are equivalent to

       sum_Z theta_Z v_Z v_Z^t = L X,

   where X is the exact character table, L consists of the distinguished
   restriction columns, and v_Z is the restriction of a central simple.
   Exact span certificates eliminate 276 frames. Nine verified based-ring
   automorphisms reduce the 96 remaining frames to twelve orbits. Eleven
   exact rational Farkas certificates eliminate eleven of these orbits,
   leaving precisely frames 42, 117, 304, which are equivalent. The phase
   relaxation covers every root of unity by normalized trace to
   Q(sqrt(2), zeta_7 + zeta_7^(-1)); it is not a bounded twist-order guess.
   The independent `frames/replay.py` checks all these certificates.

4. **The surviving frame is rigid enough for an indicator obstruction.** In
   frame 42, an exact Gram null-vector and a sum-of-squares identity force nine
   high beta restriction vectors 2V-e_a+e_c, each with multiplicity two.
   STS forces their twists to be zeta_7^(+k) and zeta_7^(-k). The remaining
   central objects have dimension c*gamma and restriction cV, where
   gamma = 49+35r, c is in {1,2,5}, and sum c^2 = 98.
   Define P_n = sum c^2 theta^n over these remaining objects. Then

       P_1 = -2 - 10r,   P_2 = -2,   P_3 = -2 + 10r.

   The second-indicator signs are forced positive by explicit odd-square
   multiplicity witnesses. For a nonunit source simple, its nth indicator is

       b_i(n) + r*(P_n+2)/20,

   where b_i(n)=1 if 7 does not divide n, and b_i(n) is respectively 6, 7, or 8
   for the three dimension classes if 7 divides n.

5. **The twist domain is finite and complete.** Cauchy's theorem restricts
   exponent primes to {2,5,7}. Modular Galois symmetry makes the weighted twist
   multiset constant on unit-square orbits. Its total weight is 98. For an
   order 2^a*5^b*7^c, the square-orbit size is the product of the local sizes:
   2^max(a-3,0), 2*5^(b-1) if b>0, and 3*7^(c-1) if c>0. The missing local
   factors equal one. Thus a<=9, b<=3, c<=2 and the product is at most 98.
   Enumeration gives exactly 424 orbit types. Their power sums were checked
   independently by exact cyclotomic polynomial arithmetic.

6. **Exact terminal contradiction.** Cyclic rotation on
   Hom(1, X_i^n) has integral eigenvalue multiplicities. Its kth power trace,
   with g=gcd(n,k), is the appropriate Galois conjugate of the indicator of
   X_i^g at order n/g. Applying these identities at orders
   4,5,7,8,10,16,20, together with indicator field membership, gives a
   necessary system of 628 equations in 572 integer variables. All coefficients
   were independently rebuilt with arbitrary-precision arithmetic.

   The terminal certificate consists of 1,648 exact integer bound deductions
   (380 + 486 + 782), followed by a rational separating inequality. Its positive
   separation is

       2717541156573712541191977062303
       / 359103652930042901916159999600.

   This proves that the necessary integer system has no solution. The final
   three equivalent frames are therefore impossible, completing the exclusion.

## Files and provenance

- `verification.json`: compact receipt of the fresh complete replay.
- `proof_manifest.json`: repository-relative SHA-256 closure of proof files and
  every external repository source/data file read by the complete replay.
- `domain/replay.py`: reconstructs the complete high domain from the canonical
  tensor and existing exact arithmetic helpers; no saved center witness is input.
- `domain/enumerate_low.py`: independently generates all 2,142 possible beta
  restrictions, filters to 96 vectors, and exhausts all 372 labelled low frames.
- `frames/replay.py`: checks the 276 span certificates, nine source
  automorphisms, and eleven exact phase exclusions.
- `frames/frame42_gram.py` and `frames/frame42_sts_coeffs.py`: exact surviving
  Gram and twist calculations.
- `model/check.py`: clean arbitrary-precision reconstruction of the 424 orbit
  types and all 628 terminal equations; includes 3,344 direct local Gauss checks.
- `terminal/`: portable standard-library checker, model JSON, exact cuts,
  and final separator.
- `independent/`: separately implemented exact checker and linked certificate.
- `provenance/`: mathematical domain/reduction audits and the stage runner.
- `optional_vipr/`: complete alternative text VIPR proof, its exact MPS input,
  and the official-checker receipt. This is a backup, not a replay dependency.

The canonical tensor is
`site/dist/downloads/fusion-tensors/R8_3_3472.txt`; its normalized JSON SHA-256 is
`33984d45e69ff778e70847def8349abda79ed6c0eaea242a73b533649f9b153a`.
The full replay checks the source-derived necessary system and its arithmetic
contradiction together. The terminal checkers alone certify their supplied
integer system. No failed discovery models, caches, solver executables, or
incomplete certificates are included in this package.

## Primary mathematical references

- V. Ostrik, *On formal codegrees of fusion categories* and *Pivotal fusion
  categories of rank 3* (sphericalization and central induction):
  https://arxiv.org/abs/0810.3242 and https://arxiv.org/abs/1309.4822.
- T. Deshpande, *On centers of bimodule categories and induction-restriction
  functors*, Lemma 4.3 and Corollary 4.5:
  https://arxiv.org/abs/1611.04486.
- P. Bruillard, S.-H. Ng, E. Rowell, Z. Wang, *Rank-finiteness for modular
  categories*, Cauchy's theorem and modular identities:
  https://arxiv.org/abs/1310.7050.
- S.-H. Ng, P. Schauenburg, *Higher Frobenius-Schur Indicators for Pivotal
  Categories*, Theorem 5.1 and its proof:
  https://arxiv.org/abs/math/0503167.
- Z. Liu, S. Palcoux, Y. Ren, G. Vercleyen, *Triangular Prism Equations and
  Categorification*, version 5, Theorem 3.9:
  https://arxiv.org/abs/2203.06522v5.
