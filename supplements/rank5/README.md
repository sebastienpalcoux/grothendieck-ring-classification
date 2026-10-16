# Rank-five classification through multiplicity twenty

> **AI-generated research · independent verification pending.** Treat these
> results, proofs, code and data with caution. They have not yet been
> independently verified by human experts or formalized in Lean. Automated
> checks establish only their stated computational scope.

The classification records **17 realized and 40,982 excluded rings among
40,999 inputs**, with no open case through multiplicity twenty. Every recorded
model is unitary. The unrestricted classification remains a separate question.

[Current manuscript](../../manuscripts/rank5/papers/manuscript.pdf) ·
[TeX sources](../../manuscripts/rank5/papers/manuscript.tex) ·
[Complete public replay package](../../evidence/prepublication_20261017/rank5/README.md)

The complete public replay reconstructs all 40,999 decisions from pinned
census tensors and proof sources, including inert-prime parity and the
multiplicity-19–20 extension. Use this entry point from the repository root:

```bash
python3 tools/restore_data.py
python3 evidence/prepublication_20261017/rank5/replay.py --check-package
python3 evidence/prepublication_20261017/rank5/replay.py --jobs 2
python3 -O evidence/prepublication_20261017/rank5/replay.py --jobs 2
```

The package guide specifies the pinned dependencies and C++17 compiler
requirement. Both complete runs passed and produced byte-identical ledgers
with SHA-256 `12886636134e0500a403ae1b635f5b901612d64b203dad1e1fdf94b0da2c31f1`.
The ledger is reconstructed; unavailable source-archive bytes are not claimed
to have been recovered. No private attachment is required.

The compact source files in this directory support individual criteria and
tensor crosswalks. Their standalone `verify.py` does not cover every criterion
in the through-twenty classification and is not a substitute for the complete
public replay. See [verification scope](../../docs/PREPUBLICATION_REVIEW.md) and
[provenance](../../docs/PROVENANCE.md).
