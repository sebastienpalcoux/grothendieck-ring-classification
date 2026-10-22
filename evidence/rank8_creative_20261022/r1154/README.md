# R1154: reconstruction of a forced semionic center packet

**R8_3_1154 remains unresolved.** The new necessary structural theorem is
in [PROOF.md](PROOF.md). It combines pointed-indicator saturation, the
previously forced A2 projector, the exact STS relation, charge conjugation,
and Verlinde integrality.

It uniquely determines the four full S columns belonging to I(g), forces
two non-self-dual pairs with twists +i,+i,−i,−i, and reconstructs all four
full fusion matrices. The two other possible two-dimensional STS blocks
are excluded by irrational fusion-matrix differences. Every one of the
25 current pair histograms on all three patterns passes the resulting
nonnegative-integral fusion-matrix checks. No full center or category is
constructed.

## Replays

Run all four accepted result families with the read-only aggregator:

    python3 evidence/rank8_creative_20261022/r1154/verify.py

It recomputes and compares the complete receipts in memory without
updating checked-in files. The standalone producer scripts below write
their own receipts.

- `verify_semionic_packet.py` / `semionic_packet.json`: the 25-branch
  packet reconstruction. All results are exact; no numerical optimizer is
  used in this proof. The normal and optimized invocations pass.
- `verify_quartic_witness.py` / `quartic_witness_replay.json`: one exact
  fourth-product extension on pattern6971/pair histogram1. All4,900 Gram
  entries through degree eight and all560 restriction entries agree.
  Its70 word vectors span rank11. This witness only shows that this
  higher-moment relaxation survives.
- `verify_packet_closure.py` / `packet_closure.json`: exact tensor support
  and simultaneous commutant on all 25 branches, proved in
  [PACKET_CLOSURE.md](PACKET_CLOSURE.md). Every packet object and its dual
  generate the full center within two tensor steps. The forced operators
  leave a common scalar space of dimension n−9.
- `verify_quantum_subgroup_route.py` / `quantum_subgroup_route.json`:
  all 72 simple dimensions in SU(3)_7 tensor Fib. Their global dimension
  is 5D, but a positive field-coordinate criterion excludes an algebra
  of dimension 5, hence excludes this direct connected-etale module
  construction. See [QUANTUM_SUBGROUP_ROUTE.md](QUANTUM_SUBGROUP_ROUTE.md).

The semionic packet theorem has passed the separate automated review in
[R1154_PACKET_REVIEW.md](../unified/audits/R1154_PACKET_REVIEW.md).

## Other attempts and precise limits

`completion_probe.py` couples symmetric integral N1 entry bounds,
forgetful intertwining, five low spectral columns, commutation with the
three forced operators, the forced four-copy difference action, trace,
and the complete squared Frobenius norm. A necessary matrix was found
for pattern8766/pair histogram1 and every imposed equation was checked
exactly. Its characteristic polynomial differs from the mandatory one;
therefore it is not a central fusion-matrix solution. The script uses
SciPy/HiGHS only for discovery and makes no infeasibility assertion.
`completion_probe_results.json` preserves that matrix and polynomial.

`galois_forgetful_probe.py` extends the existing reciprocal-Galois
bilinear check from the five low coordinate vectors to those vectors
plus all eight restriction rows. Every one of the25 previously chosen
Galois witnesses passes. It supplies no further exclusion.

`quartic_projection_probe.py` derives the rank-one residual fourth-word
Gram domain. `quartic_extension_results.json` records **one** exact
survivor, which is independently replayed above. An attempted broader
joint enumeration was interrupted before a complete census; its log
`quartic_probe_1000.log` is not an exclusion certificate. No completeness
is claimed for that search.

`semionic_block_probe.py` / `.log` are discovery scratch calculations,
superseded by the clean proof and `verify_semionic_packet.py`.

All sources written in this folder are additive. Frozen earlier evidence,
classification ledgers, manuscripts and website files were left unchanged.
