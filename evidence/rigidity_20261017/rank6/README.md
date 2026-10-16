# Rank-six necessary conditions

**AI-generated research · independent verification pending.** The research and data have not been independently verified by a human mathematician or formalized in Lean.

Both **R6_4_155** and **R6_8_1660** remain unresolved. This package records theoretical constraints and exact surviving data; it supplies neither a categorification nor a general exclusion.

- For R6_4_155, odd generalized pivotal rotations must factor through a cyclic spin character. All 1,144 tested blocks pass. The all-order path-Clifford divisibility condition for R′(m) is equivalent to m being even, and hence holds at m=4.
- For R6_8_1660, saturated modular representations determine every indicator and every central phase mass. The eight spin objects form four dual pairs, each restricting to 2X+2gX+sigma+3T. The exact phase Gram constraints leave 640 labelled restriction profiles, in branches of 68,286,286. These are restriction-data profiles, not categories.

The central fermion also supplies local Clifford constraints on T=sigma X in the second case. Their basic divisibility is automatic at all tensor powers because sigma^(2k)=2^(k−1)(1+g) and sigma^(2k+1)=2^k sigma. This observation does not resolve either case. No exploratory extra cyclic calculation is used by this publication package.

Run from the repository root:

```sh
python evidence/rigidity_20261017/rank6/run_checks.py --repo .
python -O evidence/rigidity_20261017/rank6/run_checks.py --repo .
```

These commands verify the package manifest and prerequisite identities, then replay both complete case checkers, including their independent arithmetic audits and invalid-input controls. Optimization is forwarded to all child checkers. Each command emits one JSON result; `--output PATH` also saves it. Python 3.10 or later and SymPy are required.

For an inexpensive identity and status check:

```sh
python evidence/rigidity_20261017/rank6/run_checks.py --repo . --metadata-only
```

`MANIFEST.json` binds every published file in this rank-six evidence directory and the exact external inputs. `research_progress.json` binds the prerequisite research manifest and states the scope of every result. The two case directories contain their proofs, exact checkers and receipts. The independent mathematical review is in `publication_rank6_audit.md`.

The manuscript arguments and arithmetic replays have different roles: the replays verify their specified finite identities; they do not formalize the categorical proofs or establish the existence of compatible associators.
