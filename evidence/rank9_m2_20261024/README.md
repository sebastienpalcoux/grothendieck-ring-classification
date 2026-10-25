# Rank-nine fusion rings of exact multiplicity two

<!-- correctness-20261025 -->
**Correctness revision · 25 October 2026.** The current classification is unchanged. Three model-identification arguments are repaired, R8_3_721 has a direct exact completion, and implementation/replay defects are corrected. [Findings, corrections and exact commands](../../evidence/correctness_20261025/README.md). Independent human verification remains pending.
<!-- /correctness-20261025 -->

**2,083 rings: 2,043 general complex exclusions, 36 unitary models, four unresolved.**

[Ledger](ledger.json) · [CSV](ledger.csv) · [Models](models.json) · [Open cases](unresolved.json) · [Manuscript](../../publications/rank9-m2/paper/rank9-m2.pdf) · [Historical source archive](replay.zip)

The four unresolved IDs are R9_2_137,1607,1975,1976. They share dimension type (1^4,2,(4+3sqrt(2))^4). Braided categorification is excluded for all four; general existence remains open. The three commutative cases have a common necessary frontier of two uniform D8 Morita types, with forced pointed associator restrictions. These rings are not claimed to be categorical models.

The current archive authority is `phase5/results/ledger.json`. The old archive's root `verify.py` checks phase five; `--baseline` adds phase four, not phases one–three. Use the new all-phase entry point from the repository root:

```bash
python3 evidence/correctness_20261025/replay_rank9.py \
  --output-dir /tmp/rank9-current-complete --frontier --jobs 2
```

It verifies the unchanged archive before each stage, supplies the two separately bound missing phase-three certificates, replays the accepted baseline and phases two–five, and regenerates the model tensors. R920 uses an explicitly labelled exact pseudo-Boolean fallback, sharing the discovery implementation; no successful independent eight-bit replay is claimed. Stored group/cohomology narrowing records are checked here. Their fresh full regeneration is in the dated audit archive. Separate categorical premises remain explicit.

```bash
python3 evidence/correctness_20261025/replay_rank9.py \
  --output-dir /tmp/rank9-current-complete --frontier --jobs 2
```

It verifies the unchanged archive before each stage, supplies the two separately bound missing phase-three certificates, replays the accepted baseline and phases two–five, and regenerates the model tensors. R920 uses an explicitly labelled exact pseudo-Boolean fallback, sharing the discovery implementation; no successful independent eight-bit replay is claimed. Stored group/cohomology narrowing records are checked here. Their fresh full regeneration is in the dated audit archive. Separate categorical premises remain explicit.

The [fourth-continuation proofs](proofs/phase4/REPORT.md) settle six exclusions and three models. The [fifth-continuation proofs](proofs/phase5/REPORT.md) add four general exclusions and one unitary model. Their 14 case changes are bound in the [publication reconciliation](../research_20261024/accepted.json). The archive also preserves the earlier correction of invalid half-E6 subring claims. Absence from a positive catalogue is never an exclusion criterion.

All readable current proofs appear once on this evidence shelf. The archive contains complete code, finite certificates, constructors and prior snapshots. Downloaded primary papers are cited by URL/hash rather than redistributed. Exact computational replay and AI-based categorical review do not replace independent human verification or formalization.
