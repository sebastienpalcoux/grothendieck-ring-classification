# Fourteen further general exclusions

This continuation excludes fourteen previously unresolved census rings as
fusion categories over the complex field. No pivotal, spherical,
pseudo-unitary or unitary structure is assumed on the proposed ambient category.
The proofs use the following necessary criteria.

| Criterion | Cases | Exact replay |
| --- | --- | --- |
| Relative-trace ideal bound after sphericalization | R7_4_1417, R7_4_1420 | `r7_relative_trace/verify_relative_trace.py` |
| Two-row induction forces a central boson and impossible descent | R7_2_160 | `r7_central_boson/verify_r160.py` |
| Galois-invariant pointed associator incompatibility | R8_2_312, R8_2_315, R8_2_317 | `r8_associators/verify_r312.py`, `r8_associators/verify_psu_pointed.py` |
| Square-order normal abelian kernels force integral extensions | R8_2_53, R8_2_93, R8_2_191, R8_2_299, R8_2_158, R8_2_186, R8_2_579, R8_2_682 | `r8_extension_integrality/verify_r53_r93.py`, `verify_r191_r299.py`, `verify_dim48_four.py` |

Each proof has a separate categorical hypothesis audit and exact source-bound
replay. The ordinary PSU(2)_6 calculation has only three induction patterns;
its fixed integer separating vectors are checked without an optimization solver.
The intermediate dimension-12 classification checks every oriented table and
both valid C4 actions; six tables pass associativity and exactly two have the
required outer involution. The finite-group checks enumerate 38 subgroups of
the group of order 36, 10 of A4, and 30 of S4.

The resulting partition, within the complete attached census bands, is:

| Rank | Multiplicities | General exclusions | Unitary models | General questions open |
| --- | --- | ---: | ---: | ---: |
| 7 | 1–4 | 4135 | 27 | 39 |
| 8 | 1–2 | 857 | 72 | 44 |

All integral and weakly integral rank-eight cases within these bands are now
decided. The remaining rank-eight cases have irrational global FP dimension.
The rank-six frontier remains R6_4_155 and R6_8_1660, pending further evidence
including the user's local computation.

Run from the repository root:

```sh
python3 tools/verify_upper_residual_20261002c.py
python3 -O tools/verify_upper_residual_20261002c.py
```

The verifier pins every proof dependency, checks every ledger transition and
unchanged record, restores the exact published parent ledgers and software in
an isolated temporary copy, then replays the frozen
[43-decision parent stage](../upper_residual_20261002b/README.md). The parent
proofs and receipts retain their original bytes. Together the two stages resolve
57 further rings: 44 general exclusions and 13 unitary models.

`remaining_ids.json` is the complete current frontier. Files in `scoped_research`
are necessary-condition reductions for open cases and do not assign negative
classification decisions. In particular R7_4_1212/R7_4_1213 remain generally
unresolved despite their pivotal exclusions and smaller signed-character frontier.
