# Source-bound replay of the three commutative rank-nine gates

**All three pass.** The gate certificates were extracted from the actual
tracked `evidence/rank9_m2_20261024/replay.zip`, SHA-256
`38b4339c86c71fdba65cc7a72df57b16248b508f11dbe8fdb2016c43d77e6ff2`.
This equals the archive identity in the published source manifest.
Inside the archive, the root is
`Rank9_M2_Theoretical_Continuation_20261023`; the certificates are
`phase2/signed/gate_R9_2_<ID>.json`.

The unchanged independent eight-bit verifier rebuilt the oriented signed
associativity problems, replayed the scalar-character obstructions and
global-dimension gates, blocked their complete permitted gauge/automorphism
orbits, and obtained `UNSAT` in each case. Assertions were active. Each
input came directly from the current `data/current_remaining_cases.py`,
and its SHA-256 matched the corresponding archived certificate.

| Ring | Signed representatives | Orbit tables blocked | Completeness | Seconds |
|---|---:|---:|---|---:|
| R9_2_137 | 6 | 12 | UNSAT | 2.29 |
| R9_2_1607 | 10 | 14 | UNSAT | 2.07 |
| R9_2_1976 | 8 | 15 | UNSAT | 3.85 |

Tensor SHA-256 values:

- R137: `c509d23c9a638aaea8a624a6c5186ad3f0c1b6e6f432576b45300f6e630c56e6`.
- R1607: `16b023a44f69bb516b8a8c9933a2b360b44219a07de2f1599e8f216eb74dbfa2`.
- R1976: `2280410fa5b33121f9b5d9cfdea15f90bf56933f9b26c0ccdbe047c153d08d30`.

The conclusion is a general-complex **existence reduction** to a
pseudo-unitary Galois conjugate with the same fusion ring. It supplies the
scope prerequisite for the new categorical arguments, and by itself is
neither a model nor an exclusion.

Reproduce with `python replay_rank9_signed_gates.py`; it imposes a
twenty-second overall check limit and refuses Python `-O`.
`rank9_signed_gates_replay_receipt.json` contains the exact outcomes.
`rank9_signed_gate_provenance.json` binds all retained source files to
their extracted hashes and the frozen public archive identity.
The same minimal source folder is shared with the separately replayed
R1975 gate; no solver search for new categories or long computation was used.
