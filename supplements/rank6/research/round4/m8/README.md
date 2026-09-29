# Fourth-continuation multiplicity-eight campaign

Two new general exclusions are proved: `R6_8_311` and `R6_8_3664`.
`R6_8_1660` remains unresolved, with an exactly verified necessary-relaxation
witness. Census tensors and all inherited certificates are unchanged.

## Accepted general certificates

| Ring | Direct certificate | Full-tensor verifier | Low frames | Exact rays |
| --- | --- | --- | ---: | ---: |
| R6_8_311 | `R6_8_311_certificate.json` | `round4_m8_ising.verify_general` | 2 | 16 |
| R6_8_3664 | `R6_8_3664_certificate.json` | `round4_m8_subfield.verify_general` | 13 | 2 |

The new uniform necessary condition projects central objects onto a fusion
subcategory and preserves the twist. For Fibonacci, low twist-one restriction
columns satisfy `c_fib <= c_unit`; high columns with a nonzero Fibonacci
coordinate can only have the two Fibonacci twists. For Ising, low twist-one
columns satisfy `c_sigma = 0` and `c_g <= c_unit`; high columns have the exact
Ising-supported twist sets and twist-resolved dimension masses.

The Fibonacci implementation computes normalized traces in the complete
biquadratic character field Q(sqrt(5),sqrt(6)), rather than its degree-32
cyclotomic ambient field. Conductor 120 and height three give 43 projected
trace types. Four of the target's 13 low frames fail inherited moment bounds,
three fail Fibonacci projection, four lack compatible character labels, and
two fail exact linear feasibility: (equations, variables) = (708,2184) and
(663,1792).

The Ising implementation retains the complete character field in Q(zeta_24).
Conductor 24 and height three give 53 trace types. The two low frames each
have two character labellings and four indicator choices; all 16 branches
have exact rays. Their systems have sizes (387,802) and (1017,1896).

Unrestricted signed sphericalization reductions precede both pseudo-unitary
obstructions: respectively 96 and 768 quotients, eight and 24 sign orbits, and
13 and 36 nongauge dimension-character rejections. Each leaves exactly the
original ring's FP Galois orbit as a possible categorical dimension component.

Both proofs passed normal and optimized Python replay with LP/MILP optimizers
disabled. Each passed eight deliberate-corruption checks. The Fibonacci
proof also has an independent replay under `research/round4/models/`.

```sh
python research/round4/m8/replay.py
python -O research/round4/m8/replay.py
python -O research/round4/m8/mutation_audit.py
python research/round4/m8/replay_311.py
python -O research/round4/m8/replay_311.py
python -O research/round4/m8/mutation_311.py
```

## Propagation and controls

`controls.json` and `ising_controls.json` each include all ten frozen
frontier inputs and all 54 known realizations. Fibonacci: one frontier target,
nine ineligible; three known-model controls survive, 51 are explicitly outside
the implementation. Ising: three frontier targets are handled in targeted
campaigns (R6_4_91 in its separate campaign); seven are ineligible. One model
control survives and 53 are explicitly outside the implementation. These
completed scans have no timeouts or errors.

The census structural screens find 443 Fibonacci and 150 Ising subring
cases among 16,612 tensors. These are eligibility screens, not additional
full exclusion replays. Their rows preserve inherited classification status.

## Remaining ring R6_8_1660

Its unrestricted signed reduction succeeds: 640 quotients, 24 sign orbits,
and 58 nongauge character rejections. Ising support and mass equations survive
through height six. The height-three low-Verlinde/restriction-product refinement
also survives, including the tested parity criterion.

`1660_necessary_witness.json` is an exact rational feasible point for that
1,304-equation, 2,007-variable necessary relaxation. It has 278 nonzero entries
and is replayed with optimizers disabled by:

```sh
python -O research/round4/m8/replay_witness_1660.py
```

This witness has fractional counts: it is not an integral induction matrix,
modular datum, or category. `1660_normalized_galois.json` additionally checks joint character signatures
augmented by the normalized dimension square `d_Z^2/D^2`. The existing exact
point satisfies all 252 added equations, giving 1,556 equations in total.
`1660_integer_frames.json` records the separate 60-second integral-Gram
enumeration budget: 1,027,399,680 nodes and 1,781,812 partial frames, with
incomplete coverage. No obstruction is inferred from this interruption.
Morita reconstruction over `1+g` returns the same based ring, so does not
transfer the exclusion of the non-self-dual partner.

The unpruned `3664_subfield_h3.json` is historical discovery evidence from before
Fibonacci support was imposed and is not accepted by the strengthened verifier.

Primary background: Ng--Schauenburg, *Frobenius--Schur Indicators and Exponents
of Spherical Categories*, arXiv:math/0601012; Ng--Schauenburg, *Congruence
Subgroups and Generalized Frobenius--Schur Indicators*, arXiv:0806.2493.
The new projection and subfield arguments are proved in the fourth-continuation
manuscript chapters.
