# Upper-rank recovery checkpoint, 2 October 2026

This branch preserves 38 approved further decisions: **25 general exclusions and 13 unitary models**. The working census has **42 unresolved rank-7 cases and 60 unresolved rank-8 cases**. The complete classification remains open. The baseline published release is commit `7c78b88486d5412adeed10d77275e3eaa2de0b7d`; this checkpoint does not claim a synchronized manuscript/website release.

| Rank and exact multiplicity | Rings | General exclusions | Unitary models | General unresolved |
|---|---:|---:|---:|---:|
| 7, 1 | 43 | 30 | 13 | 0 |
| 7, 2 | 319 | 301 | 10 | 8 |
| 7, 3 | 1059 | 1045 | 2 | 12 |
| 7, 4 | 2780 | 2756 | 2 | 22 |
| 8, 1 | 96 | 45 | 48 | 3 |
| 8, 2 | 877 | 796 | 24 | 57 |

The 36 earlier new decisions had source-bound checks and independent mathematical audits before the environment failed. The new R8_2_694 exclusion and R8_2_868 model received independent theoretical audits during recovery. The remote published census was recovered; all 973 rank-8 tensor fingerprints matched the published decision ledger. Fresh exact checks establish R694's theorem premises and all 512 coefficients of the R868 model. Rank-7 census source order and rank-8 lexicographic tensor order are different; the recovery verifier preserves each identifier convention.

- `decisions.json` preserves every new decision, its scope, source tensor fingerprint and model basis map.
- `previous_records.json` preserves all 140 original general-open inputs.
- `remaining_ids.json` lists the 102 general-open cases after the 38 transitions.
- `retained_research.md` records the previous theoretical arguments and their exact limits.
- `R694_DIM28_GRADING_PROOF.md` and `R868_HI7_DUAL_PROOF.md` are self-contained recovery proofs.
- `scoped_results.json` keeps pivotal/unitary/pseudo-unitary/braided results separate from general exclusions.
- `verify_recovery.py` is a standard-library checker for source binding, counts, R694 premises, and the independently constructed R868 tensor. It does not replace the inaccessible 36 original proof/certificate replays.
- `oeis_comment_draft.txt` is copyable proposal text, not an OEIS submission.

Run after checking out this branch:

```sh
python3 evidence/upper_residual_20261002b_recovery/verify_recovery.py
python3 -O evidence/upper_residual_20261002b_recovery/verify_recovery.py
```

Both rank-six cases remain unchanged while the user's laptop computation runs. The R160 proposed negative unitary witness was rejected because it was not a common fusion character; no new unitary exclusion of R160 is claimed. Central lifts in the three rank-eight multiplicity-one cases are not automatically bosons. A central fermion may fix underlying simple objects, so that route has an explicit gap.

The workspace connection failed before complete stage replays, table regeneration, PDF compilation, archive rebuilding and website publication. The pre-failure files cannot currently be accessed; their survival has not been established. The remote baseline is intact. All publication flags in `checkpoint.json` remain false until those tasks actually pass.
