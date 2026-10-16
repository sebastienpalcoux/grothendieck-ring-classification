# Unrestricted rank-four proof: independent AI audit evidence

**AI-generated research · independent verification pending.** These reviews and
checks are supporting research evidence. They are not independent human
verification or a Lean formalization of the categorical proof.

Five mathematical reviews cover the structural arguments, quadratic field,
cubic field and pivotal bound, quartic field, and complete finite certification.
The current proof is in `manuscripts/rank4/papers/companion.tex`; the standalone
finite certificate package is in `supplements/rank4/unrestricted/`.

From the repository root, run:

```sh
python evidence/rank4_unrestricted_20261017/run_checks.py
python -O evidence/rank4_unrestricted_20261017/run_checks.py
```

The six independent programs verify algebraic identities, character charts,
rational inequalities, and exact quartic root/Galois calculations. SymPy is
required. Every check remains active under Python optimization. Quadratic
endpoint comparisons use exact algebraic signs. The cubic receipt binds the
current cubic and pivotal-bound section files; the quartic programs read the
canonical exact chart in the computational package.

`MANIFEST.json` binds the audit and checker sources, the three canonical input
files, and the exact contents of the six result receipts. Elapsed times are
excluded from receipt comparison. `--repository-root PATH` supports a separately
extracted evidence directory with an accompanying repository or research bundle.
The maintainer option `--write-manifest` records a fully successful replay.

For the complete finite classification replay, from its package directory run:

```sh
python supplementary/check.py --deep
python verify_package.py
```

The theoretical arguments give `FPdim < 1000` and multiplicity at most 31
before enumeration. Exact certification then gives fifteen rank-four rings,
sphericality of every categorification, and the sharp bounds
`FPdim ≤ 24 + 12√3` and multiplicity at most 6. The categorical implications
depend on the mathematical proofs and cited existence results; executable
arithmetic alone does not establish them.
