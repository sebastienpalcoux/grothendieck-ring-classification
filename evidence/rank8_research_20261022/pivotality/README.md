# Four general-to-spherical reductions

The authoritative proof is [PROOF.md](PROOF.md), with the complete receipt
`general_spherical_gates.json` and reproducible verifier
`verify_general_spherical_gates.py`.

```sh
python3 evidence/rank8_research_20261022/pivotality/verify_general_spherical_gates.py
```

Every complex categorification of `R8_3_982`, `R8_3_1768`, `R8_3_1795` or
`R8_3_3472` admits a spherical structure and has a pseudo-unitary Galois
conjugate. This supplies neither a model nor a general unbraided exclusion.

The first three proofs use full signed parity domains modulo a justified
basis-sign normalization. Their complete unrestricted counts are respectively
96, 3136 and 4672. All nongauge-original classes fail exact dimension-character
tests. The fourth proof uses positive-second-indicator lifts and their proved
modulo-four conditions, with no additional sign gauge; its unique signed
solution is the original tensor.

Independent review and replay are in
`../r928_r941/PIVOTALITY_REVIEW.md`,
`../r928_r941/pivotality_independent_review.json`, and
`../r928_r941/pivotality_optimized_replay.log`.

The `probe_*` files and separate case JSONs retain the exploratory calculation.
In particular, the unrestricted R3472 search in `probe_signed.log` timed out
and supplies no conclusion. It is not used by the authoritative proof or
verifier. The completed indicator-normalized search is categorically justified
separately in the proof.
