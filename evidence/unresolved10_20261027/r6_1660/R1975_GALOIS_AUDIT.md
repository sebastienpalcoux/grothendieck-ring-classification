# Independent audit: R1975 Galois-unit restriction on its uniform Morita ring

**Verdict: the formal-codegree calculation and forced central restriction
are correct.** This note does not audit the separate relative-center parity
obstruction. It uses the previously accepted categorical Morita reduction
and source signed Galois-to-pseudo-unitary gate as explicit dependencies.

Let `G=D8`, `H=Z(G)`, `Q=G/H=V4`. In the uniform rank-twelve ring the four
noninvertibles satisfy

\[
 gX_q=X_qg=X_{q+gH},\qquad
 X_pX_q=\sum_{gH=p+q+\alpha}g+2\sum_{t\in Q}X_t.
\]

Thus `X_q*=X_(q+α)` and `d=FPdim(X_q)=4+3 sqrt(2)` satisfies
`d²=2+8d`. The global FP dimension is

\[
 D=8+4d^2=144+96\sqrt2,
 \quad D'=144-96\sqrt2,
 \quad D/D'=17+12\sqrt2=1+4d.
\]

## Complete irreducible calculation without diagonalizing a matrix

For a scalar irreducible, the restriction to `G` is a character `ψ` of
`Q`, and `X_q` acts by `ψ(q)t`.

- If `ψ=1`, the scalar `t` satisfies `t²=2+8t`; the two roots are `d,d′`.
  The formal codegrees are `8+4t²=D,D′`.
- For any of the three nontrivial `ψ`, the relation is
  `t²=2ψ(α)`, with two roots. The duality `q* = q+α` gives formal codegree
  `8+4ψ(α)t²=16` for all six scalar irreducibles.
- The standard two-dimensional representation of `D8` extends with
  every `X_q` acting by zero: its central involution acts by `−I`, while
  that involution fixes every `X_q`. The group algebra formal codegree
  is `|G|/2=4`.

These eight scalar irreducibles and one degree-two irreducible exhaust
the semisimple algebra, since `8*1²+2²=12`. The regular Casimir therefore
has characteristic polynomial

\[
 (t-16)^6(t-8)^4(t^2-288t+2304).
\]

The element `v=1+Σ_q X_q` is central. It acts by `1` on every rational
block above and by `1+4d=D/D′`, respectively `1+4d′=D′/D`, on the two
remaining blocks.

## Categorical implication and degree normalization

In a pseudo-unitary realization, let `B⊂I(1)` be the distinguished
central simple corresponding to the Galois-conjugate FP character.
For an irreducible `E` of degree `e_E`, write `f_E` for its formal codegree
and `λ_E(v)=χ_E(v)/e_E` for the eigenvalue of a central element. The
induction-character identity and modular `S` symmetry imply

\[
 \lambda_E(FB)=f_E/\sigma(f_E).
\]

Indeed, `dim A_E=D/f_E`, `dim B=D/σ(D)`, and the two symmetric
`S` entries are `(D/f_E)λ_E(FB)` and `D/σ(f_E)`. The irreducible
degree is accounted for by `λ_E=χ_E/e_E`. The regular Casimir acts by
`e_E f_E`; its Galois ratio is the same because `e_E` is rational.
There is therefore no missing factor of two on the matrix block.

All central eigenvalues of `FB` and `v` agree. Faithfulness of the full
semisimple algebra, and centrality of `FB`, give the exact restriction

\[
                  \boxed{F(B)=1+X_0+X_1+X_2+X_3.}
\]

In particular, every `X_q` has multiplicity exactly one, which is the
input needed by the separate parity argument.

## General-complex scope

The actual certificate is in the tracked archive
`evidence/rank9_m2_20261024/replay.zip`, under
`Rank9_M2_Theoretical_Continuation_20261023/phase2/signed/gate_R9_2_1975.json`.
The archive has SHA-256
`38b4339c86c71fdba65cc7a72df57b16248b508f11dbe8fdb2016c43d77e6ff2`,
matching its published source manifest. Both the certificate and the
current `data/current_remaining_cases.py` tensor have tensor SHA-256
`8b30652d59e868a120b6c423e46a99ab51f6032af752dc0082a3d80fd9e61323`.

**Fresh replay passed.** The archived independent eight-bit verifier rebuilt
the 28-variable, 199-equation oriented signed problem, checked both branch
certificates and complete gauge/automorphism orbits, and returned `UNSAT`
after their removal. The run took under one second. Every integer
associativity difference has absolute value at most 72, so its eight-bit
zero test is exact. The current tensor is supplied directly, rather than
trusting an archived copy. The retained verifier uses assertions, and the
wrapper refuses optimized Python to ensure those checks remain active.

The small signed spectrum has a transparent explanation. After the permitted
gauges, the first branch is the original tensor. Its only nonzero,
equal-dual scalar dimension vectors are

\[
 (1,d,d,d,d,1,1,1,2),\qquad d=4\pm3\sqrt2.
\]

Their intrinsic global dimensions are `144±96 sqrt(2)`. In the second
signed branch, the corresponding vectors have all four noninvertible
entries equal to `sqrt(2)` or all equal to `-sqrt(2)`, yielding global
dimension `16`. This branch is impossible: the original scalar formal
codegree `f=144+96 sqrt(2)` gives a scalar formal codegree `2f` of the
sphericalization, of global dimension `2*16`. The quotient `16/f` would
therefore be an algebraic integer, but its field norm is `1/9`.
Every other scalar character in either branch either has a zero simple
dimension or assigns opposite nonzero dimensions to dual pairs
`b1↔b2` and `b3↔b4`; neither can be a spherical dimension character.

Consequently every categorification's intrinsic global dimension is a
Galois conjugate of the FP global dimension. Number-field descent and Galois
transport give the required **existence reduction** to a pseudo-unitary
category of the same source ring. This conclusion does not assume a
pivotal structure on the original category: the enumeration is performed
on its canonical sphericalization's signed quotient.

Reproduce this source-bound check with `python replay_r1975_gate.py`.
The exact output is `r1975_gate_replay_receipt.json`; extracted-file hashes
and the archive identity are in `r1975_gate_provenance.json`. Only the
twenty files required for this replay are retained in `r1975_gate_replay/`.

Apply the actual subgroup-algebra Morita reduction to that representative.
ENO, *On fusion categories*, Theorem 2.15, preserves intrinsic global
dimension under this duality; Corollary 8.14 preserves FP dimension.
Consequently the resulting rank-twelve Morita category is pseudo-unitary.
Its canonical positive spherical structure permits the argument above.
This route does not assert that every original category was unitary or
pseudo-unitary, and it does not require transporting a chosen positive
spherical structure through an arbitrary Galois embedding.

Primary sources checked directly:

- T. Deshpande, *On centers of bimodule categories and induction-restriction
  functors*, <https://arxiv.org/pdf/1611.04486>, Proposition 2.8 and §2.7.
- P. Etingof, D. Nikshych, V. Ostrik, *On fusion categories*,
  <https://arxiv.org/pdf/math/0203060>, Theorem 2.15 and Corollary 8.14.

The project's prior independent normalization audit is
`evidence/rank9_m2_20261024/proofs/phase3/audit_quadratic_symmetry/GALOIS_UNIT_AUDIT.md`.
The tensor binding and relative-center parity theorem remain the other
investigators' separate checks; no final exclusion is asserted in this
note alone.
